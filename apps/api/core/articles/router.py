from fastapi import APIRouter

from core.articles.service import list_articles, publish_article


router = APIRouter()


@router.get("/articles")
def list_articles_route() -> dict:
    return list_articles()


@router.post("/articles/publish")
def publish_article_route(payload: dict) -> dict:
    return publish_article(
        draft=payload.get("draft", {}),
        confidence=payload.get("confidence", {}),
    )

