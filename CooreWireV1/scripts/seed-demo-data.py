from pathlib import Path
import sys
import json
import os
from datetime import UTC, datetime

from sqlalchemy import text

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from core.db.base import Base
from core.db.models.article import ArticleStatus
from core.db.session import build_engine, build_session_factory
from core.repositories.articles import ArticleRepository
from core.repositories.stories import StoryRepository


def _database_url() -> str:
    return os.getenv("COREWIRE_DATABASE_URL", "sqlite:///corewire-local.db")


def _demo_snapshots() -> list[dict]:
    return [
        {
            "draft_id": "draft-high-1",
            "analysis_id": "analysis-corewire-1",
            "slug": "corewire-launched-the-pipeline",
            "status": ArticleStatus.PUBLISHED.value,
            "homepage_eligible": True,
            "headline": "CoreWire launched the integrated pipeline.",
            "dek": "Two independent sources support the launch sequence.",
            "confidence": "high",
            "source_count": 2,
            "updated_at": "2026-03-12T10:00:00Z",
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
            "story_tier": "standard",
            "requested_profile": "balanced",
            "effective_profile": "balanced",
        },
        {
            "draft_id": "draft-high-2",
            "analysis_id": "analysis-corewire-2",
            "slug": "corewire-seo-hardening-underway",
            "status": ArticleStatus.PUBLISHED.value,
            "homepage_eligible": False,
            "headline": "CoreWire continues SEO hardening work.",
            "dek": "Search integrity and metadata work moved into integration scope.",
            "confidence": "medium",
            "source_count": 2,
            "updated_at": "2026-03-12T11:00:00Z",
            "facts": [
                {
                    "text": "SEO hardening remains part of the integration scope.",
                    "citations": ["Source 1", "Source 2"],
                }
            ],
            "analysis": [
                "Technical SEO work improves search integrity without changing the editorial model."
            ],
            "disagreements": [],
            "sources": ["Source 1", "Source 2"],
            "story_tier": "standard",
            "requested_profile": "balanced",
            "effective_profile": "balanced",
        },
        {
            "draft_id": "draft-low-1",
            "analysis_id": "analysis-corewire-3",
            "slug": "corewire-verifying-the-rollout-details",
            "status": ArticleStatus.DEVELOPING.value,
            "homepage_eligible": False,
            "headline": "CoreWire is still verifying rollout details.",
            "dek": "The story remains visible off homepage lead placement while corroboration continues.",
            "confidence": "low",
            "source_count": 1,
            "updated_at": "2026-03-12T12:00:00Z",
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
            "story_tier": "developing",
            "requested_profile": "economy",
            "effective_profile": "economy",
        },
    ]


def seed_demo_data() -> dict[str, int]:
    engine = build_engine(_database_url())
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)

    with session_factory() as session:
        story_repository = StoryRepository(session)
        article_repository = ArticleRepository(session)

        session.execute(text("DELETE FROM published_articles"))
        session.execute(text("DELETE FROM article_drafts"))
        session.execute(text("DELETE FROM story_analysis"))
        session.execute(text("DELETE FROM story_clusters"))

        snapshots = _demo_snapshots()

        for index, snapshot in enumerate(snapshots, start=1):
            cluster = story_repository.create_cluster(
                {
                    "id": f"cluster-{index}",
                    "cluster_key": snapshot["slug"],
                    "topic_label": snapshot["headline"],
                    "status": "active",
                }
            )
            analysis = story_repository.create_analysis(
                {
                    "id": snapshot["analysis_id"],
                    "story_cluster_id": cluster.id,
                    "overall_confidence": snapshot["confidence"],
                    "why_analysis_text": " ".join(snapshot["analysis"]),
                    "disagreement_summary": " ".join(snapshot["disagreements"]),
                    "verified_facts_json": json.dumps(snapshot["facts"]),
                    "open_questions_json": "[]",
                    "low_confidence_reasons_json": "[]",
                }
            )
            draft = article_repository.create_draft(
                {
                    "id": snapshot["draft_id"],
                    "story_analysis_id": analysis.id,
                    "headline": snapshot["headline"],
                    "dek": snapshot["dek"],
                    "body_json": json.dumps([]),
                    "facts_json": json.dumps(snapshot["facts"]),
                    "analysis_json": json.dumps(snapshot["analysis"]),
                    "citations_json": json.dumps(snapshot["sources"]),
                    "validation_status": "valid",
                }
            )
            article_repository.create_published_article(
                {
                    "id": f"article-{index}",
                    "article_draft_id": draft.id,
                    "slug": snapshot["slug"],
                    "status": snapshot["status"],
                    "homepage_eligible": snapshot["homepage_eligible"],
                    "published_at": datetime.now(UTC),
                    "updated_at": datetime.now(UTC),
                    "rendered_snapshot_json": json.dumps(snapshot),
                }
            )

        session.commit()

    engine.dispose()

    return {
        "published_articles": len(_demo_snapshots()),
        "homepage_articles": sum(
            1 for article in _demo_snapshots() if article["homepage_eligible"]
        ),
        "developing_articles": sum(
            1 for article in _demo_snapshots() if article["status"] == "developing_story"
        ),
    }


if __name__ == "__main__":
    print(seed_demo_data())
