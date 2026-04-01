from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.analysis.extraction import extract_analysis_sections
from core.analysis.writer import generate_flagship_analysis


def test_generate_flagship_analysis_returns_full_article_before_blocks():
    thesis = "A thesis"

    article = generate_flagship_analysis(
        {"verified_facts": ["Fact"]},
        [{"name": "Iran"}],
        thesis,
    )

    assert article["thesis"] == thesis
    assert len(article["full_article"]) > 1200


def test_extract_analysis_sections_returns_renderable_blocks():
    extracted = extract_analysis_sections(
        {
            "full_article": "Long article body",
            "known_facts": ["Fact 1"],
            "next_moves": ["Move 1"],
            "unknowns": ["Unknown 1"],
        }
    )

    assert "fact_blocks" in extracted
    assert "analysis_blocks" in extracted
    assert "disagreements" in extracted
