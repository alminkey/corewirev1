from fastapi import APIRouter, Depends

from core.admin.auth import require_owner_token
from core.analytics.service import get_analytics_summary


router = APIRouter(prefix="/admin", tags=["analytics"])


@router.get("/analytics", dependencies=[Depends(require_owner_token)])
def get_admin_analytics() -> dict:
    return get_analytics_summary()
