from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app


def test_admin_routes_require_owner_token_and_expose_overview_for_owner():
    client = TestClient(app)

    unauthorized = client.get("/api/admin/overview")
    authorized = client.get(
        "/api/admin/overview",
        headers={"x-owner-token": "corewire-owner-token"},
    )

    assert unauthorized.status_code == 401
    assert authorized.status_code == 200
    assert authorized.json()["publish_mode"] == "hybrid"


def test_owner_can_fetch_dashboard_summary_with_health_queue_and_publish_stats():
    client = TestClient(app)

    response = client.get(
        "/api/admin/overview",
        headers={"x-owner-token": "corewire-owner-token"},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["health"]["system"] == "stable"
    assert payload["autonomy"]["mode"] == "hybrid"
    assert payload["pause_state"] == {
        "ingest": False,
        "publish": False,
    }
    assert payload["queue"]["review"] >= 0
    assert payload["published"]["total"] >= 0
    assert isinstance(payload["recent_activity"], list)
