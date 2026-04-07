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


def test_build_research_dossier_builds_hidden_layers_from_deep_analysis_inputs():
    candidate = {
        "title": "Hormuz coalition strain",
        "summary": "Shipping disruption spreads across Gulf routes.",
        "public_narrative": "restoring free navigation",
        "real_objective": "breaking Iran's deterrence before coalition fatigue forces a narrower settlement",
        "timing_pressures": [
            "Washington is racing against fuel-price pressure and allied drift.",
        ],
        "hidden_incentives": [
            "Gulf states want shipping reopened without giving Washington a blank-check war mandate.",
        ],
        "obscured_questions": [
            "What the coalition still cannot admit publicly is how much escalation it will tolerate before reopening becomes secondary to containment.",
        ],
        "sources": [
            {
                "publisher": "AP",
                "title": "Shipping disruption spreads across Gulf routes",
                "url": "https://example.com/ap",
            },
            {
                "publisher": "Reuters",
                "title": "Allies split over burden of reopening the waterway",
                "url": "https://example.com/reuters",
            },
        ],
    }

    dossier = build_research_dossier(candidate)

    assert dossier["timing_pressures"] == [
        "Washington is racing against fuel-price pressure and allied drift.",
    ]
    assert dossier["hidden_incentives"] == [
        "Gulf states want shipping reopened without giving Washington a blank-check war mandate.",
    ]
    assert dossier["obscured_questions"] == [
        "What the coalition still cannot admit publicly is how much escalation it will tolerate before reopening becomes secondary to containment.",
    ]
    assert dossier["hidden_layers"] == [
        "The public argument centers on restoring free navigation, but the deeper objective is breaking Iran's deterrence before coalition fatigue forces a narrower settlement.",
        "Washington is racing against fuel-price pressure and allied drift.",
        "Gulf states want shipping reopened without giving Washington a blank-check war mandate.",
        "What the coalition still cannot admit publicly is how much escalation it will tolerate before reopening becomes secondary to containment.",
    ]


def test_build_research_dossier_adds_flagship_insight_signals():
    dossier = build_research_dossier(
        {
            "title": "Hormuz crisis",
            "summary": "Shipping disruption spreads across Gulf routes.",
            "public_narrative": "reopening shipping and restoring deterrence",
            "real_objective": "forcing Iran into concessions before coalition discipline frays",
            "timing_pressures": ["Washington is racing against fuel pressure."],
            "why_it_matters": "Shipping disruption is splitting the coalition.",
            "obscured_questions": [
                "Whether Washington can threaten harder without losing allied support."
            ],
            "unknowns": ["Whether the coalition can hold."],
            "sources": [
                {
                    "publisher": "AP",
                    "title": "Shipping disruption spreads across Gulf routes",
                    "url": "https://example.com/ap",
                },
                {
                    "publisher": "Reuters",
                    "title": "Allies split over burden of reopening the waterway",
                    "url": "https://example.com/reuters",
                },
            ],
        }
    )

    assert dossier["core_contradictions"] == [
        "The public case is about reopening shipping and restoring deterrence, but the deeper fight is over whether forcing Iran into concessions before coalition discipline frays can be achieved without splitting the coalition that has to bear the cost."
    ]
    assert dossier["why_now_signals"] == [
        "Washington is racing against fuel pressure."
    ]
    assert dossier["buried_consequences"] == [
        "Shipping disruption is splitting the coalition."
    ]
    assert dossier["hard_questions"] == [
        "Whether Washington can threaten harder without losing allied support.",
        "Whether the coalition can hold.",
    ]


def test_build_research_dossier_adds_lead_insight_candidates():
    dossier = build_research_dossier(
        {
            "title": "Hormuz crisis",
            "summary": "Shipping disruption spreads across Gulf routes.",
            "public_narrative": "reopening shipping and restoring deterrence",
            "real_objective": "forcing Iran into concessions before coalition discipline frays",
            "timing_pressures": ["Washington is racing against fuel pressure."],
            "hidden_incentives": [
                "Several Gulf capitals want U.S. protection without owning escalation."
            ],
            "obscured_questions": [
                "Whether Washington can threaten harder without losing allied support."
            ],
            "why_it_matters": "Shipping disruption is splitting the coalition.",
            "sources": [
                {
                    "publisher": "AP",
                    "title": "Shipping disruption spreads across Gulf routes",
                    "url": "https://example.com/ap",
                },
                {
                    "publisher": "Reuters",
                    "title": "Allies split over burden of reopening the waterway",
                    "url": "https://example.com/reuters",
                },
            ],
        }
    )

    assert dossier["lead_insight_candidates"]
    assert any(
        "public case" in candidate.lower() or "real contest" in candidate.lower()
        for candidate in dossier["lead_insight_candidates"]
    )


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
        "Hormuz crisis is escalating because the real contest is now between "
        "Iran's bid to raise shipping costs and the U.S. drive to force strategic concessions."
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
        "The crisis is escalating because the real contest is now between the U.S. drive to "
        "force strategic concessions from Iran before the costs spread further and Israel's effort "
        "to degrade Iran's regional deterrence."
    )
