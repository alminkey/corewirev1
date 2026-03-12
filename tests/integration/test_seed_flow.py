from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


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
