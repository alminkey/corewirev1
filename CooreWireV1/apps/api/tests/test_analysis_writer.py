from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.analysis.extraction import extract_analysis_sections
from core.analysis.writer import generate_flagship_analysis


def test_generate_flagship_analysis_uses_dossier_and_actor_inputs():
    thesis = "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure."

    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading.", "Insurance costs are rising."],
            "claims": ["Iran says it is acting defensively"],
            "stakes": ["The conflict is changing insurance, fuel, and trade costs."],
            "unknowns": ["It remains unclear how long the pressure can be sustained."],
            "sources": [{"publisher": "AP", "url": "https://example.com/ap"}],
        },
        [
            {"name": "Iran", "goal": "raise shipping costs", "likely_next_move": "maintain maritime pressure"},
            {"name": "United States", "goal": "force strategic concessions", "likely_next_move": "increase regional deterrence"},
        ],
        thesis,
    )

    assert article["thesis"] == thesis
    assert article["known_facts"] == [
        "Shipping disruption is spreading.",
        "Insurance costs are rising.",
    ]
    assert "Hormuz crisis" in article["full_article"]
    assert "Shipping disruption is spreading." in article["full_article"]
    assert "Iran says it is acting defensively" in article["full_article"]
    assert "raise shipping costs" in article["full_article"]
    assert "force strategic concessions" in article["full_article"]
    assert "insurance, fuel, and trade costs" in article["full_article"]
    assert "maintain maritime pressure" in article["next_moves"][0]
    assert "The strategic problem now looks different for each actor." in article["full_article"]
    assert "At its core, Hormuz crisis is no longer just about the latest exchange." in article["full_article"]
    assert "Hormuz crisis is being driven by a collision between visible events and harder strategic objectives." not in article["full_article"]
    assert len(article["full_article"]) > 1200


def test_generate_flagship_analysis_avoids_source_title_leakage_and_groups_next_moves():
    thesis = (
        "Hormuz crisis is escalating because Iran wants to raise shipping costs "
        "while United States is trying to force strategic concessions."
    )

    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": ["Trump says allies should carry more of the burden."],
            "stakes": ["The conflict is changing insurance, fuel, and trade costs."],
            "unknowns": ["It remains unclear how long the pressure can be sustained."],
            "source_signals": [
                "Bahrain waters down UN proposal over opposition to allowing force to open Strait of Hormuz"
            ],
            "sources": [{"publisher": "AP", "url": "https://example.com/ap"}],
        },
        [
            {
                "name": "United States",
                "goal": "force strategic concessions",
                "likely_next_move": "increase military and diplomatic pressure",
            },
            {
                "name": "Israel",
                "goal": "degrade Iran's deterrence",
                "likely_next_move": "increase military and diplomatic pressure",
            },
            {
                "name": "Iran",
                "goal": "raise shipping costs",
                "likely_next_move": "keep using maritime pressure to raise costs",
            },
        ],
        thesis,
    )

    assert "Bahrain waters down UN proposal" not in article["full_article"]
    assert "Public messaging is already shaping the frame of the crisis." not in article["full_article"]
    assert article["next_moves"] == [
        "United States and Israel are likely to increase military and diplomatic pressure.",
        "Iran is likely to keep using maritime pressure to raise costs.",
    ]
    assert (
        "Washington and Israel are not trying to solve the same problem, but their interests still overlap."
        in article["full_article"]
    )
    assert "\n\nIran, by contrast, is trying to raise shipping costs." in article["full_article"]
    assert "; it currently benefits from" not in article["full_article"]
    assert "Washington's next move is likely to be to increase military and diplomatic pressure." in article["full_article"]
    assert "Israel's next move is likely to be to increase military and diplomatic pressure." in article["full_article"]
    assert "That tension makes the next phase easier to sketch than to control." in article["full_article"]


def test_generate_flagship_analysis_uses_more_editorial_voice_and_closing_cadence():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": ["Iran says it is acting defensively."],
            "stakes": ["The conflict is changing insurance, fuel, and trade costs."],
            "unknowns": ["It remains unclear how long the pressure can be sustained."],
            "sources": [],
        },
        [
            {
                "name": "Iran",
                "goal": "raise shipping costs",
                "likely_next_move": "keep using maritime pressure to raise costs",
            }
        ],
        "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure.",
    )

    assert "The public case for the confrontation is straightforward." in article["full_article"]
    assert "What remains unresolved is straightforward but decisive." not in article["full_article"]
    assert "Until those questions are resolved, the crisis will keep spilling costs beyond the battlefield." in article["full_article"]


