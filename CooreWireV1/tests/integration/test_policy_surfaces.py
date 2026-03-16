from pathlib import Path
import sys

from fastapi.testclient import TestClient

api_path = str(Path(__file__).resolve().parents[2] / "apps" / "api")
sys.path.insert(0, api_path)

from app import app


def test_public_policy_pages_and_compliance_metadata_surface_exist():
    disclosure_page = (
        Path(__file__).resolve().parents[2]
        / "apps"
        / "web"
        / "app"
        / "policies"
        / "ai-disclosure"
        / "page.tsx"
    )
    corrections_page = (
        Path(__file__).resolve().parents[2]
        / "apps"
        / "web"
        / "app"
        / "policies"
        / "corrections"
        / "page.tsx"
    )

    assert disclosure_page.exists()
    assert corrections_page.exists()

    client = TestClient(app)
    response = client.get("/api/compliance/policies")

    assert response.status_code == 200

    payload = response.json()
    assert payload["ai_disclosure"]["slug"] == "ai-disclosure"
    assert payload["corrections"]["slug"] == "corrections"
