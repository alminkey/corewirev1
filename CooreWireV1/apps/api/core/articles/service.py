import json
import os

from sqlalchemy.exc import OperationalError

from core.db.models.article import ArticleStatus
from core.db.session import build_engine, build_session_factory

from core.articles.schemas import ArticleDetail, ArticleSource, StoryCard
from core.repositories.articles import ArticleRepository


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
            "sources": [
                {
                    "label": "Source 1",
                    "publisher": "Source 1",
                    "title": None,
                    "url": None,
                    "role": "source",
                },
                {
                    "label": "Source 2",
                    "publisher": "Source 2",
                    "title": None,
                    "url": None,
                    "role": "source",
                },
            ],
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
            "sources": [
                {
                    "label": "Source 3",
                    "publisher": "Source 3",
                    "title": None,
                    "url": None,
                    "role": "source",
                }
            ],
        },
    }


def _database_url() -> str:
    return os.getenv("COREWIRE_DATABASE_URL", "sqlite:///corewire-local.db")


def _snapshot_to_story_card(snapshot: dict) -> StoryCard:
    return {
        "slug": snapshot["slug"],
        "headline": snapshot["headline"],
        "status": snapshot["status"],
        "confidence": snapshot.get("confidence", "unknown"),
        "source_count": snapshot.get("source_count", 0),
        "updated_at": snapshot.get("updated_at", ""),
        "dek": snapshot.get("dek", ""),
        "story_tier": snapshot.get("story_tier", "standard"),
        "requested_profile": snapshot.get("requested_profile", "balanced"),
        "effective_profile": snapshot.get("effective_profile", "balanced"),
    }


def _normalize_source(source: object) -> ArticleSource:
    if isinstance(source, str):
        return {
            "label": source,
            "publisher": source,
            "title": None,
            "url": None,
            "role": "source",
        }

    if isinstance(source, dict):
        publisher = source.get("publisher") or source.get("organization") or source.get("label")
        title = source.get("title") or source.get("type")
        url = source.get("url")
        label = source.get("label") or publisher or title or "Unknown source"
        return {
            "label": str(label),
            "publisher": str(publisher) if publisher else None,
            "title": str(title) if title else None,
            "url": str(url) if url else None,
            "role": str(source.get("role") or "source"),
        }

    return {
        "label": str(source),
        "publisher": str(source),
        "title": None,
        "url": None,
        "role": "source",
    }


def _snapshot_to_article_detail(snapshot: dict) -> ArticleDetail:
    facts = []
    for fact in snapshot.get("facts", []):
        facts.append(
            {
                "text": fact.get("text") or fact.get("statement", ""),
                "citations": fact.get("citations") or fact.get("sources", []),
            }
        )

    return {
        **_snapshot_to_story_card(snapshot),
        "facts": facts,
        "analysis": snapshot.get("analysis", []),
        "disagreements": snapshot.get("disagreements", []),
        "sources": [_normalize_source(source) for source in snapshot.get("sources", [])],
    }


def _load_articles_from_database() -> list[dict]:
    engine = build_engine(_database_url())
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            repository = ArticleRepository(session)
            articles = repository.list_published_articles()
            snapshots = [
                json.loads(article.rendered_snapshot_json)
                for article in articles
                if article.rendered_snapshot_json
            ]
            return snapshots
    except OperationalError:
        return []
    finally:
        engine.dispose()


def list_published_articles_feed() -> list[StoryCard]:
    database_articles = _load_articles_from_database()
    if not database_articles:
        return []

    published = [
        item for item in database_articles
        if item.get("status") == ArticleStatus.PUBLISHED.value
    ]
    return [_snapshot_to_story_card(item) for item in published]


def _load_article_detail_from_database(slug: str) -> dict | None:
    engine = build_engine(_database_url())
    session_factory = build_session_factory(engine)

    try:
        with session_factory() as session:
            repository = ArticleRepository(session)
            article = repository.get_published_article_by_slug(slug)
            if article is None or not article.rendered_snapshot_json:
                return None
            return json.loads(article.rendered_snapshot_json)
    except OperationalError:
        return None
    finally:
        engine.dispose()


def list_articles() -> dict:
    database_articles = _load_articles_from_database()
    if database_articles:
        published = [item for item in database_articles if item.get("status") == ArticleStatus.PUBLISHED.value]
        developing = [item for item in database_articles if item.get("status") == ArticleStatus.DEVELOPING.value]
        lead_story = published[0] if published else (developing[0] if developing else database_articles[0])
        top_stories = published[1:] if len(published) > 1 else []
        return {
            "lead_story": _snapshot_to_story_card(lead_story),
            "top_stories": [_snapshot_to_story_card(item) for item in top_stories],
            "developing_stories": [_snapshot_to_story_card(item) for item in developing],
        }

    story_cards = _story_cards()
    return {
        "lead_story": story_cards[0],
        "top_stories": [story_cards[1]],
        "developing_stories": [story_cards[2]],
    }


def get_article_by_slug(slug: str) -> ArticleDetail | None:
    database_article = _load_article_detail_from_database(slug)
    if database_article is not None:
        return _snapshot_to_article_detail(database_article)
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

