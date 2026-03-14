from pathlib import Path


def test_launch_docs_and_e2e_specs_cover_rehearsal_and_smoke_closure():
    repo_root = Path(__file__).resolve().parents[2]

    production_checklist = repo_root / "docs" / "ops" / "production-readiness-checklist.md"
    staging_rehearsal = repo_root / "docs" / "ops" / "staging-rehearsal.md"
    publish_flow_spec = repo_root / "tests" / "e2e" / "publish-flow.spec.ts"
    seo_smoke_spec = repo_root / "tests" / "e2e" / "seo-smoke.spec.ts"

    assert production_checklist.exists()
    assert staging_rehearsal.exists()
    assert publish_flow_spec.exists()
    assert seo_smoke_spec.exists()

    production_text = production_checklist.read_text(encoding="utf-8").lower()
    staging_text = staging_rehearsal.read_text(encoding="utf-8").lower()
    publish_text = publish_flow_spec.read_text(encoding="utf-8").lower()
    seo_text = seo_smoke_spec.read_text(encoding="utf-8").lower()

    assert "rollback" in production_text
    assert "launch signoff" in production_text
    assert "staging rehearsal" in staging_text
    assert "publish flow" in staging_text
    assert "homepage" in publish_text
    assert "article" in publish_text
    assert "sitemap" in seo_text
    assert "robots" in seo_text
