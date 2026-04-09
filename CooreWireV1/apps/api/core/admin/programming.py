from copy import deepcopy

from core.admin.settings import ProgrammingSettings


_PROGRAMMING_SETTINGS: ProgrammingSettings = {
    "topics": [
        {"name": "ai", "enabled": True},
        {"name": "business", "enabled": True},
    ],
    "intervals": [
        {"label": "daily-cycle", "minutes": 360, "enabled": True},
    ],
    "schedule_windows": [
        {
            "label": "default-daytime",
            "start_hour": 6,
            "end_hour": 22,
            "timezone": "Europe/Zagreb",
            "enabled": True,
        }
    ],
}


def get_programming_settings() -> ProgrammingSettings:
    return deepcopy(_PROGRAMMING_SETTINGS)


def update_programming_settings(payload: dict) -> ProgrammingSettings:
    global _PROGRAMMING_SETTINGS

    _PROGRAMMING_SETTINGS = {
        "topics": list(payload.get("topics", _PROGRAMMING_SETTINGS["topics"])),
        "intervals": list(payload.get("intervals", _PROGRAMMING_SETTINGS["intervals"])),
        "schedule_windows": list(
            payload.get("schedule_windows", _PROGRAMMING_SETTINGS["schedule_windows"])
        ),
    }
    return get_programming_settings()
