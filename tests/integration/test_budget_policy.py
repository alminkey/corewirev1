from pathlib import Path
import sys

api_path = str(Path(__file__).resolve().parents[2] / "apps" / "api")
sys.path.insert(0, api_path)
for module_name in list(sys.modules):
    if module_name == "core" or module_name.startswith("core."):
        del sys.modules[module_name]

from core.policy.budget import select_story_profile


def test_flagship_story_can_select_premium_profile_while_standard_story_defaults_to_balanced():
    flagship_story = {
        "slug": "flagship-investigation",
        "headline": "Flagship investigation",
        "status": "draft",
        "confidence": "high",
        "source_count": 6,
        "updated_at": "2026-03-13T00:00:00Z",
        "dek": "A high-priority investigation.",
        "story_tier": "flagship",
        "requested_profile": "premium",
    }
    standard_story = {
        "slug": "daily-briefing",
        "headline": "Daily briefing",
        "status": "draft",
        "confidence": "medium",
        "source_count": 3,
        "updated_at": "2026-03-13T00:00:00Z",
        "dek": "A standard article.",
        "story_tier": "standard",
    }

    flagship_selection = select_story_profile(flagship_story)
    standard_selection = select_story_profile(standard_story)

    assert flagship_selection["profile"] == "premium"
    assert flagship_selection["estimated_cost_band"] == "$0.30-$0.70"
    assert standard_selection["profile"] == "balanced"
    assert standard_selection["estimated_cost_band"] == "$0.18-$0.45"
