from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.corroboration.service import match_evidence


def test_claim_gets_support_and_contradiction_links():
    claim = {"claim_text": "CoreWire launched the pipeline on Tuesday."}
    related_documents = [
        {"body_text": "CoreWire launched the pipeline on Tuesday."},
        {"body_text": "CoreWire did not launch the pipeline on Tuesday."},
    ]

    evidence = match_evidence(claim, related_documents)

    relations = {item["relation_type"] for item in evidence}
    assert "supports" in relations
    assert "contradicts" in relations
