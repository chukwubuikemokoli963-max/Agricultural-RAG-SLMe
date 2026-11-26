
import re

CROP_GROUPS = {
    "cassava": ["cassava", "casava", "kasava"],
    "maize": ["maize", "corn"],
    "rice": ["rice"],
    "yam": ["yam", "yams"],
    "tomato": ["tomato", "tomatoes"],
    "pepper": ["pepper", "peppers"],
    "groundnut": ["groundnut", "groundnuts"],
    "cowpea": ["cowpea", "cowpeas"],
    "banana": ["banana", "bananas"],
    "plantain": ["plantain", "plantains"],
    "wheat": ["wheat"],
    "barley": ["barley"],
    "millet": ["millet"],
    "sorghum": ["sorghum"],
    "potato": ["potato", "potatoes"]
}

CEREALS = {
    "maize", "rice", "wheat",
    "barley", "millet", "sorghum"
}

DROUGHT_PATTERN = (
    r"drought|rain no dey fall|"
    r"rainfall is insufficient|"
    r"lack of rain|no rainfall|"
    r"no rain\b|insufficient rain|"
    r"dry spell|water shortage"
)

ACTION_PATTERN = (
    r"\b(plant|grow|mulch|harvest|"
    r"collect|store|irrigate|conserve|"
    r"incorporate|remove|monitor|"
    r"select|apply|avoid|control|"
    r"maintain|reduce|use|space)\b"
)

WATER_PATTERN = (
    r"drought|water|rain|moisture|"
    r"irrigat|mulch|dry|"
    r"early.maturing"
)


def find_crops(text):

    text = str(text).lower()

    found = set()

    for crop, aliases in CROP_GROUPS.items():

        for alias in aliases:

            if re.search(
                r"\b" + re.escape(alias) + r"\b",
                text
            ):
                found.add(crop)

    return found


def passage_matches_crop(question, passage):

    target_crops = find_crops(question)

    passage_crops = find_crops(passage)

    if not target_crops:
        return True

    if passage_crops and not (
        target_crops & passage_crops
    ):
        return False

    if (
        re.search(r"\bcereals?\b", passage.lower())
        and not target_crops & CEREALS
    ):
        return False

    return True


def is_action_question(question):

    return bool(re.search(
        r"what should i do|wetin i go do|"
        r"how can i|how do i|"
        r"which manure|what manure|"
        r"how i go take|"
        r"manage|control|prevent|treat",
        question.lower()
    ))


def unsafe_quantity(passage):

    chemical = re.search(
        r"pesticide|herbicide|fungicide|"
        r"insecticide|fertili[sz]er|"
        r"urea|nitrogen|npk",
        passage.lower()
    )

    quantity = re.search(
        r"\d+(?:\.\d+)?\s*"
        r"(kg|mg|ml|grams?|litres?|liters?|ppm|%)",
        passage.lower()
    )

    return bool(chemical and quantity)


def passage_is_relevant(question, passage):

    if not passage_matches_crop(
        question, passage
    ):
        return False

    if unsafe_quantity(passage):
        return False

    if re.search(
        DROUGHT_PATTERN,
        question.lower()
    ):

        if not re.search(
            WATER_PATTERN,
            passage.lower()
        ):
            return False

        if re.search(
            r"\bflooding\b|\bwaterlogging\b|"
            r"\bexcess rainfall\b",
            passage.lower()
        ):
            return False

    if is_action_question(question):

        if not re.search(
            ACTION_PATTERN,
            passage.lower()
        ):
            return False

    if re.search(
        r"\bmanure\b",
        question.lower()
    ):

        if not re.search(
            r"manure|compost|organic matter|"
            r"green manure",
            passage.lower()
        ):
            return False

    return True


def refine_response(question, result):

    result = dict(result)

    eligible = {
        "extractive_evidence",
        "extractive_fallback"
    }

    if result.get("status") not in eligible:
        return result

    answer = str(result.get("answer", ""))

    sources = result.get("sources", [])

    source_map = {
        str(source.get("reference")): source
        for source in sources
    }

    passages = []

    seen = set()

    rejected = 0

    for line in answer.splitlines():

        match = re.match(
            r'^\s*-\s+["“](.+)["”]\s*\[(\d+)\]\s*$',
            line
        )

        if not match:
            continue

        passage = match.group(1).strip()

        reference = match.group(2)

        if reference not in source_map:

            rejected += 1
            continue

        if not passage_is_relevant(
            question, passage
        ):

            rejected += 1
            continue

        normalized = re.sub(
            r"\W+", " ", passage.lower()
        ).strip()

        if normalized in seen:

            rejected += 1
            continue

        seen.add(normalized)

        passages.append(
            (passage, reference)
        )

    result["quality_rejected_passages"] = rejected

    if not passages:

        result["answer"] = (
            "I could not find sufficiently relevant "
            "information to answer your question. "
            "Please provide your crop, location "
            "and more details about the problem."
        )

        result["status"] = "insufficient_evidence"

        result["sources"] = []

        return result

    references = {}

    new_sources = []

    lines = []

    for passage, old_reference in passages:

        if old_reference not in references:

            new_reference = len(references) + 1

            references[old_reference] = new_reference

            source = dict(
                source_map[old_reference]
            )

            source["reference"] = new_reference

            new_sources.append(source)

        new_reference = references[old_reference]

        lines.append(
            f'- "{passage}" [{new_reference}]'
        )

    result["answer"] = (
        "Relevant information from the available "
        "agricultural knowledge base:\n\n"
        + "\n\n".join(lines)
        + "\n\nThis information is not a confirmed "
        "diagnosis. Confirm your growing conditions "
        "with an agricultural extension officer."
    )

    result["sources"] = new_sources

    return result
