from fastapi import APIRouter, Depends

from core.admin.auth import require_owner_token


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/overview", dependencies=[Depends(require_owner_token)])
def get_admin_overview() -> dict:
    return {
        "publish_mode": "hybrid",
        "system_health": "stable",
        "review_queue_count": 3,
    }
