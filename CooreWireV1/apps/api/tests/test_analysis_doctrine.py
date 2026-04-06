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
            "What matters more than the public case is the contradiction underneath it. "
            "The public case is about reopening shipping and restoring deterrence, but the deeper fight is over whether coalition governments can keep maritime pressure high without breaking their own political tolerance for an energy shock. "
            "The timing is not incidental. Washington is racing against fuel pressure and allied drift. "
            "The buried consequence is easier to miss than the headline event. The first real fracture may appear inside the coalition, not at sea. "
            "Washington is trying to preserve coercive leverage while Gulf partners narrow the mandate and hedge against infrastructure risk. "
            "Iran is trying to make shipping and insurance costs rise faster than its adversaries can turn military pressure into surrender. "
            "That is why the conflict now matters beyond the battlefield and why the next phase is likely to be shaped by maritime pressure, coalition drift, and energy-market nerves. "
            "The hardest pressure point is now becoming unavoidable. Until that pressure breaks one side's strategy, the conflict will keep widening the costs it is supposed to contain. "
        )
        * 3,
        "actor_map": [
            {"name": "Iran", "goal": "raise shipping costs", "likely_next_move": "maintain maritime pressure"},
            {"name": "United States", "goal": "force strategic concessions", "likely_next_move": "increase deterrence"},
        ],
        "obscured_layer": [
            "What matters more is whether coalition governments can keep maritime pressure high without breaking their own political tolerance for an energy shock.",
            "Washington is trying to preserve coercive leverage while Gulf partners narrow the mandate and hedge against infrastructure risk.",
        ],
        "stakes": [
            "The conflict is reshaping energy and insurance costs.",
        ],
        "next_moves": [
            "Iran is likely to maintain maritime pressure.",
            "United States is likely to increase deterrence.",
        ],
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


def test_analysis_flags_shallow_flagship_depth():
    article = {
        "thesis": "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure.",
        "full_article": (
            "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure. "
            "One paragraph of summary follows."
        ),
        "actor_map": [
            {"name": "Iran", "goal": "raise shipping costs", "likely_next_move": "maintain maritime pressure"},
            {"name": "United States", "goal": "force strategic concessions", "likely_next_move": "increase deterrence"},
        ],
        "obscured_layer": ["A single thin hidden-layer sentence."],
        "next_moves": ["Iran is likely to maintain maritime pressure."],
        "stakes": [],
    }

    result = validate_analysis_doctrine(article)

    assert result["passed"] is False
    assert "thin_full_article" in result["violations"]
    assert "thin_hidden_layer" in result["violations"]
    assert "thin_consequence_layer" in result["violations"]


def test_analysis_flags_missing_flagship_insight_layers():
    article = {
        "thesis": "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure.",
        "full_article": (
            "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure. "
            "The public case for the confrontation is straightforward. "
            "The strategic problem now looks different for each actor. "
            "The consequences are no longer confined to the battlefield. "
            "That tension makes the next phase easier to sketch than to control. "
        )
        * 10,
        "actor_map": [
            {"name": "Iran", "goal": "raise shipping costs", "likely_next_move": "maintain maritime pressure"},
            {"name": "United States", "goal": "force strategic concessions", "likely_next_move": "increase deterrence"},
        ],
        "obscured_layer": [
            "What matters more is the pressure building beneath the public case.",
            "A generic hidden layer sentence that does not reveal a contradiction.",
        ],
        "stakes": ["Costs are rising."],
        "next_moves": ["Iran is likely to maintain maritime pressure."],
        "unknowns": ["It remains unclear what happens next."],
    }

    result = validate_analysis_doctrine(article)

    assert result["passed"] is False
    assert "weak_core_contradiction" in result["violations"]
    assert "weak_why_now" in result["violations"]
    assert "weak_buried_consequence" in result["violations"]
    assert "weak_hard_ending" in result["violations"]
