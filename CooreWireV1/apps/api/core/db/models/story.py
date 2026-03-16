from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class StoryCluster(Base):
    __tablename__ = "story_clusters"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    cluster_key: Mapped[str | None] = mapped_column(String(255))
    topic_label: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str | None] = mapped_column(String(64))
    first_seen_at: Mapped[DateTime | None] = mapped_column(DateTime)
    last_updated_at: Mapped[DateTime | None] = mapped_column(DateTime)

    analyses: Mapped[list["StoryAnalysis"]] = relationship(back_populates="cluster")


class StoryAnalysis(Base):
    __tablename__ = "story_analysis"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    story_cluster_id: Mapped[str] = mapped_column(
        ForeignKey("story_clusters.id"), index=True
    )
    verified_facts_json: Mapped[str | None] = mapped_column(Text)
    open_questions_json: Mapped[str | None] = mapped_column(Text)
    why_analysis_text: Mapped[str | None] = mapped_column(Text)
    disagreement_summary: Mapped[str | None] = mapped_column(Text)
    overall_confidence: Mapped[str | None] = mapped_column(String(32))
    low_confidence_reasons_json: Mapped[str | None] = mapped_column(Text)

    cluster: Mapped["StoryCluster"] = relationship(back_populates="analyses")

