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
