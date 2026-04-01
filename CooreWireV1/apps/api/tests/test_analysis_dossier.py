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
        "claims": ["Iran says it is acting defensively"],
    }

    dossier = build_research_dossier(candidate)

    assert "verified_facts" in dossier
    assert "claims" in dossier
    assert "unknowns" in dossier


def test_build_actor_map_tracks_goals_constraints_and_next_moves():
    actor_map = build_actor_map(
        {},
        [{"name": "Iran", "goal": "raise cost"}],
    )

    assert actor_map[0]["goal"] == "raise cost"
    assert "constraints" in actor_map[0]
    assert "likely_next_move" in actor_map[0]


def test_form_analysis_thesis_returns_causal_claim():
    thesis = form_analysis_thesis(
        {"topic": "War"},
        [{"name": "US", "goal": "pressure Iran"}],
    )

    assert thesis
