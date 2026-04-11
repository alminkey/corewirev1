import json
import os
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from core.articles.service import list_published_articles_feed
from core.db.base import Base
from core.db.models.article import ArticleDraft, ArticleStatus
from core.db.models.story import StoryAnalysis, StoryCluster
from core.db.session import build_engine, build_session_factory
from core.repositories.articles import ArticleRepository


def _database_url() -> str:
    return os.getenv("COREWIRE_DATABASE_URL", "sqlite:///corewire-local.db")


def list_admin_content() -> dict:
    engine = build_engine(_database_url())
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            Base.metadata.create_all(engine)
            drafts = list(
                session.scalars(select(ArticleDraft).order_by(ArticleDraft.id.desc())).all()
            )
            return {
                "drafts": [_serialize_draft(draft) for draft in drafts],
                "published": list_published_articles_feed(),
            }
    except OperationalError:
        return {"drafts": [], "published": list_published_articles_feed()}
    finally:
        engine.dispose()


def create_manual_story_draft(payload: dict) -> dict:
    engine = build_engine(_database_url())
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            Base.metadata.create_all(engine)

            cluster = StoryCluster(
                id=str(uuid.uuid4()),
                cluster_key=payload.get("slug") or payload.get("headline") or "manual-story",
                topic_label=payload.get("headline") or "Manual story",
                status="manual",
            )
            analysis = StoryAnalysis(
                id=str(uuid.uuid4()),
                story_cluster_id=cluster.id,
                verified_facts_json="[]",
                open_questions_json="[]",
                why_analysis_text="",
                disagreement_summary="",
                overall_confidence="manual",
                low_confidence_reasons_json="[]",
            )
            draft = ArticleDraft(
                id=str(uuid.uuid4()),
                story_analysis_id=analysis.id,
                headline=payload.get("headline"),
                dek=payload.get("dek"),
                body_json=json.dumps(
                    {
                        "headline": payload.get("headline", ""),
                        "dek": payload.get("dek", ""),
                        "full_article": payload.get("body", ""),
                        "slug": payload.get("slug", ""),
                        "tags": payload.get("tags", []),
                    }
                ),
                facts_json="[]",
                analysis_json="[]",
                citations_json="[]",
                validation_status="draft",
            )
            session.add_all([cluster, analysis, draft])
            session.commit()
            session.refresh(draft)
            return _serialize_draft(draft)
    finally:
        engine.dispose()


def get_manual_story_draft(draft_id: str) -> dict | None:
    engine = build_engine(_database_url())
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            Base.metadata.create_all(engine)
            draft = session.get(ArticleDraft, draft_id)
            if draft is None:
                return None
            return _serialize_draft(draft)
    finally:
        engine.dispose()


def update_manual_story_draft(draft_id: str, payload: dict) -> dict | None:
    engine = build_engine(_database_url())
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            Base.metadata.create_all(engine)
            draft = session.get(ArticleDraft, draft_id)
            if draft is None:
                return None

            body_payload = _parse_json_object(draft.body_json)
            body_payload.update(
                {
                    "headline": payload.get("headline", draft.headline or body_payload.get("headline", "")),
                    "dek": payload.get("dek", draft.dek or body_payload.get("dek", "")),
                    "full_article": payload.get(
                        "body", body_payload.get("full_article") or body_payload.get("body", "")
                    ),
                    "slug": payload.get("slug", body_payload.get("slug", "")),
                    "tags": payload.get("tags", body_payload.get("tags", [])),
                }
            )

            if "headline" in payload:
                draft.headline = payload["headline"]
            if "dek" in payload:
                draft.dek = payload["dek"]

            draft.body_json = json.dumps(body_payload)
            session.commit()
            session.refresh(draft)
            return _serialize_draft(draft)
    finally:
        engine.dispose()


def publish_manual_story_draft(draft_id: str) -> dict | None:
    engine = build_engine(_database_url())
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            Base.metadata.create_all(engine)
            draft = session.get(ArticleDraft, draft_id)
            if draft is None:
                return None

            draft.validation_status = ArticleStatus.PUBLISHED.value
            _upsert_published_article(session, draft, status=ArticleStatus.PUBLISHED.value)
            session.commit()
            session.refresh(draft)
            return _serialize_draft(draft)
    finally:
        engine.dispose()


def archive_manual_story_draft(draft_id: str) -> dict | None:
    engine = build_engine(_database_url())
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            Base.metadata.create_all(engine)
            draft = session.get(ArticleDraft, draft_id)
            if draft is None:
                return None

            draft.validation_status = "archived"
            _upsert_published_article(session, draft, status=ArticleStatus.SUPERSEDED.value)
            session.commit()
            session.refresh(draft)
            return _serialize_draft(draft)
    finally:
        engine.dispose()


def _parse_json_object(value: str | None) -> dict:
    if not value:
        return {}
    parsed = json.loads(value)
    return parsed if isinstance(parsed, dict) else {}


def _serialize_draft(draft: ArticleDraft) -> dict:
    body_payload = _parse_json_object(draft.body_json)
    return {
        "id": draft.id,
        "headline": draft.headline or body_payload.get("headline", ""),
        "dek": draft.dek or body_payload.get("dek", ""),
        "body": body_payload.get("full_article") or body_payload.get("body", ""),
        "slug": body_payload.get("slug", ""),
        "tags": body_payload.get("tags", []),
        "status": draft.validation_status or "draft",
    }


def _upsert_published_article(session, draft: ArticleDraft, *, status: str) -> None:
    article_repository = ArticleRepository(session)
    now = datetime.now(UTC)
    snapshot = _build_manual_snapshot(draft, status=status, updated_at=now)
    slug = snapshot["slug"]
    homepage_eligible = status == ArticleStatus.PUBLISHED.value

    existing_article = article_repository.get_published_article_by_slug(slug)
    if existing_article is not None:
        article_repository.update_published_article_status(
            slug,
            status=status,
            homepage_eligible=homepage_eligible,
            rendered_snapshot_json=json.dumps(snapshot),
            updated_at=now,
        )
        return

    if status != ArticleStatus.PUBLISHED.value:
        return

    article_repository.create_published_article(
        {
            "id": str(uuid.uuid4()),
            "article_draft_id": draft.id,
            "slug": slug,
            "status": status,
            "homepage_eligible": homepage_eligible,
            "published_at": now,
            "updated_at": now,
            "rendered_snapshot_json": json.dumps(snapshot),
        }
    )


def _build_manual_snapshot(draft: ArticleDraft, *, status: str, updated_at: datetime) -> dict:
    body_payload = _parse_json_object(draft.body_json)
    headline = draft.headline or body_payload.get("headline") or "Untitled draft"
    dek = draft.dek or body_payload.get("dek") or ""
    slug = body_payload.get("slug") or headline.lower().replace(" ", "-")
    tags = body_payload.get("tags", [])

    return {
        "slug": slug,
        "headline": headline,
        "status": status,
        "confidence": "manual",
        "source_count": 0,
        "updated_at": updated_at.isoformat(),
        "dek": dek,
        "full_article": body_payload.get("full_article") or body_payload.get("body", ""),
        "facts": [],
        "analysis": [],
        "disagreements": [],
        "sources": [],
        "story_tier": "manual",
        "requested_profile": "manual",
        "effective_profile": "manual",
        "tags": tags,
    }
