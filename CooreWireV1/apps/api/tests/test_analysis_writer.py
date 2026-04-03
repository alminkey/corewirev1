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
