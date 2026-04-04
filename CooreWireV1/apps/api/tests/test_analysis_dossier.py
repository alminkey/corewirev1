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


def test_build_research_dossier_uses_source_titles_as_signals_and_stakes_context():
    candidate = {
        "title": "Hormuz shipping crisis deepens",
        "summary": "Oil shipping disruption spreads across Gulf routes.",
        "why_it_matters": "The conflict is changing insurance, fuel, and trade costs.",
        "sources": [
            {
                "publisher": "AP",
                "title": "Insurance costs rise as Gulf routes remain exposed",
                "url": "https://example.com/ap",
            },
            {
                "publisher": "Reuters",
                "title": "Iran says maritime pressure will continue until strikes stop",
                "url": "https://example.com/reuters",
            },
        ],
    }

    dossier = build_research_dossier(candidate)

    assert dossier["verified_facts"] == [
        "Oil shipping disruption spreads across Gulf routes.",
    ]
    assert dossier["claims"] == []
    assert dossier["source_signals"] == [
        "Insurance costs rise as Gulf routes remain exposed",
        "Iran says maritime pressure will continue until strikes stop",
    ]
    assert dossier["stakes"] == [
        "The conflict is changing insurance, fuel, and trade costs.",
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
    assert actor_map[0]["likely_next_move"] != actor_map[1]["likely_next_move"]


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


def test_form_analysis_thesis_uses_actor_names_for_more_natural_flagship_claim():
    thesis = form_analysis_thesis(
        {"topic": "Hormuz crisis"},
        [
            {"name": "Iran", "goal": "raise shipping costs"},
            {"name": "United States", "goal": "force strategic concessions"},
        ],
    )

    assert thesis == (
        "Hormuz crisis is escalating because Iran wants to raise shipping costs "
        "while United States is trying to force strategic concessions."
    )


def test_form_analysis_thesis_avoids_repeating_topic_when_title_is_already_a_claim():
    thesis = form_analysis_thesis(
        {
            "topic": (
                "The Hormuz war is becoming a test of who can impose global costs faster "
                "than the other side can impose surrender"
            )
        },
        [
            {
                "name": "United States",
                "goal": "force strategic concessions from Iran before the costs spread further",
            },
            {
                "name": "Israel",
                "goal": "degrade Iran's regional deterrence",
            },
        ],
    )

    assert thesis == (
        "The crisis is escalating because United States wants to force strategic concessions "
        "from Iran before the costs spread further while Israel is trying to degrade Iran's regional deterrence."
    )
