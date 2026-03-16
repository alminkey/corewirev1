from pathlib import Path


def test_runtime_and_ops_runbooks_exist():
    root = Path(__file__).resolve().parents[2]

    assert (root / "docs" / "runbooks" / "local-start.md").exists()
    assert (root / "docs" / "ops" / "production-readiness-checklist.md").exists()
    assert (root / "docs" / "ops" / "seo-readiness-checklist.md").exists()
