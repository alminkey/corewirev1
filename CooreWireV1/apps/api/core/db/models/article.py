from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class ArticleStatus(str, Enum):
    PUBLISHED = "published"
    DEVELOPING = "developing_story"
    RETRACTED = "retracted"
    SUPERSEDED = "superseded"


class ArticleDraft(Base):
    __tablename__ = "article_drafts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    story_analysis_id: Mapped[str] = mapped_column(
        ForeignKey("story_analysis.id"), index=True
    )
    headline: Mapped[str | None] = mapped_column(String(512))
    dek: Mapped[str | None] = mapped_column(String(512))
    body_json: Mapped[str | None] = mapped_column(Text)
    facts_json: Mapped[str | None] = mapped_column(Text)
    analysis_json: Mapped[str | None] = mapped_column(Text)
    citations_json: Mapped[str | None] = mapped_column(Text)
    validation_status: Mapped[str | None] = mapped_column(String(64))

    published_article: Mapped["PublishedArticle"] = relationship(
        back_populates="draft"
    )


class PublishedArticle(Base):
    __tablename__ = "published_articles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    article_draft_id: Mapped[str] = mapped_column(
        ForeignKey("article_drafts.id"), index=True
    )
    slug: Mapped[str | None] = mapped_column(String(512))
    status: Mapped[ArticleStatus] = mapped_column(SqlEnum(ArticleStatus))
    homepage_eligible: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[DateTime | None] = mapped_column(DateTime)
    updated_at: Mapped[DateTime | None] = mapped_column(DateTime)
    rendered_snapshot_json: Mapped[str | None] = mapped_column(Text)

    draft: Mapped["ArticleDraft"] = relationship(back_populates="published_article")


class ArticleClaimLink(Base):
    __tablename__ = "article_claim_links"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    published_article_id: Mapped[str] = mapped_column(
        ForeignKey("published_articles.id"), index=True
    )
    article_block_key: Mapped[str | None] = mapped_column(String(255))
    claim_id: Mapped[str | None] = mapped_column(String(36))
    claim_evidence_id: Mapped[str | None] = mapped_column(String(36))

