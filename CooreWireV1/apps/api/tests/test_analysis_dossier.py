from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.analysis.actors import build_actor_map
from core.analysis.dossier import build_research_dossier
from core.analysis.thesis import form_analysis_thesis


def test_build_research_dossier_separates_facts_claims_and_unknowns():
    candidate = {
        "title": "Hormuz tensions rise",
        "summary": "Shipping disruption spreads.",
        "sources": [
            {
                "publisher": "AP",
                "title": "Shipping hit",
                "url": "https://example.com",
            }
        ],
        "claims": [
            "Iran says it is acting defensively",
            {"text": "Washington says the pressure is working"},
        ],
        "unknowns": ["It is still unclear how long shipping disruptions can be sustained."],
    }

    dossier = build_research_dossier(candidate)

    assert dossier["topic"] == "Hormuz tensions rise"
    assert dossier["verified_facts"] == ["Shipping disruption spreads."]
    assert dossier["claims"] == [
        "Iran says it is acting defensively",
        "Washington says the pressure is working",
    ]
    assert dossier["unknowns"] == [
        "It is still unclear how long shipping disruptions can be sustained.",
        "Independent corroboration remains limited.",
    ]


def test_build_actor_map_tracks_goals_constraints_current_position_and_next_moves():
    actor_map = build_actor_map(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption spreads."],
            "unknowns": ["How long pressure can be sustained remains unclear."],
        },
        [
            {
                "name": "Iran",
                "goal": "raise shipping costs",
                "constraints": ["sanctions pressure"],
                "current_advantages": ["can pressure maritime flows"],
                "current_pressures": ["risk of escalation"],
            },
            {
                "name": "United States",
                "goal": "force strategic concessions",
            },
        ],
    )

    assert actor_map[0]["goal"] == "raise shipping costs"
    assert "constraints" in actor_map[0]
    assert actor_map[0]["currently_benefits"] == ["can pressure maritime flows"]
    assert actor_map[0]["currently_pressures"] == ["risk of escalation"]
    assert "likely_next_move" in actor_map[0]
    assert actor_map[0]["likely_next_move"]
    assert actor_map[1]["currently_benefits"] == []
    assert actor_map[1]["currently_pressures"] == []
    assert actor_map[1]["likely_next_move"]


def test_form_analysis_thesis_returns_causal_claim():
    thesis = form_analysis_thesis(
        {"topic": "Hormuz crisis"},
        [
            {"name": "Iran", "goal": "raise shipping costs"},
            {"name": "United States", "goal": "force strategic concessions"},
        ],
    )

    assert "because" in thesis.lower()
    assert "hormuz" in thesis.lower()
    assert "shipping costs" in thesis.lower() or "strategic concessions" in thesis.lower()


def test_form_analysis_thesis_changes_with_topic_and_actor_goals():
    first = form_analysis_thesis(
        {"topic": "Hormuz crisis"},
        [{"name": "Iran", "goal": "raise shipping costs"}],
    )
    second = form_analysis_thesis(
        {"topic": "Chip sanctions"},
        [{"name": "United States", "goal": "slow Chinese AI capacity"}],
    )

    assert first != second
    assert "hormuz" in first.lower()
    assert "chip" in second.lower() or "chinese ai capacity" in second.lower()
