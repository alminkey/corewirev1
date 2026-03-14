from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app


def test_owner_can_read_review_queue_sections():
    client = TestClient(app)

    response = client.get(
        "/api/admin/review-queue",
        headers={"x-owner-token": "corewire-owner-token"},
    )

    assert response.status_code == 200

    payload = response.json()

    assert len(payload["pending_drafts"]) >= 1
    assert len(payload["low_confidence"]) >= 1
    assert len(payload["flagged_items"]) >= 1
