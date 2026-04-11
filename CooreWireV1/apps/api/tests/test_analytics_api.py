from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app


def test_owner_can_read_product_and_operational_analytics_summaries():
    client = TestClient(app)

    response = client.get(
        "/api/admin/analytics",
        headers={"x-owner-token": "corewire-owner-token"},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["page_metrics"]["homepage_views"] >= 1
    assert payload["queue_metrics"]["pending_jobs"] >= 0
    assert payload["cost_metrics"]["monthly_budget_used_usd"] >= 0
    assert len(payload["source_health"]) >= 1


def test_owner_can_read_dashboard_summary_and_analytics_without_contract_conflict():
    client = TestClient(app)

    overview = client.get(
        "/api/admin/overview",
        headers={"x-owner-token": "corewire-owner-token"},
    )
    analytics = client.get(
        "/api/admin/analytics",
        headers={"x-owner-token": "corewire-owner-token"},
    )

    assert overview.status_code == 200
    assert analytics.status_code == 200
    assert overview.json()["published"]["total"] >= 0
    assert analytics.json()["page_metrics"]["homepage_views"] >= 1
