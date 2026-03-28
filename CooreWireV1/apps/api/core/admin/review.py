import json
import os

from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import joinedload

from core.db.base import Base
from core.db.models.article import ArticleDraft
from core.db.models.story import StoryAnalysis
from core.db.session import build_engine, build_session_factory


def _database_url() -> str:
    return os.getenv("COREWIRE_DATABASE_URL", "sqlite:///corewire-local.db")


def get_review_queue() -> dict:
    database_queue = _load_review_queue_from_database()
    if database_queue is not None:
        return database_queue

    return {
        "pending_drafts": [
            {"id": "draft-1", "headline": "Flagship draft awaiting owner review"}
        ],
        "low_confidence": [
            {"id": "story-1", "headline": "Developing story with limited corroboration"}
        ],
        "flagged_items": [
            {"id": "flag-1", "headline": "Story requires compliance review"}
        ],
    }


def get_review_detail(review_id: str) -> dict | None:
    engine = build_engine(_database_url())
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            Base.metadata.create_all(engine)
            statement = (
                select(ArticleDraft, StoryAnalysis)
                .join(StoryAnalysis, StoryAnalysis.id == ArticleDraft.story_analysis_id)
                .where(ArticleDraft.id == review_id)
            )
            row = session.execute(statement).first()
            if row is None:
                return None
            return _serialize_review_detail(*row)
    except OperationalError:
        return None
    finally:
        engine.dispose()


def apply_review_decision(review_id: str, action: str) -> dict | None:
    status_map = {
        "approve": "published",
        "reject": "rejected",
        "request_rerun": "rerun_requested",
    }
    if action not in status_map:
        raise ValueError(f"Unsupported review action: {action}")

    engine = build_engine(_database_url())
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            Base.metadata.create_all(engine)
            draft = session.get(ArticleDraft, review_id)
            if draft is None:
                return None
            draft.validation_status = status_map[action]
            session.commit()
            return {
                "id": draft.id,
                "status": draft.validation_status,
                "action": action,
            }
    except OperationalError:
        return None
    finally:
        engine.dispose()


def _load_review_queue_from_database() -> dict | None:
    engine = build_engine(_database_url())
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            Base.metadata.create_all(engine)
            statement = (
                select(ArticleDraft, StoryAnalysis)
                .join(StoryAnalysis, StoryAnalysis.id == ArticleDraft.story_analysis_id)
                .order_by(ArticleDraft.id.desc())
            )
            rows = session.execute(statement).all()

            pending_drafts: list[dict] = []
            low_confidence: list[dict] = []
            flagged_items: list[dict] = []

            for draft, analysis in rows:
                item = {
                    "id": draft.id,
                    "headline": draft.headline or "Untitled draft",
                    "status": draft.validation_status,
                }
                if draft.validation_status == "flagged":
                    flagged_items.append(item)
                elif analysis.overall_confidence == "low":
                    low_confidence.append(item)
                elif draft.validation_status == "review_required":
                    pending_drafts.append(item)

            return {
                "pending_drafts": pending_drafts,
                "low_confidence": low_confidence,
                "flagged_items": flagged_items,
            }
    except OperationalError:
        return None
    finally:
        engine.dispose()


def _serialize_review_detail(draft: ArticleDraft, analysis: StoryAnalysis) -> dict:
    draft_payload = _parse_json_object(draft.body_json)
    citations = _parse_json_list(draft.citations_json)
    sources = draft_payload.get("sources") or _extract_source_objects(citations)
    editorial_flags = draft_payload.get("editorial_flags") or []
    facts = _normalize_content_blocks(
        _parse_json_list(draft.facts_json) or draft_payload.get("fact_blocks") or []
    )
    analysis_blocks = _normalize_content_blocks(
        _parse_json_list(draft.analysis_json) or draft_payload.get("analysis_blocks") or []
    )
    reasons = _extract_reason_strings(
        _parse_json_list(analysis.low_confidence_reasons_json)
    ) or _extract_reason_strings(citations)

    return {
        "id": draft.id,
        "headline": draft.headline or draft_payload.get("headline") or "Untitled draft",
        "dek": draft.dek or draft_payload.get("dek") or "",
        "status": draft.validation_status,
        "confidence": analysis.overall_confidence,
        "reasons": reasons,
        "draft": {
            "headline": draft_payload.get("headline") or draft.headline or "Untitled draft",
            "dek": draft_payload.get("dek") or draft.dek or "",
            "narrative": draft_payload.get("narrative") or "",
            "facts": facts,
            "analysis": analysis_blocks,
            "sources": sources,
            "editorial_flags": editorial_flags,
        },
    }


def _parse_json_object(value: str | None) -> dict:
    if not value:
        return {}
    parsed = json.loads(value)
    return parsed if isinstance(parsed, dict) else {}


def _parse_json_list(value: str | None) -> list:
    if not value:
        return []
    parsed = json.loads(value)
    return parsed if isinstance(parsed, list) else []


def _normalize_content_blocks(values: list) -> list[dict]:
    normalized: list[dict] = []
    for value in values:
        if isinstance(value, str):
            normalized.append({"text": value})
        elif isinstance(value, dict):
            normalized.append(value)
    return normalized


def _extract_reason_strings(values: list) -> list[str]:
    reasons: list[str] = []
    for value in values:
        if isinstance(value, str):
            reasons.append(value)
        elif isinstance(value, dict):
            maybe_reason = value.get("message") or value.get("reason")
            if isinstance(maybe_reason, str):
                reasons.append(maybe_reason)
    return reasons


def _extract_source_objects(values: list) -> list[dict]:
    sources: list[dict] = []
    for value in values:
        if isinstance(value, dict) and any(
            value.get(key) for key in ("label", "publisher", "title", "url")
        ):
            sources.append(value)
    return sources
