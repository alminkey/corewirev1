from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.analysis.service import analyze_story
from core.confidence.service import score_confidence


def test_analysis_separates_verified_facts_from_why_analysis():
    evidence_bundle = {
        "claims": [
            {
                "claim_text": "CoreWire launched the pipeline on Tuesday.",
                "supporting_quote": "CoreWire launched the pipeline on Tuesday.",
            }
        ],
        "evidence": [
            {
                "relation_type": "supports",
                "evidence_quote": "CoreWire launched the pipeline on Tuesday.",
            }
        ],
    }

    analysis = analyze_story(evidence_bundle)

    assert analysis["verified_facts"][0] == "CoreWire launched the pipeline on Tuesday."
    assert analysis["why_analysis"].startswith("Analysis:")


def test_low_source_diversity_reduces_confidence():
    evidence_bundle = {
        "evidence": [
            {"relation_type": "supports", "source_id": "source-1"},
            {"relation_type": "supports", "source_id": "source-1"},
        ]
    }

    confidence = score_confidence(evidence_bundle)

    assert confidence["level"] == "low"
    assert confidence["homepage_eligible"] is False
