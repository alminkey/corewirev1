from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.analysis.doctrine import validate_analysis_doctrine
from core.analysis.types import build_analysis_contract


def test_analysis_requires_thesis_why_actor_map_and_new_value():
    article = {
        "thesis": "",
        "body": "Generic summary.",
        "actor_map": [],
        "obscured_layer": [],
    }

    result = validate_analysis_doctrine(article)

    assert result["passed"] is False
    assert "missing_thesis" in result["violations"]
    assert "missing_why" in result["violations"]
    assert "missing_actor_map" in result["violations"]
    assert "missing_new_value" in result["violations"]


def test_analysis_contract_contains_full_article_and_renderable_sections():
    contract = build_analysis_contract({})

    assert set(contract.keys()) >= {
        "thesis",
        "known_facts",
        "actor_map",
        "obscured_layer",
        "next_moves",
        "unknowns",
        "full_article",
    }


def test_analysis_doctrine_passes_strong_analysis_payload():
    article = {
        "thesis": "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure.",
        "full_article": (
            "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure. "
            "Public claims obscure a deeper struggle over cost, deterrence, and bargaining leverage."
        ),
        "actor_map": [
            {"name": "Iran", "goal": "raise shipping costs", "likely_next_move": "maintain maritime pressure"},
            {"name": "United States", "goal": "force strategic concessions", "likely_next_move": "increase deterrence"},
        ],
        "obscured_layer": ["Public claims obscure a deeper struggle over cost and leverage."],
    }

    result = validate_analysis_doctrine(article)

    assert result == {"passed": True, "violations": []}


def test_analysis_flags_generic_thesis_thin_actor_map_and_generic_language():
    article = {
        "thesis": "The crisis remains complex and tensions are high.",
        "body": (
            "The situation remains tense and it remains to be seen what happens next. "
            "This article explains the issue for the reader."
        ),
        "actor_map": [{"name": "Iran"}],
        "obscured_layer": ["A thin placeholder."],
    }

    result = validate_analysis_doctrine(article)

    assert result["passed"] is False
    assert "generic_thesis" in result["violations"]
    assert "thin_actor_map" in result["violations"]
    assert "generic_analysis_language" in result["violations"]
    assert "meta_reader_language" in result["violations"]
