from typing import TypedDict


COST_BANDS = {
    "economy": "$0.08-$0.22",
    "balanced": "$0.18-$0.45",
    "premium": "$0.30-$0.70",
}


class StoryProfileSelection(TypedDict):
    profile: str
    estimated_cost_band: str


def select_story_profile(story: dict) -> StoryProfileSelection:
    requested_profile = story.get("requested_profile")
    story_tier = story.get("story_tier", "standard")

    if requested_profile == "premium" and story_tier == "flagship":
        profile = "premium"
    else:
        profile = requested_profile or "balanced"
        if profile == "premium":
            profile = "balanced"

    return {
        "profile": profile,
        "estimated_cost_band": COST_BANDS[profile],
    }
