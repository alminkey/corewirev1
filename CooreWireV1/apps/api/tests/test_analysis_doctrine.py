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
