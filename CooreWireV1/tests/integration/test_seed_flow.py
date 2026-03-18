from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import uuid
import sys

from sqlalchemy import text


def load_seed_module():
    path = Path(__file__).resolve().parents[2] / "scripts" / "seed-demo-data.py"
    spec = spec_from_file_location("corewire_seed_demo_data", path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_seed_flow_creates_homepage_story_and_developing_story():
    seed_module = load_seed_module()

    seeded_counts = seed_module.seed_demo_data()

    assert seeded_counts["published_articles"] >= 2
    assert seeded_counts["homepage_articles"] >= 1
    assert seeded_counts["developing_articles"] >= 1


def test_seed_flow_persists_articles_for_api_queries(monkeypatch):
    root = Path(__file__).resolve().parents[2]
    database_path = root / f"test-seed-{uuid.uuid4().hex}.db"
    database_url = f"sqlite+pysqlite:///{database_path}"

    monkeypatch.setenv("COREWIRE_DATABASE_URL", database_url)

    seed_module = load_seed_module()
    seed_module.seed_demo_data()
    api_path = str(root / "apps" / "api")
    if api_path not in sys.path:
        sys.path.insert(0, api_path)
    sys.modules.pop("core", None)

    from core.articles.service import list_articles
    from core.db.session import build_engine

    listing = list_articles()
    engine = build_engine(database_url)

    try:
        with engine.connect() as connection:
            published_count = connection.execute(
                text("select count(*) from published_articles")
            ).scalar_one()

        assert published_count >= 2
        assert listing["lead_story"]["slug"] == "corewire-launched-the-pipeline"
        assert listing["developing_stories"][0]["slug"] == "corewire-verifying-the-rollout-details"
    finally:
        engine.dispose()
        if database_path.exists():
            database_path.unlink()
