from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.editorial.quality import assess_prose_quality


def test_quality_filters_block_repeated_filler_unsupported_transitions_and_thin_summary():
    low_quality_draft = {
        "narrative": (
            "In today's world, this is important. In today's world, this is important. "
            "Meanwhile, this happened. This happened."
        )
    }

    quality = assess_prose_quality(low_quality_draft)

    assert quality["valid"] is False
    assert "repeated_filler" in quality["issues"]
    assert "unsupported_transition" in quality["issues"]
    assert "thin_summary_prose" in quality["issues"]


def test_quality_filters_allow_connected_specific_prose():
    polished_draft = {
        "narrative": (
            "CoreWire launched the pipeline on Tuesday. The launch matters because "
            "it turns a staged prototype into a more usable newsroom system."
        )
    }

    quality = assess_prose_quality(polished_draft)

    assert quality["valid"] is True
    assert quality["issues"] == []
