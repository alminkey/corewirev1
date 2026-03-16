from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine, inspect


def load_migration_module():
    path = (
        Path(__file__).resolve().parents[2]
        / "apps"
        / "api"
        / "alembic"
        / "versions"
        / "0001_initial_corewire_schema.py"
    )
    spec = spec_from_file_location("corewire_migration_0001", path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_initial_migration_creates_required_tables():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    migration = load_migration_module()

    with engine.begin() as connection:
        migration.op = Operations(MigrationContext.configure(connection))
        migration.upgrade()

        table_names = set(inspect(connection).get_table_names())

    assert "sources" in table_names
    assert "source_items" in table_names
    assert "documents" in table_names
    assert "story_clusters" in table_names
    assert "article_drafts" in table_names
    assert "published_articles" in table_names
    assert "pipeline_runs" in table_names
