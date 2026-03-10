from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), index=True)
    claim_text: Mapped[str | None] = mapped_column(Text)
    claim_type: Mapped[str | None] = mapped_column(String(64))
    subject: Mapped[str | None] = mapped_column(String(255))
    predicate: Mapped[str | None] = mapped_column(String(255))
    object: Mapped[str | None] = mapped_column(String(255))
    supporting_quote: Mapped[str | None] = mapped_column(Text)
    extraction_confidence: Mapped[str | None] = mapped_column(String(32))

    evidence: Mapped[list["ClaimEvidence"]] = relationship(back_populates="claim")


class ClaimEvidence(Base):
    __tablename__ = "claim_evidence"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    claim_id: Mapped[str] = mapped_column(ForeignKey("claims.id"), index=True)
    evidence_document_id: Mapped[str] = mapped_column(
        ForeignKey("documents.id"), index=True
    )
    relation_type: Mapped[str | None] = mapped_column(String(32))
    evidence_quote: Mapped[str | None] = mapped_column(Text)
    evidence_strength: Mapped[str | None] = mapped_column(String(32))
    source_diversity_weight: Mapped[str | None] = mapped_column(String(32))

    claim: Mapped["Claim"] = relationship(back_populates="evidence")

