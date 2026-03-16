from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.claims.service import extract_claims


def test_claim_extraction_returns_supporting_quote_for_each_claim():
    document = {
        "title": "Example story",
        "body_text": "CoreWire launched a new analysis pipeline on Tuesday.",
    }

    claims = extract_claims(document)

    assert len(claims) == 1
    assert claims[0]["claim_text"] == "CoreWire launched a new analysis pipeline on Tuesday."
    assert claims[0]["supporting_quote"] == document["body_text"]
