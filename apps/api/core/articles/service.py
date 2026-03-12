from core.db.models.article import ArticleStatus


def list_articles() -> dict:
    return {
        "lead_story": None,
        "top_stories": [],
        "developing_stories": [],
    }


def publish_article(draft: dict, confidence: dict) -> dict:
    is_low_confidence = confidence.get("level") == "low"

    status = ArticleStatus.PUBLISHED.value
    homepage_eligible = bool(confidence.get("homepage_eligible", True))

    if is_low_confidence:
        status = ArticleStatus.DEVELOPING.value
        homepage_eligible = False

    return {
        "draft_id": draft.get("id"),
        "slug": draft.get("slug"),
        "status": status,
        "homepage_eligible": homepage_eligible,
    }