def test_generate_flagship_analysis_compresses_actor_section_into_editorial_flow():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": ["Iran says it is acting defensively."],
            "stakes": ["The conflict is changing insurance, fuel, and trade costs."],
            "unknowns": ["It remains unclear how long the pressure can be sustained."],
            "sources": [],
        },
        [
            {
                "name": "United States",
                "goal": "force strategic concessions",
                "constraints": ["fuel-price pressure"],
                "currently_benefits": ["military leverage"],
                "currently_pressures": ["allied reluctance"],
                "likely_next_move": "increase military and diplomatic pressure",
            },
            {
                "name": "Israel",
                "goal": "degrade Iran's deterrence",
                "constraints": ["dependence on U.S. backing"],
                "currently_benefits": ["a rare window for escalation"],
                "currently_pressures": ["regional escalation risk"],
                "likely_next_move": "push to extend the military phase",
            },
            {
                "name": "Iran",
                "goal": "raise shipping costs",
                "constraints": ["inferior conventional air power"],
                "currently_benefits": ["global market leverage"],
                "currently_pressures": ["long-term sanctions"],
                "likely_next_move": "keep using maritime pressure to raise costs",
            },
            {
                "name": "Bahrain and Gulf states",
                "goal": "restore shipping security",
                "constraints": ["geographic exposure"],
                "currently_benefits": ["outside military cover"],
                "currently_pressures": ["infrastructure risk"],
                "likely_next_move": "press for shipping security without a blank-check war mandate",
            },
        ],
        "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure.",
    )

    assert "Washington and Israel are not trying to solve the same problem, but their interests still overlap." in article["full_article"]
    assert "Iran, by contrast, is trying to raise shipping costs." in article["full_article"]
    assert article["full_article"].count("\n\nFor ") == 0


def test_generate_flagship_analysis_prefers_deep_hidden_layers_over_generic_obscured_line():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": ["Iran says it is acting defensively."],
            "stakes": ["The conflict is changing insurance, fuel, and trade costs."],
            "hidden_layers": [
                "The public argument centers on restoring navigation, but the deeper objective is to keep the coalition together long enough to force Iranian concessions.",
                "Washington is racing against fuel-price pressure and allied fatigue.",
                "Gulf states want shipping reopened without turning their own infrastructure into the next battlefield.",
            ],
            "unknowns": ["It remains unclear how long the pressure can be sustained."],
            "sources": [],
        },
        [
            {
                "name": "United States",
                "goal": "force strategic concessions",
                "likely_next_move": "increase military and diplomatic pressure",
            },
            {
                "name": "Israel",
                "goal": "degrade Iran's deterrence",
                "likely_next_move": "push to extend the military phase",
            },
        ],
        "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure.",
    )

    assert (
        "The public argument centers on restoring navigation, but the deeper objective is to keep the coalition together long enough to force Iranian concessions."
        in article["full_article"]
    )
    assert "Washington is racing against fuel-price pressure and allied fatigue." in article["full_article"]
    assert (
        "Gulf states want shipping reopened without turning their own infrastructure into the next battlefield."
        in article["full_article"]
    )
    assert "Behind the public language, the deeper contest is over whether" not in article["full_article"]


def test_generate_flagship_analysis_uses_composed_hidden_layer_and_next_phase_transitions():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": ["Iran says it is acting defensively."],
            "stakes": ["The conflict is changing insurance, fuel, and trade costs."],
            "hidden_layers": [
                "The public argument centers on restoring navigation, but the deeper objective is to keep the coalition together long enough to force Iranian concessions.",
                "Washington is racing against fuel-price pressure and allied fatigue.",
                "Gulf states want shipping reopened without turning their own infrastructure into the next battlefield.",
            ],
            "unknowns": ["It remains unclear how long the pressure can be sustained."],
            "sources": [],
        },
        [
            {
                "name": "United States",
                "goal": "force strategic concessions",
                "likely_next_move": "increase military and diplomatic pressure",
            },
            {
                "name": "Israel",
                "goal": "degrade Iran's deterrence",
                "likely_next_move": "push to extend the military phase",
            },
            {
                "name": "Iran",
                "goal": "raise shipping costs",
                "likely_next_move": "keep using maritime pressure to raise costs",
            },
        ],
        "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure.",
    )

    assert article["obscured_layer"][0] == "What matters more is the pressure building beneath the public case."
    assert (
        "The public argument centers on restoring navigation, but the deeper objective is to keep the coalition together long enough to force Iranian concessions. Washington is racing against fuel-price pressure and allied fatigue."
        in article["obscured_layer"][1]
    )
    assert (
        "What matters more is the pressure building beneath the public case."
        in article["full_article"]
    )
    assert "That tension makes the next phase easier to sketch than to control." in article["full_article"]
    assert "The next phase is likely to follow a few predictable tracks." not in article["full_article"]


