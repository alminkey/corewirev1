from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app
from core.operator import router as operator_router_module


def test_internal_operator_endpoint_accepts_supported_commands():
    client = TestClient(app)

    response = client.post(
        "/api/operator/commands",
        headers={"x-internal-token": "corewire-internal-token"},
        json={
            "commands": [
                {"type": "create_story", "payload": {"topic": "AI regulation"}},
                {"type": "rerun_analysis", "payload": {"story_id": "story-1"}},
                {"type": "publish_draft", "payload": {"draft_id": "draft-1"}},
                {"type": "set_autonomy_mode", "payload": {"mode": "hybrid"}},
                {"type": "disable_source", "payload": {"source": "Example Source"}},
            ]
        },
    )

    assert response.status_code == 200

    payload = response.json()
    assert len(payload["results"]) == 5
    assert payload["results"][0]["accepted"] is True
    assert payload["results"][3]["type"] == "set_autonomy_mode"


def test_internal_operator_endpoint_runs_pilot_story_commands(monkeypatch):
    def fake_execute_operator_command(command: dict) -> dict:
        if command["type"] == "discover_trending_story":
            return {
                "type": "discover_trending_story",
                "accepted": True,
                "profile": "balanced",
                "router": "openrouter",
                "shortlist": [
                    {
                        "title": "OpenAI updates enterprise coding workflow",
                        "summary": "Vendors are tightening agentic coding loops.",
                        "why_it_matters": "This shows where enterprise AI tooling is moving.",
                        "source_count": 3,
                        "confidence": "high",
                        "sources": [
                            {"publisher": "Reuters", "url": "https://example.com/reuters"},
                            {"publisher": "The Verge", "url": "https://example.com/verge"},
                            {"publisher": "TechCrunch", "url": "https://example.com/tc"},
                        ],
                    }
                ],
            }
        if command["type"] == "build_story_draft":
            return {
                "type": "build_story_draft",
                "accepted": True,
                "profile": "balanced",
                "router": "openrouter",
                "draft": {
                    "headline": "AI tooling vendors tighten enterprise coding loop",
                    "dek": "A fuller report built from corroborated sources.",
                    "fact_blocks": [{"text": "Vendors shipped new enterprise workflow updates."}],
                    "analysis_blocks": [{"text": "The move suggests platform consolidation."}],
                },
            }
        return {
            "type": command.get("type"),
            "accepted": True,
            "payload": command.get("payload", {}),
        }

    monkeypatch.setattr(
        operator_router_module, "execute_operator_command", fake_execute_operator_command
    )

    client = TestClient(app)

    response = client.post(
        "/api/operator/commands",
        headers={"x-internal-token": "corewire-internal-token"},
        json={
            "commands": [
                {
                    "type": "discover_trending_story",
                    "payload": {"domain": "ai-tech-business", "count": 3},
                },
                {
                    "type": "build_story_draft",
                    "payload": {
                        "candidate": {
                            "title": "OpenAI updates enterprise coding workflow",
                            "sources": [
                                {"publisher": "Reuters", "url": "https://example.com/reuters"}
                            ],
                        },
                        "length": "full_report",
                    },
                },
            ]
        },
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["results"][0]["router"] == "openrouter"
    assert payload["results"][0]["profile"] == "balanced"
    assert payload["results"][0]["shortlist"][0]["source_count"] == 3
    assert payload["results"][1]["draft"]["headline"] == (
        "AI tooling vendors tighten enterprise coding loop"
    )


def test_internal_operator_endpoint_supports_publish_and_archive_commands(monkeypatch):
    def fake_execute_operator_command(command: dict) -> dict:
        return {
            "type": command.get("type"),
            "accepted": True,
            "article": {
                "slug": "preview-story",
                "status": "published" if command.get("type") != "archive_preview_article" else "superseded",
                "homepage_eligible": command.get("type") != "archive_preview_article",
            },
            "correlation": {
                "ticket_id": command.get("ticket_id"),
                "actor_id": command.get("actor_id"),
                "correlation_id": command.get("correlation_id"),
            },
        }

    monkeypatch.setattr(
        operator_router_module, "execute_operator_command", fake_execute_operator_command
    )

    client = TestClient(app)
    response = client.post(
        "/api/operator/commands",
        headers={"x-internal-token": "corewire-internal-token"},
        json={
            "commands": [
                {
                    "type": "publish_preview_article",
                    "ticket_id": "ticket-1",
                    "actor_id": "owner-1",
                    "correlation_id": "corr-1",
                    "payload": {"draft": {"headline": "Preview story"}},
                },
                {
                    "type": "archive_preview_article",
                    "ticket_id": "ticket-1",
                    "actor_id": "owner-1",
                    "correlation_id": "corr-2",
                    "payload": {"slug": "preview-story"},
                },
            ]
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["results"][0]["article"]["status"] == "published"
    assert payload["results"][0]["correlation"]["ticket_id"] == "ticket-1"
    assert payload["results"][1]["article"]["status"] == "superseded"


def test_internal_operator_endpoint_supports_publish_policy_command(monkeypatch):
    def fake_execute_operator_command(command: dict) -> dict:
        return {
            "type": command.get("type"),
            "accepted": True,
            "decision": {"action": "review_required", "reasons": ["medium_confidence"]},
            "review_item": {"queue": "pending_drafts", "headline": "Needs review"},
        }

    monkeypatch.setattr(
        operator_router_module, "execute_operator_command", fake_execute_operator_command
    )

    client = TestClient(app)
    response = client.post(
        "/api/operator/commands",
        headers={"x-internal-token": "corewire-internal-token"},
        json={
            "commands": [
                {
                    "type": "publish_if_eligible",
                    "payload": {"draft": {"headline": "Needs review"}},
                }
            ]
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["results"][0]["decision"]["action"] == "review_required"
    assert payload["results"][0]["review_item"]["queue"] == "pending_drafts"


def test_internal_operator_endpoint_supports_composite_content_pipeline(monkeypatch):
    def fake_execute_operator_command(command: dict) -> dict:
        return {
            "type": command.get("type"),
            "accepted": True,
            "selected_candidate": {"title": "Composite candidate"},
            "draft": {"headline": "Composite draft"},
            "decision": {"action": "auto_publish", "reasons": []},
            "article": {"slug": "composite-story", "status": "published"},
        }

    monkeypatch.setattr(
        operator_router_module, "execute_operator_command", fake_execute_operator_command
    )

    client = TestClient(app)
    response = client.post(
        "/api/operator/commands",
        headers={"x-internal-token": "corewire-internal-token"},
        json={
            "commands": [
                {
                    "type": "run_content_pipeline",
                    "payload": {"domain": "ai-tech-business", "count": 3},
                }
            ]
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["results"][0]["selected_candidate"]["title"] == "Composite candidate"
    assert payload["results"][0]["decision"]["action"] == "auto_publish"
