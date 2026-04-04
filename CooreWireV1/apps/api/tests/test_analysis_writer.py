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

    assert "The crisis is being driven by a collision between visible events and harder strategic objectives." in article["full_article"]
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
