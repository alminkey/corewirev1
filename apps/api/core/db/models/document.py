from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str | None] = mapped_column(String(255))
    domain: Mapped[str | None] = mapped_column(String(255))
    rss_url: Mapped[str | None] = mapped_column(String(1024))
    language: Mapped[str | None] = mapped_column(String(32))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    items: Mapped[list["SourceItem"]] = relationship(back_populates="source")


class SourceItem(Base):
    __tablename__ = "source_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id"), index=True)
    original_url: Mapped[str | None] = mapped_column(String(2048))
    canonical_url: Mapped[str | None] = mapped_column(String(2048))
    discovered_at: Mapped[DateTime | None] = mapped_column(DateTime)
    published_at: Mapped[DateTime | None] = mapped_column(DateTime)
    acquisition_status: Mapped[str | None] = mapped_column(String(64))
    raw_html_object_key: Mapped[str | None] = mapped_column(String(512))

    source: Mapped["Source"] = relationship(back_populates="items")
    document: Mapped["Document"] = relationship(back_populates="source_item")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    source_item_id: Mapped[str] = mapped_column(
        ForeignKey("source_items.id"), index=True
    )
    title: Mapped[str | None] = mapped_column(String(512))
    dek: Mapped[str | None] = mapped_column(String(512))
    byline: Mapped[str | None] = mapped_column(String(255))
    language: Mapped[str | None] = mapped_column(String(32))
    body_text: Mapped[str | None] = mapped_column(Text)
    extraction_quality_score: Mapped[str | None] = mapped_column(String(64))
    extracted_at: Mapped[DateTime | None] = mapped_column(DateTime)

    source_item: Mapped["SourceItem"] = relationship(back_populates="document")

