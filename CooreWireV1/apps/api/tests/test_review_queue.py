from pathlib import Path
import sys
import uuid
import json

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app
from core.admin.review import get_review_queue
from core.db.base import Base
from core.db.models.article import ArticleDraft
from core.db.models.story import StoryAnalysis, StoryCluster
from core.db.session import build_engine, build_session_factory


def test_owner_can_read_review_queue_sections():
    client = TestClient(app)

    response = client.get(
        "/api/admin/review-queue",
        headers={"x-owner-token": "corewire-owner-token"},
    )

    assert response.status_code == 200

    payload = response.json()

    assert set(payload.keys()) == {"pending_drafts", "low_confidence", "flagged_items"}
    assert isinstance(payload["pending_drafts"], list)
    assert isinstance(payload["low_confidence"], list)
    assert isinstance(payload["flagged_items"], list)


def test_review_queue_returns_empty_sections_without_stub_when_database_is_empty(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-empty-review-queue-{uuid.uuid4().hex}.db"
    database_url = f"sqlite+pysqlite:///{database_path}"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", database_url)

    engine = build_engine(database_url)
    Base.metadata.create_all(engine)

    try:
        payload = get_review_queue()
        assert payload == {
            "pending_drafts": [],
            "low_confidence": [],
            "flagged_items": [],
        }
    finally:
        engine.dispose()
        if database_path.exists():
            database_path.unlink()


def test_owner_review_queue_reads_persisted_review_items(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-review-queue-{uuid.uuid4().hex}.db"
    database_url = f"sqlite+pysqlite:///{database_path}"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", database_url)

    engine = build_engine(database_url)
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            cluster = StoryCluster(
                id="cluster-review",
                cluster_key="cluster-review",
                topic_label="Review",
                status="active",
            )
            analysis = StoryAnalysis(
                id="analysis-review",
                story_cluster_id="cluster-review",
                verified_facts_json="[]",
                open_questions_json="[]",
                why_analysis_text="Why it matters.",
                disagreement_summary="",
                overall_confidence="medium",
                low_confidence_reasons_json=json.dumps(["medium_confidence"]),
            )
            draft = ArticleDraft(
                id="draft-review",
                story_analysis_id="analysis-review",
                headline="Persisted review draft",
                dek="Needs owner review",
                body_json="[]",
                facts_json="[]",
                analysis_json="[]",
                citations_json="[]",
                validation_status="review_required",
            )
            session.add_all([cluster, analysis, draft])
            session.commit()

        client = TestClient(app)
        response = client.get(
            "/api/admin/review-queue",
            headers={"x-owner-token": "corewire-owner-token"},
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["pending_drafts"][0]["headline"] == "Persisted review draft"
    finally:
        engine.dispose()
        if database_path.exists():
            database_path.unlink()


def test_owner_can_read_review_detail_and_submit_decision(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-review-detail-{uuid.uuid4().hex}.db"
    database_url = f"sqlite+pysqlite:///{database_path}"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", database_url)

    engine = build_engine(database_url)
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            cluster = StoryCluster(
                id="cluster-review-detail",
                cluster_key="cluster-review-detail",
                topic_label="Review Detail",
                status="active",
            )
            analysis = StoryAnalysis(
                id="analysis-review-detail",
                story_cluster_id="cluster-review-detail",
                verified_facts_json="[]",
                open_questions_json="[]",
                why_analysis_text="Why it matters.",
                disagreement_summary="",
                overall_confidence="medium",
                low_confidence_reasons_json=json.dumps(["insufficient_source_authority"]),
            )
            draft = ArticleDraft(
                id="draft-review-detail",
                story_analysis_id="analysis-review-detail",
                headline="Persisted review detail draft",
                dek="Needs owner review before publish",
                body_json=json.dumps(
                    {
                        "headline": "Persisted review detail draft",
                        "dek": "Needs owner review before publish",
                        "narrative": "Narrative text.",
                        "fact_blocks": [{"text": "Fact block"}],
                        "analysis_blocks": [{"text": "Analysis block"}],
                        "sources": [
                            {
                                "label": "Reuters",
                                "publisher": "Reuters",
                                "title": "Enterprise AI report",
                                "url": "https://example.com/reuters",
                                "role": "article",
                            }
                        ],
                        "editorial_flags": [
                            {"severity": "medium", "message": "Needs authority review"}
                        ],
                    }
                ),
                facts_json=json.dumps([{"text": "Fact block"}]),
                analysis_json=json.dumps([{"text": "Analysis block"}]),
                citations_json=json.dumps(["insufficient_source_authority"]),
                validation_status="review_required",
            )
            session.add_all([cluster, analysis, draft])
            session.commit()

        client = TestClient(app)

        detail_response = client.get(
            "/api/admin/review-queue/draft-review-detail",
            headers={"x-owner-token": "corewire-owner-token"},
        )

        assert detail_response.status_code == 200
        detail_payload = detail_response.json()
        assert detail_payload["id"] == "draft-review-detail"
        assert detail_payload["headline"] == "Persisted review detail draft"
        assert detail_payload["reasons"] == ["insufficient_source_authority"]
        assert detail_payload["draft"]["narrative"] == "Narrative text."
        assert detail_payload["draft"]["sources"][0]["publisher"] == "Reuters"

        decision_response = client.post(
            "/api/admin/review-queue/draft-review-detail/decision",
            headers={"x-owner-token": "corewire-owner-token"},
            json={"action": "request_rerun"},
        )

        assert decision_response.status_code == 200
        decision_payload = decision_response.json()
        assert decision_payload["id"] == "draft-review-detail"
        assert decision_payload["status"] == "rerun_requested"

        queue_response = client.get(
            "/api/admin/review-queue",
            headers={"x-owner-token": "corewire-owner-token"},
        )
        assert queue_response.status_code == 200
        queue_payload = queue_response.json()
        assert queue_payload["pending_drafts"] == []
    finally:
        engine.dispose()
        if database_path.exists():
            database_path.unlink()


def test_review_detail_normalizes_legacy_reason_and_source_payloads(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-review-legacy-{uuid.uuid4().hex}.db"
    database_url = f"sqlite+pysqlite:///{database_path}"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", database_url)

    engine = build_engine(database_url)
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            cluster = StoryCluster(
                id="cluster-review-legacy",
                cluster_key="cluster-review-legacy",
                topic_label="Legacy Review Detail",
                status="active",
            )
            analysis = StoryAnalysis(
                id="analysis-review-legacy",
                story_cluster_id="cluster-review-legacy",
                verified_facts_json="[]",
                open_questions_json="[]",
                why_analysis_text="Why it matters.",
                disagreement_summary="",
                overall_confidence="low",
                low_confidence_reasons_json=json.dumps(["insufficient_source_authority"]),
            )
            draft = ArticleDraft(
                id="draft-review-legacy",
                story_analysis_id="analysis-review-legacy",
                headline="Legacy review draft",
                dek="Still needs review",
                body_json=json.dumps(
                    {
                        "headline": "Legacy review draft",
                        "dek": "Still needs review",
                        "narrative": "",
                    }
                ),
                facts_json=json.dumps(
                    [{"text": "Only one source currently backs the rollout details."}]
                ),
                analysis_json=json.dumps(
                    ["The developing label protects the homepage until independent corroboration arrives."]
                ),
                citations_json=json.dumps(
                    [
                        {
                            "label": "Source 3",
                            "publisher": "Ops Monitor",
                            "title": "Rollout verification note",
                            "url": "https://example.com/verify-1",
                            "role": "reference",
                        }
                    ]
                ),
                validation_status="review_required",
            )
            session.add_all([cluster, analysis, draft])
            session.commit()

        client = TestClient(app)
        response = client.get(
            "/api/admin/review-queue/draft-review-legacy",
            headers={"x-owner-token": "corewire-owner-token"},
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["reasons"] == ["insufficient_source_authority"]
        assert payload["draft"]["sources"][0]["publisher"] == "Ops Monitor"
        assert payload["draft"]["analysis"] == [
            {
                "text": "The developing label protects the homepage until independent corroboration arrives."
            }
        ]
    finally:
        engine.dispose()
        if database_path.exists():
            database_path.unlink()
