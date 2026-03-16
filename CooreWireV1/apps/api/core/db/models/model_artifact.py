from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class ModelArtifact(Base):
    __tablename__ = "model_artifacts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    pipeline_run_id: Mapped[str] = mapped_column(
        ForeignKey("pipeline_runs.id"), index=True
    )
    artifact_type: Mapped[str | None] = mapped_column(String(64))
    object_key: Mapped[str | None] = mapped_column(String(512))
    schema_validation_status: Mapped[str | None] = mapped_column(String(64))

