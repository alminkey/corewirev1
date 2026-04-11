from fastapi import APIRouter, Depends, HTTPException

from core.articles.service import list_published_articles_feed
from core.admin.auth import require_owner_token
from core.admin.content import (
    archive_manual_story_draft,
    create_manual_story_draft,
    get_manual_story_draft,
    list_admin_content,
    publish_manual_story_draft,
    update_manual_story_draft,
)
from core.admin.overview import get_admin_overview_summary
from core.admin.programming import get_programming_settings, update_programming_settings
from core.admin.review import apply_review_decision, get_review_detail, get_review_queue
from core.admin.settings import get_autonomy_settings


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/overview", dependencies=[Depends(require_owner_token)])
def get_admin_overview() -> dict:
    return get_admin_overview_summary()


@router.get("/settings/autonomy", dependencies=[Depends(require_owner_token)])
def get_admin_autonomy_settings() -> dict:
    return get_autonomy_settings()


@router.get("/settings/programming", dependencies=[Depends(require_owner_token)])
def get_admin_programming_settings() -> dict:
    return get_programming_settings()


@router.put("/settings/programming", dependencies=[Depends(require_owner_token)])
def put_admin_programming_settings(payload: dict) -> dict:
    return update_programming_settings(payload)


@router.get("/review-queue", dependencies=[Depends(require_owner_token)])
def get_admin_review_queue() -> dict:
    return get_review_queue()


@router.get("/published", dependencies=[Depends(require_owner_token)])
def get_admin_published_articles() -> list[dict]:
    return list_published_articles_feed()


@router.get("/content", dependencies=[Depends(require_owner_token)])
def get_admin_content() -> dict:
    return list_admin_content()


@router.post("/content/drafts", dependencies=[Depends(require_owner_token)])
def post_admin_content_draft(payload: dict) -> dict:
    return create_manual_story_draft(payload)


@router.get("/content/drafts/{draft_id}", dependencies=[Depends(require_owner_token)])
def get_admin_content_draft(draft_id: str) -> dict:
    draft = get_manual_story_draft(draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="Draft not found")
    return draft


@router.patch("/content/drafts/{draft_id}", dependencies=[Depends(require_owner_token)])
def patch_admin_content_draft(draft_id: str, payload: dict) -> dict:
    draft = update_manual_story_draft(draft_id, payload)
    if draft is None:
        raise HTTPException(status_code=404, detail="Draft not found")
    return draft


@router.post("/content/drafts/{draft_id}/publish", dependencies=[Depends(require_owner_token)])
def post_admin_content_draft_publish(draft_id: str) -> dict:
    draft = publish_manual_story_draft(draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="Draft not found")
    return draft


@router.post("/content/drafts/{draft_id}/archive", dependencies=[Depends(require_owner_token)])
def post_admin_content_draft_archive(draft_id: str) -> dict:
    draft = archive_manual_story_draft(draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="Draft not found")
    return draft


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