def test_generate_flagship_analysis_expands_why_now_from_timing_pressure_signals():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": ["Iran says it is acting defensively."],
            "stakes": ["The conflict is changing insurance, fuel, and trade costs."],
            "timing_pressures": [
                "Washington is racing against fuel-price pressure and allied fatigue.",
                "Iran is trying to prove it can widen costs before any diplomatic off-ramp hardens.",
            ],
            "hidden_incentives": [
                "Neither side wants to publicly admit how much coalition discipline is shaping the battlefield."
            ],
            "unknowns": ["It remains unclear how long the pressure can be sustained."],
            "sources": [],
        },
        [
            {
                "name": "United States",
                "goal": "force strategic concessions",
                "likely_next_move": "increase military and diplomatic pressure",
            },
            {
                "name": "Iran",
                "goal": "raise shipping costs",
                "likely_next_move": "keep using maritime pressure to raise costs",
            },
        ],
        "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure.",
    )

    assert "The timing matters because the pressure is no longer moving at the same speed for every side." in article["full_article"]
    assert "Washington is racing against fuel-price pressure and allied fatigue." in article["full_article"]
    assert "Iran is trying to prove it can widen costs before any diplomatic off-ramp hardens." in article["full_article"]


def test_generate_flagship_analysis_expands_consequence_layer_beyond_generic_stakes():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": ["Iran says it is acting defensively."],
            "stakes": [
                "The conflict is changing insurance, fuel, and trade costs.",
                "The cost of reopening shipping lanes is starting to split the coalition.",
            ],
            "unknowns": ["It remains unclear how long the pressure can be sustained."],
            "sources": [],
        },
        [
            {
                "name": "United States",
                "goal": "force strategic concessions",
                "currently_pressures": ["fuel-price pressure", "allied reluctance"],
                "likely_next_move": "increase military and diplomatic pressure",
            },
            {
                "name": "Iran",
                "goal": "raise shipping costs",
                "currently_benefits": ["global market leverage"],
                "likely_next_move": "keep using maritime pressure to raise costs",
            },
        ],
        "Hormuz crisis is escalating because shipping leverage now collides with coercive pressure.",
    )

    assert "The consequences are no longer confined to the battlefield." in article["full_article"]
    assert "The conflict is changing insurance, fuel, and trade costs." in article["full_article"]
    assert "The cost of reopening shipping lanes is starting to split the coalition." in article["full_article"]
    assert "That is increasing pressure on Washington through fuel-price pressure and allied reluctance." in article["full_article"]
    assert "At the same time, it is giving Iran room to exploit global market leverage." in article["full_article"]


def test_generate_flagship_analysis_uses_plural_verbs_for_compound_actor_names():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": [],
            "stakes": [],
            "unknowns": [],
            "sources": [],
        },
        [
            {
                "name": "Bahrain and Gulf states",
                "goal": "restore shipping security",
                "likely_next_move": "press for shipping security without a blank-check war mandate",
            }
        ],
        "Hormuz crisis matters because Bahrain and Gulf states want to restore shipping security.",
    )

    assert article["next_moves"] == [
        "Bahrain and Gulf states are likely to press for shipping security without a blank-check war mandate."
    ]
    assert "Bahrain and Gulf states wants to restore shipping security" not in article["full_article"]
    assert "Bahrain and Gulf states are trying to restore shipping security." in article["full_article"]
    assert "Their next move is likely to be to press for shipping security without a blank-check war mandate." in article["full_article"]


def test_generate_flagship_analysis_uses_singular_verb_for_united_states():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": [],
            "stakes": [],
            "unknowns": [],
            "sources": [],
        },
        [
            {
                "name": "United States",
                "goal": "force strategic concessions",
                "likely_next_move": "increase military and diplomatic pressure",
            }
        ],
        "Hormuz crisis matters because United States wants to force strategic concessions.",
    )

    assert article["next_moves"] == [
        "United States is likely to increase military and diplomatic pressure."
    ]


def test_generate_flagship_analysis_uses_short_subject_when_topic_is_already_a_claim():
    article = generate_flagship_analysis(
        {
            "topic": (
                "The Hormuz war is becoming a test of who can impose global costs faster "
                "than the other side can impose surrender"
            ),
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": [],
            "stakes": [],
            "unknowns": [],
            "sources": [],
        },
        [],
        "The crisis is escalating because coercive pressure is colliding with maritime leverage.",
    )

    assert "At its core, the crisis is no longer just about the latest exchange." in article["full_article"]
    assert (
        "The Hormuz war is becoming a test of who can impose global costs faster than the other side can impose surrender is being driven"
        not in article["full_article"]
    )


def test_extract_analysis_sections_returns_renderable_blocks():
    extracted = extract_analysis_sections(
        {
            "full_article": "Paragraph 1.\n\nParagraph 2.\n\nParagraph 3.",
            "known_facts": ["Fact 1", ""],
            "stakes": ["Fuel and insurance costs are rising."],
            "obscured_layer": ["The deeper struggle is over leverage."],
            "next_moves": ["Iran is likely to maintain pressure."],
            "unknowns": ["Unknown 1", ""],
        }
    )

    assert extracted["fact_blocks"] == [{"text": "Fact 1", "citations": []}]
    assert extracted["analysis_blocks"] == [
        {"text": "Fuel and insurance costs are rising."},
        {"text": "The deeper struggle is over leverage."},
        {"text": "Iran is likely to maintain pressure."},
    ]
    assert extracted["disagreements"] == ["Unknown 1"]
