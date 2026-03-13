from typing import TypedDict


class AutonomySettings(TypedDict):
    mode: str
    allowed_modes: list[str]
    homepage_auto_publish: bool
    developing_story_auto_publish: bool
    pause_ingest: bool
    pause_publish: bool


def get_autonomy_settings() -> AutonomySettings:
    return {
        "mode": "hybrid",
        "allowed_modes": ["manual", "hybrid", "autonomous"],
        "homepage_auto_publish": True,
        "developing_story_auto_publish": True,
        "pause_ingest": False,
        "pause_publish": False,
    }
