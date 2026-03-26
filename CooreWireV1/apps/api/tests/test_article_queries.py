from pathlib import Path
import sys
import json
import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app
from core.articles.service import get_article_by_slug, list_articles
from core.db.base import Base
from core.db.models.article import ArticleDraft, ArticleStatus, PublishedArticle
from core.db.models.story import StoryAnalysis, StoryCluster
from core.db.session import build_engine, build_session_factory


def _seed_articles(database_url: str) -> None:
    engine = build_engine(database_url)
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)

    with session_factory() as session:
        cluster = StoryCluster(
            id="cluster-1",
            cluster_key="cluster-1",
            topic_label="CoreWire",
            status="active",
        )
        analysis = StoryAnalysis(
            id="analysis-1",
            story_cluster_id="cluster-1",
            verified_facts_json="[]",
            open_questions_json="[]",
            why_analysis_text="Why it matters.",
            disagreement_summary="",
            overall_confidence="high",
            low_confidence_reasons_json="[]",
        )
        lead_draft = ArticleDraft(
            id="draft-1",
            story_analysis_id="analysis-1",
            headline="Database-backed lead story",
            dek="Lead dek",
            body_json="[]",
            facts_json="[]",
            analysis_json="[]",
            citations_json="[]",
            validation_status="valid",
        )
        developing_draft = ArticleDraft(
            id="draft-2",
            story_analysis_id="analysis-1",
            headline="Database-backed developing story",
            dek="Developing dek",
            body_json="[]",
            facts_json="[]",
            analysis_json="[]",
            citations_json="[]",
            validation_status="valid",
        )
        lead_article = PublishedArticle(
            id="article-1",
            article_draft_id="draft-1",
            slug="db-backed-lead-story",
            status=ArticleStatus.PUBLISHED,
            homepage_eligible=True,
            rendered_snapshot_json=json.dumps(
                {
                    "slug": "db-backed-lead-story",
                    "headline": "Database-backed lead story",
                    "status": "published",
                    "confidence": "high",
                    "source_count": 3,
                    "updated_at": "2026-03-17T10:00:00Z",
                    "dek": "Lead dek",
                    "facts": [{"text": "Fact from DB", "citations": ["Source A"]}],
                    "analysis": ["Analysis from DB"],
                    "disagreements": ["Disagreement from DB"],
                    "sources": ["Source A", "Source B", "Source C"],
                    "story_tier": "standard",
                    "requested_profile": "balanced",
                    "effective_profile": "balanced",
                }
            ),
        )
        developing_article = PublishedArticle(
            id="article-2",
            article_draft_id="draft-2",
            slug="db-backed-developing-story",
            status=ArticleStatus.DEVELOPING,
            homepage_eligible=False,
            rendered_snapshot_json=json.dumps(
                {
                    "slug": "db-backed-developing-story",
                    "headline": "Database-backed developing story",
                    "status": "developing_story",
                    "confidence": "low",
                    "source_count": 1,
                    "updated_at": "2026-03-17T11:00:00Z",
                    "dek": "Developing dek",
                    "facts": [{"text": "Only one source", "citations": ["Source Z"]}],
                    "analysis": ["Needs more corroboration"],
                    "disagreements": [],
                    "sources": ["Source Z"],
                    "story_tier": "developing",
                    "requested_profile": "economy",
                    "effective_profile": "economy",
                }
            ),
        )

        session.add_all(
            [
                cluster,
                analysis,
                lead_draft,
                developing_draft,
                lead_article,
                developing_article,
            ]
        )
        session.commit()
    engine.dispose()


