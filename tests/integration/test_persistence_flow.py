from datetime import UTC, datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2] / "apps" / "api"))
sys.path.append(
    str(Path(__file__).resolve().parents[2] / "apps" / "workers" / "core")
)

from core.db.base import Base
from core.db.session import build_engine, build_session_factory
from core.repositories.articles import ArticleRepository
from core.repositories.stories import StoryRepository
from repositories.pipeline import PipelineRepository


def test_publish_flow_persists_story_and_article_records():
    engine = build_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)

    with session_factory() as session:
        story_repository = StoryRepository(session)
        article_repository = ArticleRepository(session)
        pipeline_repository = PipelineRepository(session)

        cluster = story_repository.create_cluster(
            {
                "id": "cluster-1",
                "cluster_key": "story-one",
                "topic_label": "Story One",
                "status": "active",
            }
        )
        analysis = story_repository.create_analysis(
            {
                "id": "analysis-1",
                "story_cluster_id": cluster.id,
                "overall_confidence": "high",
            }
        )
        draft = article_repository.create_draft(
            {
                "id": "draft-1",
                "story_analysis_id": analysis.id,
                "headline": "Story One Headline",
                "validation_status": "valid",
            }
        )
        article = article_repository.create_published_article(
            {
                "id": "article-1",
                "article_draft_id": draft.id,
                "slug": "story-one-headline",
                "status": "published",
                "homepage_eligible": True,
                "published_at": datetime.now(UTC),
            }
        )
        pipeline_run = pipeline_repository.create_run(
            {
                "id": "run-1",
                "run_type": "publish",
                "target_id": article.id,
                "status": "completed",
            }
        )

        session.commit()

        assert cluster.id == "cluster-1"
        assert analysis.story_cluster_id == cluster.id
        assert draft.story_analysis_id == analysis.id
        assert article.article_draft_id == draft.id
        assert article.status.value == "published"
        assert pipeline_run.target_id == article.id
