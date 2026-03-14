from fastapi import APIRouter, Depends

from core.admin.auth import require_owner_token
from core.admin.review import get_review_queue
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
