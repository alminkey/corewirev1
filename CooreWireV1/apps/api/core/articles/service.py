from core.db.models.article import ArticleStatus

from core.articles.schemas import ArticleDetail, StoryCard


def _story_cards() -> list[StoryCard]:
    return [
        {
            "slug": "corewire-launched-the-pipeline",
            "headline": "CoreWire launched the integrated pipeline.",
            "status": ArticleStatus.PUBLISHED.value,
            "confidence": "high",
            "source_count": 2,
            "updated_at": "2026-03-12T10:00:00Z",
            "dek": "Two independent sources support the launch sequence.",
        },
        {
            "slug": "corewire-seo-hardening-underway",
            "headline": "CoreWire continues SEO hardening work.",
            "status": ArticleStatus.PUBLISHED.value,
            "confidence": "medium",
            "source_count": 2,
            "updated_at": "2026-03-12T11:00:00Z",
            "dek": "Search integrity and metadata work moved into integration scope.",
        },
        {
            "slug": "corewire-verifying-the-rollout-details",
            "headline": "CoreWire is still verifying rollout details.",
            "status": ArticleStatus.DEVELOPING.value,
            "confidence": "low",
            "source_count": 1,
            "updated_at": "2026-03-12T12:00:00Z",
            "dek": "The story remains visible off homepage lead placement while corroboration continues.",
        },
    ]


def _article_details() -> dict[str, ArticleDetail]:
    return {
        "corewire-launched-the-pipeline": {
            **_story_cards()[0],
            "facts": [
                {
                    "text": "Two supporting source documents confirm the pipeline launch.",
                    "citations": ["Source 1", "Source 2"],
                }
            ],
            "analysis": [
                "The successful orchestration path reduces the gap between skeleton code and a runnable runtime."
            ],
            "disagreements": [
                "Sources agree on the launch but differ on how complete the rollout is."
            ],
            "sources": ["Source 1", "Source 2"],
        },
        "corewire-verifying-the-rollout-details": {
            **_story_cards()[2],
            "facts": [
                {
                    "text": "Only one source currently backs the rollout details.",
                    "citations": ["Source 3"],
                }
            ],
            "analysis": [
                "The developing label protects the homepage until independent corroboration arrives."
            ],
            "disagreements": [],
            "sources": ["Source 3"],
        },
    }


def list_articles() -> dict:
    story_cards = _story_cards()
    return {
        "lead_story": story_cards[0],
        "top_stories": [story_cards[1]],
        "developing_stories": [story_cards[2]],
    }


def get_article_by_slug(slug: str) -> ArticleDetail | None:
    return _article_details().get(slug)


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

