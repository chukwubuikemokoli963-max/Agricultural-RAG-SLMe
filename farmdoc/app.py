
import os

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"

import json
import time
import threading
import requests

from pathlib import Path
from gradio_client import Client
from edge_engine import AgriculturalEdgeAssistant
from farmdoc_ui import build_farmdoc, launch_farmdoc

ROOT = Path(__file__).parent

with open(ROOT / "farmdoc_config.json") as f:
    CONFIG = json.load(f)

REMOTE_URL = CONFIG.get("remote_url", "")
REMOTE_TIMEOUT = CONFIG.get(
    "remote_timeout_seconds", 8
)

# ==========================================
# LOCAL EDGE ENGINE
# ==========================================

edge_assistant = AgriculturalEdgeAssistant(ROOT)

remote_client = None
remote_lock = threading.Lock()


# ==========================================
# REMOTE AVAILABILITY
# ==========================================

def remote_available():

    if not REMOTE_URL.startswith(
        ("https://", "http://")
    ):
        return False

    try:

        response = requests.get(
            REMOTE_URL.rstrip("/") + "/config",
            timeout=2
        )

        if response.status_code != 200:
            return False

        return isinstance(response.json(), dict)

    except Exception:

        return False


# ==========================================
# REMOTE INFERENCE
# ==========================================

def remote_inference(question):

    global remote_client

    if not remote_available():
        raise ConnectionError(
            "Remote FarmDoc unavailable"
        )

    with remote_lock:

        if remote_client is None:

            remote_client = Client(
                REMOTE_URL,
                verbose=False,
                httpx_kwargs={
                    "timeout": REMOTE_TIMEOUT
                }
            )

        job = remote_client.submit(
            question,
            api_name="/farmdoc_api"
        )

        try:

            result = job.result(
                timeout=REMOTE_TIMEOUT
            )

        except Exception:

            job.cancel()
            remote_client = None
            raise

    if isinstance(result, str):
        result = json.loads(result)

    if not isinstance(result, dict):
        raise ValueError("Invalid remote response")

    if not isinstance(result.get("answer"), str):
        raise ValueError("Missing remote answer")

    if result.get("status") == "error":
        raise RuntimeError("Remote inference failed")

    return result


# ==========================================
# AUTOMATIC ENGINE SELECTION
# ==========================================

def ask_farmdoc(question, force_edge=False):

    question = str(question or "").strip()

    if not question or len(question) > 1000:

        return {
            "answer": (
                "Please enter a farming question "
                "of no more than 1,000 characters."
            ),
            "sources": [],
            "status": "invalid_input",
            "edge": force_edge or not remote_available()
        }

    if not force_edge:

        try:

            result = remote_inference(question)

            result["edge"] = bool(
                result.get("edge", False)
            )

            return result

        except Exception as error:

            print(
                "Remote unavailable; "
                "using local edge engine:",
                type(error).__name__
            )

    result = edge_assistant.ask(question)

    result["edge"] = True

    return result


# ==========================================
# FORMAT SUPPORTING EVIDENCE
# ==========================================

def format_sources(sources):

    if not sources:
        return "No supporting documents returned."

    sections = []

    for source in sources:

        section = (
            f"### [{source.get('reference', '')}] "
            f"{source.get('title', 'Untitled')}\n\n"
            f"Document ID: "
            f"{source.get('document_id', '')}\n\n"
            f"Source metadata: "
            f"{source.get('source', '')}\n\n"
            f"Country metadata: "
            f"{source.get('country', '')}\n\n"
            f"License label: "
            f"{source.get('license', '')}\n\n"
        )

        if "synthetic" in str(
            source.get("license", "")
        ).lower():

            section += (
                "Synthetic benchmark evidence; "
                "not an independently verified "
                "official publication."
            )

        sections.append(section)

    return "\n\n---\n\n".join(sections)


# ==========================================
# INTERFACE HANDLER
# ==========================================

def interface_response(question):

    try:

        result = ask_farmdoc(question)

        indicator = (
            '<span class="edge-badge">● Edge</span>'
            if result.get("edge")
            else ""
        )

        return (
            result["answer"],
            format_sources(
                result.get("sources", [])
            ),
            indicator
        )

    except Exception:

        return (
            "FarmDoc could not complete your request.",
            "No supporting documents returned.",
            ""
        )


# ==========================================
# START LOCAL APPLICATION
# ==========================================


# PHASE11_EVIDENCE_QUALITY_INTEGRATION

from evidence_quality import refine_response

_original_ask_farmdoc = ask_farmdoc

def ask_farmdoc(question, force_edge=False):

    start = time.perf_counter()

    result = _original_ask_farmdoc(
        question,
        force_edge=force_edge
    )

    result = refine_response(
        str(question or ""),
        result
    )

    result["latency_seconds"] = round(
        time.perf_counter() - start,
        4
    )

    return result


if __name__ == "__main__":

    app = build_farmdoc(
        response_handler=interface_response,
        initial_edge=not remote_available()
    )

    launch_farmdoc(
        app,
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True
    )
