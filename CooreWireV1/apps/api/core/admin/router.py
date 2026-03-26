from fastapi import APIRouter, Depends, HTTPException

from core.articles.service import list_published_articles_feed
from core.admin.auth import require_owner_token
from core.admin.review import apply_review_decision, get_review_detail, get_review_queue
from core.admin.settings import get_autonomy_settings


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/overview", dependencies=[Depends(require_owner_token)])
def get_admin_overview() -> dict:
    return {
        "publish_mode": "hybrid",
        "system_health": "stable",
        "review_queue_count": 3,
    }


@router.get("/settings/autonomy", dependencies=[Depends(require_owner_token)])
def get_admin_autonomy_settings() -> dict:
    return get_autonomy_settings()


@router.get("/review-queue", dependencies=[Depends(require_owner_token)])
def get_admin_review_queue() -> dict:
    return get_review_queue()


@router.get("/published", dependencies=[Depends(require_owner_token)])
def get_admin_published_articles() -> list[dict]:
    return list_published_articles_feed()


@router.get("/review-queue/{review_id}", dependencies=[Depends(require_owner_token)])
def get_admin_review_detail(review_id: str) -> dict:
    detail = get_review_detail(review_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Review item not found")
    return detail


@router.post("/review-queue/{review_id}/decision", dependencies=[Depends(require_owner_token)])
def post_admin_review_decision(review_id: str, payload: dict) -> dict:
    result = apply_review_decision(review_id, payload.get("action", ""))
    if result is None:
        raise HTTPException(status_code=404, detail="Review item not found")
    return result
