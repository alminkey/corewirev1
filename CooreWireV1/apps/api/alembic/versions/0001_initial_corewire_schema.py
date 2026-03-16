"""Initial CoreWire schema.

Revision ID: 0001_initial_corewire_schema
Revises:
Create Date: 2026-03-10
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_initial_corewire_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sources",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("domain", sa.String(length=255), nullable=True),
        sa.Column("rss_url", sa.String(length=1024), nullable=True),
        sa.Column("language", sa.String(length=32), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_table(
        "source_items",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("source_id", sa.String(length=36), sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("original_url", sa.String(length=2048), nullable=True),
        sa.Column("canonical_url", sa.String(length=2048), nullable=True),
        sa.Column("discovered_at", sa.DateTime(), nullable=True),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("acquisition_status", sa.String(length=64), nullable=True),
        sa.Column("raw_html_object_key", sa.String(length=512), nullable=True),
    )
    op.create_index("ix_source_items_source_id", "source_items", ["source_id"])
    op.create_table(
        "documents",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("source_item_id", sa.String(length=36), sa.ForeignKey("source_items.id"), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=True),
        sa.Column("dek", sa.String(length=512), nullable=True),
        sa.Column("byline", sa.String(length=255), nullable=True),
        sa.Column("language", sa.String(length=32), nullable=True),
        sa.Column("body_text", sa.Text(), nullable=True),
        sa.Column("extraction_quality_score", sa.String(length=64), nullable=True),
        sa.Column("extracted_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_documents_source_item_id", "documents", ["source_item_id"])
    op.create_table(
        "claims",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("document_id", sa.String(length=36), sa.ForeignKey("documents.id"), nullable=False),
        sa.Column("claim_text", sa.Text(), nullable=True),
        sa.Column("claim_type", sa.String(length=64), nullable=True),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("predicate", sa.String(length=255), nullable=True),
        sa.Column("object", sa.String(length=255), nullable=True),
        sa.Column("supporting_quote", sa.Text(), nullable=True),
        sa.Column("extraction_confidence", sa.String(length=32), nullable=True),
    )
    op.create_index("ix_claims_document_id", "claims", ["document_id"])
    op.create_table(
        "claim_evidence",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("claim_id", sa.String(length=36), sa.ForeignKey("claims.id"), nullable=False),
        sa.Column("evidence_document_id", sa.String(length=36), sa.ForeignKey("documents.id"), nullable=False),
        sa.Column("relation_type", sa.String(length=32), nullable=True),
        sa.Column("evidence_quote", sa.Text(), nullable=True),
        sa.Column("evidence_strength", sa.String(length=32), nullable=True),
        sa.Column("source_diversity_weight", sa.String(length=32), nullable=True),
    )
    op.create_index("ix_claim_evidence_claim_id", "claim_evidence", ["claim_id"])
    op.create_index(
        "ix_claim_evidence_evidence_document_id",
        "claim_evidence",
        ["evidence_document_id"],
    )
    op.create_table(
        "story_clusters",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("cluster_key", sa.String(length=255), nullable=True),
        sa.Column("topic_label", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=True),
        sa.Column("first_seen_at", sa.DateTime(), nullable=True),
        sa.Column("last_updated_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "story_analysis",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "story_cluster_id",
            sa.String(length=36),
            sa.ForeignKey("story_clusters.id"),
            nullable=False,
        ),
        sa.Column("verified_facts_json", sa.Text(), nullable=True),
        sa.Column("open_questions_json", sa.Text(), nullable=True),
        sa.Column("why_analysis_text", sa.Text(), nullable=True),
        sa.Column("disagreement_summary", sa.Text(), nullable=True),
        sa.Column("overall_confidence", sa.String(length=32), nullable=True),
        sa.Column("low_confidence_reasons_json", sa.Text(), nullable=True),
    )
    op.create_index("ix_story_analysis_story_cluster_id", "story_analysis", ["story_cluster_id"])
    op.create_table(
        "article_drafts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "story_analysis_id",
            sa.String(length=36),
            sa.ForeignKey("story_analysis.id"),
            nullable=False,
        ),
        sa.Column("headline", sa.String(length=512), nullable=True),
        sa.Column("dek", sa.String(length=512), nullable=True),
        sa.Column("body_json", sa.Text(), nullable=True),
        sa.Column("facts_json", sa.Text(), nullable=True),
        sa.Column("analysis_json", sa.Text(), nullable=True),
        sa.Column("citations_json", sa.Text(), nullable=True),
        sa.Column("validation_status", sa.String(length=64), nullable=True),
    )
    op.create_index("ix_article_drafts_story_analysis_id", "article_drafts", ["story_analysis_id"])
    op.create_table(
        "published_articles",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "article_draft_id",
            sa.String(length=36),
            sa.ForeignKey("article_drafts.id"),
            nullable=False,
        ),
        sa.Column("slug", sa.String(length=512), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("homepage_eligible", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("rendered_snapshot_json", sa.Text(), nullable=True),
    )
    op.create_index(
        "ix_published_articles_article_draft_id",
        "published_articles",
        ["article_draft_id"],
    )
    op.create_table(
        "article_claim_links",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "published_article_id",
            sa.String(length=36),
            sa.ForeignKey("published_articles.id"),
            nullable=False,
        ),
        sa.Column("article_block_key", sa.String(length=255), nullable=True),
        sa.Column("claim_id", sa.String(length=36), nullable=True),
        sa.Column("claim_evidence_id", sa.String(length=36), nullable=True),
    )
    op.create_index(
        "ix_article_claim_links_published_article_id",
        "article_claim_links",
        ["published_article_id"],
    )
    op.create_table(
        "pipeline_runs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("run_type", sa.String(length=64), nullable=True),
        sa.Column("target_id", sa.String(length=36), nullable=True),
        sa.Column("model_name", sa.String(length=128), nullable=True),
        sa.Column("prompt_version", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("error_json", sa.Text(), nullable=True),
    )
    op.create_table(
        "model_artifacts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "pipeline_run_id",
            sa.String(length=36),
            sa.ForeignKey("pipeline_runs.id"),
            nullable=False,
        ),
        sa.Column("artifact_type", sa.String(length=64), nullable=True),
        sa.Column("object_key", sa.String(length=512), nullable=True),
        sa.Column("schema_validation_status", sa.String(length=64), nullable=True),
    )
    op.create_index("ix_model_artifacts_pipeline_run_id", "model_artifacts", ["pipeline_run_id"])


def downgrade() -> None:
    op.drop_index("ix_model_artifacts_pipeline_run_id", table_name="model_artifacts")
    op.drop_table("model_artifacts")
    op.drop_table("pipeline_runs")
    op.drop_index(
        "ix_article_claim_links_published_article_id",
        table_name="article_claim_links",
    )
    op.drop_table("article_claim_links")
    op.drop_index(
        "ix_published_articles_article_draft_id",
        table_name="published_articles",
    )
    op.drop_table("published_articles")
    op.drop_index("ix_article_drafts_story_analysis_id", table_name="article_drafts")
    op.drop_table("article_drafts")
    op.drop_index("ix_story_analysis_story_cluster_id", table_name="story_analysis")
    op.drop_table("story_analysis")
    op.drop_table("story_clusters")
    op.drop_index(
        "ix_claim_evidence_evidence_document_id",
        table_name="claim_evidence",
    )
    op.drop_index("ix_claim_evidence_claim_id", table_name="claim_evidence")
    op.drop_table("claim_evidence")
    op.drop_index("ix_claims_document_id", table_name="claims")
    op.drop_table("claims")
    op.drop_index("ix_documents_source_item_id", table_name="documents")
    op.drop_table("documents")
    op.drop_index("ix_source_items_source_id", table_name="source_items")
    op.drop_table("source_items")
    op.drop_table("sources")