def test_article_services_read_from_database(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-articles-{uuid.uuid4().hex}.db"
    database_url = f"sqlite+pysqlite:///{database_path}"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", database_url)
    try:
        _seed_articles(database_url)

        listing = list_articles()
        detail = get_article_by_slug("db-backed-lead-story")

        assert listing["lead_story"]["slug"] == "db-backed-lead-story"
        assert listing["developing_stories"][0]["slug"] == "db-backed-developing-story"
        assert detail is not None
        assert detail["headline"] == "Database-backed lead story"
        assert detail["facts"][0]["text"] == "Fact from DB"
    finally:
        if database_path.exists():
            database_path.unlink()


def test_article_detail_normalizes_preview_snapshot_shape(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-articles-preview-{uuid.uuid4().hex}.db"
    database_url = f"sqlite+pysqlite:///{database_path}"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", database_url)
    engine = build_engine(database_url)
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            cluster = StoryCluster(
                id="cluster-preview",
                cluster_key="cluster-preview",
                topic_label="Preview",
                status="active",
            )
            analysis = StoryAnalysis(
                id="analysis-preview",
                story_cluster_id="cluster-preview",
                verified_facts_json="[]",
                open_questions_json="[]",
                why_analysis_text="Why it matters.",
                disagreement_summary="",
                overall_confidence="high",
                low_confidence_reasons_json="[]",
            )
            draft = ArticleDraft(
                id="draft-preview",
                story_analysis_id="analysis-preview",
                headline="Preview headline",
                dek="Preview dek",
                body_json="[]",
                facts_json="[]",
                analysis_json="[]",
                citations_json="[]",
                validation_status="valid",
            )
            article = PublishedArticle(
                id="article-preview",
                article_draft_id="draft-preview",
                slug="preview-story",
                status=ArticleStatus.PUBLISHED,
                homepage_eligible=True,
                rendered_snapshot_json=json.dumps(
                    {
                        "slug": "preview-story",
                        "headline": "Preview headline",
                        "status": "published",
                        "confidence": "high",
                        "source_count": 2,
                        "updated_at": "2026-03-19T22:00:00Z",
                        "dek": "Preview dek",
                        "facts": [
                            {
                                "statement": "Preview fact statement",
                                "sources": ["Source A", "Source B"],
                            }
                        ],
                        "analysis": ["Preview analysis"],
                        "disagreements": [],
                        "sources": [
                            {
                                "organization": "Capgemini",
                                "type": "Industry Research Report",
                            },
                            {"organization": "IBM"},
                        ],
                        "story_tier": "standard",
                        "requested_profile": "balanced",
                        "effective_profile": "balanced",
                    }
                ),
            )
            session.add_all([cluster, analysis, draft, article])
            session.commit()

        detail = get_article_by_slug("preview-story")

        assert detail is not None
        assert detail["facts"][0]["text"] == "Preview fact statement"
        assert detail["facts"][0]["citations"] == ["Source A", "Source B"]
        assert detail["sources"] == [
            {
                "label": "Capgemini",
                "publisher": "Capgemini",
                "title": "Industry Research Report",
                "url": None,
                "role": "source",
            },
            {
                "label": "IBM",
                "publisher": "IBM",
                "title": None,
                "url": None,
                "role": "source",
            },
        ]
    finally:
        engine.dispose()
        if database_path.exists():
            database_path.unlink()


def test_homepage_endpoint_returns_live_published_and_developing_sections():
    client = TestClient(app)

    response = client.get("/api/articles")

    assert response.status_code == 200

    payload = response.json()

    assert payload["lead_story"]["slug"]
    assert payload["lead_story"]["status"] in {"published", "developing_story"}
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


def test_admin_published_endpoint_returns_only_published_articles(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-admin-published-{uuid.uuid4().hex}.db"
    database_url = f"sqlite+pysqlite:///{database_path}"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", database_url)

    try:
        _seed_articles(database_url)
        client = TestClient(app)
        response = client.get(
            "/api/admin/published",
            headers={"x-owner-token": "corewire-owner-token"},
        )

        assert response.status_code == 200
        payload = response.json()
        assert [item["slug"] for item in payload] == ["db-backed-lead-story"]
    finally:
        if database_path.exists():
            database_path.unlink()
