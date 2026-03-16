from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from core.db.models import Document, PublishedArticle, SourceItem


def test_document_belongs_to_source_item():
    document_columns = set(Document.__table__.columns.keys())
    source_item_columns = set(SourceItem.__table__.columns.keys())

    assert "source_item_id" in document_columns
    assert "id" in source_item_columns


def test_published_article_tracks_status_and_homepage_flag():
    columns = set(PublishedArticle.__table__.columns.keys())

    assert "status" in columns
    assert "homepage_eligible" in columns
