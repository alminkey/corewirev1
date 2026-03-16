from fastapi import APIRouter, Depends

from core.articles.service import publish_article
from core.security.internal_auth import require_internal_token


router = APIRouter()


@router.post("/internal/publish", dependencies=[Depends(require_internal_token)])
def internal_publish_article_route(payload: dict) -> dict:
    return publish_article(
        draft=payload.get("draft", {}),
        confidence=payload.get("confidence", {}),
    )
