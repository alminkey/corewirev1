from typing import TypedDict


class AutonomySettings(TypedDict):
    mode: str
    allowed_modes: list[str]
    homepage_auto_publish: bool
    developing_story_auto_publish: bool
    pause_ingest: bool
    pause_publish: bool


class ProgrammingTopic(TypedDict):
    name: str
    enabled: bool


class ProgrammingInterval(TypedDict):
    label: str
    minutes: int
    enabled: bool


class ProgrammingWindow(TypedDict):
    label: str
    start_hour: int
    end_hour: int
    timezone: str
    enabled: bool


class ProgrammingSettings(TypedDict):
    topics: list[ProgrammingTopic]
    intervals: list[ProgrammingInterval]
    schedule_windows: list[ProgrammingWindow]


def get_autonomy_settings() -> AutonomySettings:
    return {
        "mode": "hybrid",
        "allowed_modes": ["manual", "hybrid", "autonomous"],
        "homepage_auto_publish": True,
        "developing_story_auto_publish": True,
        "pause_ingest": False,
        "pause_publish": False,
    }
