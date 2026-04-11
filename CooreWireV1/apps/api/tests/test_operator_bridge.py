from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app


def test_internal_bridge_can_read_corewire_status_summary():
    client = TestClient(app)

    response = client.get(
        "/api/operator/bridge/status",
        headers={"x-internal-token": "corewire-internal-token"},
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["type"] == "status_summary"
    assert "health" in payload
    assert payload["health"]["system"] == "stable"
    assert "autonomy" in payload
    assert payload["autonomy"]["mode"] in {"manual", "hybrid", "autonomous"}
    assert "pause_state" in payload
    assert "ingest" in payload["pause_state"]
    assert "publish" in payload["pause_state"]
    assert "queue" in payload
    assert "review" in payload["queue"]
    assert "published" in payload
    assert "total" in payload["published"]


def test_internal_bridge_can_read_review_queue_summary():
    client = TestClient(app)

    response = client.get(
        "/api/operator/bridge/review-queue",
        headers={"x-internal-token": "corewire-internal-token"},
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["type"] == "review_queue_summary"
    assert "totals" in payload
    assert "pending_drafts" in payload["totals"]
    assert "low_confidence" in payload["totals"]
    assert "flagged_items" in payload["totals"]
    assert "items" in payload
    assert isinstance(payload["items"]["pending_drafts"], list)
    assert isinstance(payload["items"]["low_confidence"], list)
    assert isinstance(payload["items"]["flagged_items"], list)


def test_internal_bridge_can_read_published_summary():
    client = TestClient(app)

    response = client.get(
        "/api/operator/bridge/published",
        headers={"x-internal-token": "corewire-internal-token"},
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["type"] == "published_summary"
    assert "total" in payload
    assert isinstance(payload["total"], int)
    assert "recent" in payload
    assert isinstance(payload["recent"], list)
    # Each recent item should expose slug and headline at minimum
    for item in payload["recent"]:
        assert "slug" in item
        assert "headline" in item


def test_internal_bridge_can_read_autonomy_state():
    client = TestClient(app)

    response = client.get(
        "/api/operator/bridge/autonomy",
        headers={"x-internal-token": "corewire-internal-token"},
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["type"] == "autonomy_state"
    assert payload["mode"] in {"manual", "hybrid", "autonomous"}
    assert "allowed_modes" in payload
    assert payload["allowed_modes"] == ["manual", "hybrid", "autonomous"]
    assert "homepage_auto_publish" in payload
    assert "developing_story_auto_publish" in payload
    assert "pause_ingest" in payload
    assert "pause_publish" in payload


def test_internal_bridge_read_endpoints_require_internal_token():
    client = TestClient(app)

    endpoints = [
        "/api/operator/bridge/status",
        "/api/operator/bridge/review-queue",
        "/api/operator/bridge/published",
        "/api/operator/bridge/autonomy",
    ]

    for endpoint in endpoints:
        # No token at all
        no_token_response = client.get(endpoint)
        assert no_token_response.status_code == 401, (
            f"Expected 401 without token on {endpoint}, got {no_token_response.status_code}"
        )

        # Wrong token
        wrong_token_response = client.get(
            endpoint,
            headers={"x-internal-token": "not-the-right-token"},
        )
        assert wrong_token_response.status_code == 401, (
            f"Expected 401 with wrong token on {endpoint}, got {wrong_token_response.status_code}"
        )
