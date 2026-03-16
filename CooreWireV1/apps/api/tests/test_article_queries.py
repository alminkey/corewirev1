from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app


def test_homepage_endpoint_returns_live_published_and_developing_sections():
    client = TestClient(app)

    response = client.get("/api/articles")

    assert response.status_code == 200

    payload = response.json()

    assert payload["lead_story"]["slug"] == "corewire-launched-the-pipeline"
    assert len(payload["top_stories"]) >= 1
    assert len(payload["developing_stories"]) >= 1


def test_article_detail_endpoint_returns_story_by_slug():
    client = TestClient(app)

    response = client.get("/api/articles/corewire-launched-the-pipeline")

    assert response.status_code == 200

    payload = response.json()

    assert payload["slug"] == "corewire-launched-the-pipeline"
    assert payload["status"] == "published"
    assert payload["source_count"] >= 2
