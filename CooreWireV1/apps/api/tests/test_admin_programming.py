from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app


def test_owner_can_configure_topic_targets_and_generation_intervals():
    client = TestClient(app)
    headers = {"x-owner-token": "corewire-owner-token"}

    initial_response = client.get("/api/admin/settings/programming", headers=headers)

    assert initial_response.status_code == 200
    initial_payload = initial_response.json()
    assert isinstance(initial_payload["topics"], list)
    assert isinstance(initial_payload["intervals"], list)
    assert isinstance(initial_payload["schedule_windows"], list)

    update_response = client.put(
        "/api/admin/settings/programming",
        headers=headers,
        json={
            "topics": [
                {"name": "geopolitics", "enabled": True},
                {"name": "energy", "enabled": False},
            ],
            "intervals": [
                {"label": "flagship-cycle", "minutes": 720, "enabled": True}
            ],
            "schedule_windows": [
                {
                    "label": "eu-morning",
                    "start_hour": 6,
                    "end_hour": 11,
                    "timezone": "Europe/Zagreb",
                    "enabled": True,
                }
            ],
        },
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["topics"][0]["name"] == "geopolitics"
    assert updated["intervals"][0]["minutes"] == 720
    assert updated["schedule_windows"][0]["timezone"] == "Europe/Zagreb"

    persisted_response = client.get("/api/admin/settings/programming", headers=headers)
    assert persisted_response.status_code == 200
    persisted = persisted_response.json()
    assert persisted["topics"][1]["enabled"] is False
