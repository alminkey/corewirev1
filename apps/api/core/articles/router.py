from core.articles.service import publish_article


def publish_article_route(payload: dict) -> dict:
    return publish_article(
        draft=payload.get("draft", {}),
        confidence=payload.get("confidence", {}),
    )

