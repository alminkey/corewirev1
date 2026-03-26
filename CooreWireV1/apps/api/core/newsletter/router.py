from fastapi import APIRouter, HTTPException

from core.newsletter.service import subscribe_newsletter


router = APIRouter(prefix="/newsletter", tags=["newsletter"])


@router.post("/subscribe")
def subscribe_newsletter_route(payload: dict) -> dict:
    try:
        return subscribe_newsletter(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
