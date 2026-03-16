from fastapi import APIRouter, HTTPException

from core.articles.service import get_article_by_slug, list_articles, publish_article


router = APIRouter()


@router.get("/articles")
def list_articles_route() -> dict:
    return list_articles()


@router.get("/articles/{slug}")
def get_article_route(slug: str) -> dict:
    article = get_article_by_slug(slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("/articles/publish")
def publish_article_route(payload: dict) -> dict:
    return publish_article(
        draft=payload.get("draft", {}),
        confidence=payload.get("confidence", {}),
    )

