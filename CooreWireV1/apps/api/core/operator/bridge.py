"""Paperclip Bridge V1 read endpoints.

These endpoints expose CoreWire state to Paperclip (and any other internal
caller presenting a valid `x-internal-token`). They are intentionally read-only
and return compact summaries composed from the same sources the owner admin
uses, so Paperclip sees an identical view of the system.
"""

from fastapi import APIRouter, Depends

from core.admin.overview import get_admin_overview_summary
from core.admin.review import get_review_queue
from core.admin.settings import get_autonomy_settings
from core.articles.service import list_published_articles_feed
from core.operator.schemas import (
    AutonomyStateResponse,
    PublishedSummaryResponse,
    ReviewQueueSummaryResponse,
    StatusSummaryResponse,
)
from core.security.internal_auth import require_internal_token


bridge_router = APIRouter(
    prefix="/operator/bridge",
    tags=["operator-bridge"],
    dependencies=[Depends(require_internal_token)],
)


@bridge_router.get("/status")
def read_status_summary() -> StatusSummaryResponse:
    overview = get_admin_overview_summary()
    return {
        "type": "status_summary",
        "health": overview["health"],
        "autonomy": overview["autonomy"],
        "pause_state": overview["pause_state"],
        "queue": overview["queue"],
        "published": overview["published"],
        "recent_activity": overview["recent_activity"],
    }


@bridge_router.get("/review-queue")
def read_review_queue_summary() -> ReviewQueueSummaryResponse:
    queue = get_review_queue()
    pending_drafts = queue.get("pending_drafts", [])
    low_confidence = queue.get("low_confidence", [])
    flagged_items = queue.get("flagged_items", [])
    return {
        "type": "review_queue_summary",
        "totals": {
            "pending_drafts": len(pending_drafts),
            "low_confidence": len(low_confidence),
            "flagged_items": len(flagged_items),
            "review": len(pending_drafts) + len(low_confidence) + len(flagged_items),
        },
        "items": {
            "pending_drafts": pending_drafts,
            "low_confidence": low_confidence,
            "flagged_items": flagged_items,
        },
    }


@bridge_router.get("/published")
def read_published_summary() -> PublishedSummaryResponse:
    published = list_published_articles_feed()
    recent = [
        {
            "slug": item.get("slug", ""),
            "headline": item.get("headline", "Untitled article"),
            "status": item.get("status", ""),
            "confidence": item.get("confidence", ""),
            "updated_at": item.get("updated_at", ""),
        }
        for item in published[:10]
    ]
    return {
        "type": "published_summary",
        "total": len(published),
        "recent": recent,
    }


@bridge_router.get("/autonomy")
def read_autonomy_state() -> AutonomyStateResponse:
    autonomy = get_autonomy_settings()
    return {
        "type": "autonomy_state",
        **autonomy,
    }
