from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.drafting.service import build_draft
from core.editorial.standards import validate_standards
from core.editorial.structure import build_structure
from core.editorial.style import polish_draft


def test_editorial_pipeline_splits_structure_style_and_standards_validation():
    analysis = {
        "verified_facts": ["CoreWire launched the pipeline on Tuesday."],
        "why_analysis": (
            "Analysis: The launch matters because it moves CoreWire closer to a "
            "usable autonomous newsroom product."
        ),
    }

    structure = build_structure(analysis)
    draft = build_draft(analysis)
    polished = polish_draft(draft)
    validation = validate_standards(polished)

    assert structure["sections"][0]["label"] == "What Happened"
    assert structure["sections"][1]["label"] == "Why It Matters"
    assert polished["narrative"].startswith("CoreWire launched the pipeline on Tuesday.")
    assert "usable autonomous newsroom product" in polished["narrative"]
    assert validation["valid"] is True
    assert validation["issues"] == []
