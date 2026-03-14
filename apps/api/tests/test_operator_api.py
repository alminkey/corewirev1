from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app


def test_internal_operator_endpoint_accepts_supported_commands():
    client = TestClient(app)

    response = client.post(
        "/api/operator/commands",
        headers={"x-internal-token": "corewire-internal-token"},
        json={
            "commands": [
                {"type": "create_story", "payload": {"topic": "AI regulation"}},
                {"type": "rerun_analysis", "payload": {"story_id": "story-1"}},
                {"type": "publish_draft", "payload": {"draft_id": "draft-1"}},
                {"type": "set_autonomy_mode", "payload": {"mode": "hybrid"}},
                {"type": "disable_source", "payload": {"source": "Example Source"}},
            ]
        },
    )

    assert response.status_code == 200

    payload = response.json()
    assert len(payload["results"]) == 5
    assert payload["results"][0]["accepted"] is True
    assert payload["results"][3]["type"] == "set_autonomy_mode"
