from core.admin.review import get_review_queue
from core.admin.settings import get_autonomy_settings
from core.articles.service import list_published_articles_feed


def get_admin_overview_summary() -> dict:
    autonomy = get_autonomy_settings()
    review_queue = get_review_queue()
    published = list_published_articles_feed()

    pending_drafts = review_queue.get("pending_drafts", [])
    low_confidence = review_queue.get("low_confidence", [])
    flagged_items = review_queue.get("flagged_items", [])

    recent_activity: list[dict] = []
    for item in published[:3]:
        recent_activity.append(
            {
                "type": "published",
                "headline": item.get("headline", "Untitled article"),
                "slug": item.get("slug", ""),
                "updated_at": item.get("updated_at", ""),
            }
        )

    return {
        "health": {
            "system": "stable",
        },
        "autonomy": autonomy,
        "pause_state": {
            "ingest": autonomy["pause_ingest"],
            "publish": autonomy["pause_publish"],
        },
        "queue": {
            "review": len(pending_drafts) + len(low_confidence) + len(flagged_items),
            "pending_drafts": len(pending_drafts),
            "low_confidence": len(low_confidence),
            "flagged_items": len(flagged_items),
        },
        "published": {
            "total": len(published),
        },
        "recent_activity": recent_activity,
        # Backward-compatible fields for existing consumers.
        "publish_mode": autonomy["mode"],
        "system_health": "stable",
        "review_queue_count": len(pending_drafts) + len(low_confidence) + len(flagged_items),
    }
