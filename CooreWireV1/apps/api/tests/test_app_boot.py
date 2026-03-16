from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app


def test_app_exposes_health_and_article_routes():
    client = TestClient(app)

    health_response = client.get("/health")
    articles_response = client.get("/api/articles")

    assert health_response.status_code == 200
    assert health_response.json() == {"status": "ok"}
    assert articles_response.status_code == 200
