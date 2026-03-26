from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app


def test_newsletter_subscribe_endpoint_accepts_email_and_source():
    client = TestClient(app)

    response = client.post(
        "/api/newsletter/subscribe",
        json={
            "email": "reader@example.com",
            "source": "article_inline_cta",
            "topic_preferences": ["ai", "business"],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["accepted"] is True
    assert payload["provider"] == "beehiiv"
    assert payload["list_id"] == "corewire-main"
