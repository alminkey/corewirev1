from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.analysis.evaluation import score_analysis_output


def test_score_analysis_output_accepts_strong_flagship_analysis():
    article = {
        "thesis": "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure.",
        "known_facts": [
            "Shipping disruption is spreading.",
            "Insurance costs are rising.",
        ],
        "claims": ["Iran says it is acting defensively"],
        "stakes": ["The conflict is changing insurance, fuel, and trade costs."],
        "actor_map": [
            {
                "name": "Iran",
                "goal": "raise shipping costs",
                "currently_benefits": ["can pressure maritime flows"],
                "currently_pressures": ["risk of escalation"],
                "likely_next_move": "maintain maritime pressure",
            },
            {
                "name": "United States",
                "goal": "force strategic concessions",
                "currently_benefits": [],
                "currently_pressures": ["regional escalation risk"],
                "likely_next_move": "increase regional deterrence",
            },
        ],
        "obscured_layer": ["Public claims obscure a deeper struggle over cost and leverage."],
        "unknowns": ["It remains unclear how long the pressure can be sustained."],
        "full_article": (
            "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure. "
            "Shipping disruption is spreading. Insurance costs are rising. "
            "Public claims obscure a deeper struggle over cost and leverage. "
            "The conflict is changing insurance, fuel, and trade costs."
        ),
    }
    doctrine = {"passed": True, "violations": []}

    evaluation = score_analysis_output(article, doctrine)

    assert evaluation["decision"] == "accept"
    assert evaluation["passed"] is True
    assert evaluation["scores"]["thesis_strength"] >= 2
    assert evaluation["scores"]["new_value"] >= 2
    assert evaluation["scores"]["actor_map_quality"] >= 2


def test_score_analysis_output_reruns_or_rejects_generic_analysis():
    article = {
        "thesis": "The crisis remains complex and tensions are high.",
        "known_facts": ["Something happened."],
        "claims": [],
        "stakes": [],
        "actor_map": [{"name": "Iran"}],
        "obscured_layer": ["Thin placeholder."],
        "unknowns": [],
        "full_article": (
            "The situation remains tense and it remains to be seen what happens next. "
            "This article explains the issue for the reader."
        ),
    }
    doctrine = {
        "passed": False,
        "violations": [
            "generic_thesis",
            "thin_actor_map",
            "generic_analysis_language",
            "meta_reader_language",
        ],
    }

    evaluation = score_analysis_output(article, doctrine)

    assert evaluation["decision"] in {"rerun", "reject"}
    assert evaluation["passed"] is False
    assert evaluation["scores"]["thesis_strength"] < 2
    assert evaluation["scores"]["actor_map_quality"] < 2
