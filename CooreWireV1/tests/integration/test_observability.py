from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2] / "apps" / "api"))

from app import app


def test_api_exposes_readiness_and_metrics_endpoints():
    client = TestClient(app)

    ready_response = client.get("/ready")
    metrics_response = client.get("/metrics")

    assert ready_response.status_code == 200
    assert ready_response.json() == {"status": "ready"}
    assert metrics_response.status_code == 200
    assert "corewire_http_requests_total" in metrics_response.text
