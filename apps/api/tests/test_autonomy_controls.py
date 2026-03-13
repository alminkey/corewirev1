from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app


def test_owner_can_read_autonomy_controls():
    client = TestClient(app)

    response = client.get(
        "/api/admin/settings/autonomy",
        headers={"x-owner-token": "corewire-owner-token"},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["mode"] == "hybrid"
    assert payload["allowed_modes"] == ["manual", "hybrid", "autonomous"]
    assert payload["homepage_auto_publish"] is True
    assert payload["pause_publish"] is False
