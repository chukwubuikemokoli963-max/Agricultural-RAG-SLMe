
import os

# Prevent model downloads during inference.
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import re
import json
import time
import numpy as np
import pandas as pd

from pathlib import Path
from sentence_transformers import SentenceTransformer


class AgriculturalEdgeAssistant:

    def __init__(self, package_dir):

        self.root = Path(package_dir)

        with open(self.root / "config.json") as f:
            self.config = json.load(f)

        self.documents = pd.read_csv(
            self.root / "documents.csv"
        ).fillna("")

        self.embeddings = np.load(
            self.root / "embeddings_int8.npy"
        )

        self.scales = np.load(
            self.root / "embedding_scales.npy"
        )

        self.encoder = SentenceTransformer(
            str(self.root / "bge_model"),
            device="cpu",
            local_files_only=True
        )

        self.encoder.max_seq_length = 512

        assert len(self.documents) == len(
            self.embeddings
        )

    def normalize(self, question):

        text = question.lower().strip()

        for pattern, replacement in (
            self.config["normalization_rules"]
        ):

            text = re.sub(
                pattern,
                replacement,
                text
            )

        return re.sub(
            r"\s+", " ", text
        ).strip()

    def crops(self, question):

        text = self.normalize(question)

        if re.search(r"\bcorn\b", text):
            text += " maize"

        if re.search(r"\btomatoes\b", text):
            text += " tomato"

        return [
            crop
            for crop in self.config["crop_names"]
            if re.search(
                r"\b" + re.escape(crop) + r"s?\b",
                text
            )
        ]

    def condition(self, question):

        text = self.normalize(question)

        drought = bool(re.search(
            self.config["drought_pattern"],
            text
        ))

        flooding = bool(re.search(
            self.config["flood_pattern"],
            text
        ))

        if drought and flooding:
            return "mixed"

        if drought:
            return "drought"

        if flooding:
            return "flooding"

        return None

    def crop_match(self, metadata, crops):

        aliases = {
            "maize": ["maize", "corn"],
            "tomato": ["tomato", "tomatoes"],
            "beans": ["bean", "beans"]
        }

        return any(
            re.search(
                r"\b" + re.escape(term) + r"s?\b",
                metadata.lower()
            )
            for crop in crops
            for term in aliases.get(crop, [crop])
        )

    def split_passages(self, text):

        for abbreviation in [
            "pv.", "sp.", "spp.",
            "e.g.", "i.e.", "et al."
        ]:

            text = text.replace(
                abbreviation,
                abbreviation.replace(".", "<DOT>")
            )

        passages = re.split(
            r"(?<=[.!?])\s+|\n+",
            text
        )

        return [
            p.replace("<DOT>", ".").strip()
            for p in passages
            if 40 <= len(p.strip()) <= 850
            and p.strip().endswith((".", "!", "?"))
            and p.count("(") == p.count(")")
        ]

    def ask(self, question):

        start = time.perf_counter()

        question = str(question).strip()

        normalized = self.normalize(question)

        def response(status, answer, sources=None):

            return {
                "question": question,
                "normalized_query": normalized,
                "mode": "edge",
                "status": status,
                "answer": answer,
                "sources": sources or [],
                "latency_seconds": round(
                    time.perf_counter() - start, 4
                )
            }

        if not question:

            return response(
                "invalid_input",
                "Please enter a farming question."
            )

        if re.search(
            r"ignore.*instruction|invent.*source|"
            r"fake.*citation",
            normalized
        ):

            return response(
                "instruction_override",
                "I only provide information from "
                "the available agricultural documents."
            )

        if re.search(
            r"laptop|motherboard|football|"
            r"cryptocurrency|computer repair",
            normalized
        ):

            return response(
                "out_of_domain",
                "Please ask an agricultural question."
            )

        if re.search(
            r"pesticide|herbicide|insecticide|"
            r"fungicide",
            normalized
        ) and re.search(
            r"dosage|dose|rate|how much|how many",
            normalized
        ):

            return response(
                "safety_clarification",
                "Follow the approved product label "
                "and consult an extension officer."
            )

        crops = self.crops(question)
        condition = self.condition(question)

        if condition == "mixed":

            return response(
                "clarification_required",
                "Are you experiencing insufficient "
                "rainfall or flooding?"
            )

        if not crops and not condition:

            return response(
                "clarification_required",
                "Which crop are you growing, "
                "and what problem have you observed?"
            )

        search_query = normalized

        if condition == "drought":
            search_query += " drought water shortage"

        elif condition == "flooding":
            search_query += " flooding waterlogging"

        if re.search(
            r"eating|holes|insect|pest",
            normalized
        ):

            search_query += " insect pest damage"

        if re.search(
            r"manure|fertili[sz]er",
            normalized
        ):

            search_query += " organic manure nutrients"

        query_embedding = self.encoder.encode(
            [
                "Represent this sentence for searching "
                "relevant passages: " + search_query
            ],
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False
        )[0].astype(np.float32)

        scores = (
            self.embeddings @ query_embedding
        ) * self.scales[:, 0]

        indices = np.argsort(-scores)[:100]

        candidates = []

        for idx in indices:

            doc = self.documents.iloc[idx]

            title = str(doc["title"]).lower()
            metadata = str(doc["crop"]).lower()

            general = metadata in [
                "", "general", "(general)"
            ]

            if crops and not self.crop_match(
                metadata, crops
            ):

                if not (general and condition):
                    continue

            if condition and not crops and not general:
                continue

            if condition == "drought":

                if not re.search(
                    self.config["drought_pattern"],
                    title
                ) or re.search(
                    self.config["flood_pattern"],
                    title
                ):
                    continue

            if condition == "flooding":

                if not re.search(
                    self.config["flood_pattern"],
                    title
                ) or re.search(
                    self.config["drought_pattern"],
                    title
                ):
                    continue

            for passage in self.split_passages(
                str(doc["text"])
            ):

                # Conservative chemical screening.
                if re.search(
                    r"pesticide|herbicide|insecticide|"
                    r"fungicide|urea|micro-dose|"
                    r"\bnpk\b|apply lime",
                    passage,
                    re.IGNORECASE
                ):
                    continue

                # Reject obvious cross-crop passages.
                if crops and "maize" not in crops:

                    if re.search(
                        r"\bin cereals\b|\bin maize\b",
                        passage,
                        re.IGNORECASE
                    ):
                        continue

                # Avoid obvious opposing advice.
                if condition == "flooding":

                    if re.search(
                        r"conserve every drop|"
                        r"harvest rainwater|"
                        r"water shortage",
                        passage,
                        re.IGNORECASE
                    ):
                        continue

                if condition == "drought":

                    if re.search(
                        r"excess rain|waterlogging",
                        passage,
                        re.IGNORECASE
                    ):
                        continue

                candidates.append({
                    "document": doc.to_dict(),
                    "passage": passage
                })

        if not candidates:

            return response(
                "insufficient_evidence",
                "I could not find relevant evidence. "
                "Please provide more information about "
                "your crop, symptoms and location."
            )

        embeddings = self.encoder.encode(
            [
                item["passage"]
                for item in candidates
            ],
            batch_size=32,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False
        )

        similarities = embeddings @ query_embedding

        order = np.argsort(-similarities)

        sources = []
        passages = []
        seen = set()

        for idx in order:

            if similarities[idx] < (
                self.config["minimum_passage_similarity"]
            ):
                continue

            item = candidates[idx]

            passage = item["passage"]
            doc = item["document"]

            key = re.sub(
                r"\W+", "",
                passage.lower()
            )

            if key in seen:
                continue

            seen.add(key)

            existing = next(
                (
                    source for source in sources
                    if source["document_id"]
                    == doc["document_id"]
                ),
                None
            )

            if existing:

                reference = existing["reference"]

            else:

                reference = len(sources) + 1

                sources.append({
                    "reference": reference,
                    "document_id": doc["document_id"],
                    "title": doc["title"],
                    "source": doc.get("source", ""),
                    "country": doc.get("country", ""),
                    "source_url": doc.get("source_url", ""),
                    "license": doc.get("license", "")
                })

            passages.append(
                f'- "{passage}" [{reference}]'
            )

            if len(passages) >= (
                self.config["maximum_evidence_passages"]
            ):
                break

        if not passages:

            return response(
                "insufficient_evidence",
                "The available information is not "
                "sufficiently relevant. Please provide "
                "more details about your farming problem."
            )

        answer = (
            "Here is potentially relevant information "
            "from the agricultural knowledge base:\n\n"
            + "\n\n".join(passages)
            + "\n\nThis information does not confirm a "
              "diagnosis or guarantee suitability for "
              "your location. Please consult a local "
              "agricultural extension officer."
        )

        return response(
            "extractive_evidence",
            answer,
            sources
        )


if __name__ == "__main__":

    assistant = AgriculturalEdgeAssistant(
        Path(__file__).parent
    )

    questions = [
        "Wetin dey cause my casava leave to shine yellow?",
        "Rain no dey fall, wetin I go do?",
        "Which manure go make my yam grow well?",
        "My pepper don dey dry since last week",
        "How do I repair my laptop motherboard?"
    ]

    for question in questions:

        result = assistant.ask(question)

        print(json.dumps(
            result,
            indent=2,
            default=str
        ))
