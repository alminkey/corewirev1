from pathlib import Path


def test_staging_rehearsal_covers_owner_admin_and_paperclip_bridge_v1():
    rehearsal_doc = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "ops"
        / "staging-rehearsal.md"
    )

    assert rehearsal_doc.exists(), "docs/ops/staging-rehearsal.md must exist"

    contents = rehearsal_doc.read_text(encoding="utf-8")

    # Owner admin section
    assert "owner admin" in contents.lower()
    assert "/api/admin/summary" in contents

    # Bridge read checks
    assert "/api/operator/bridge/status" in contents
    assert "/api/operator/bridge/review-queue" in contents
    assert "/api/operator/bridge/published" in contents
    assert "/api/operator/bridge/autonomy" in contents

    # Bridge command checks
    assert "import_external_draft" in contents
    assert "correlation" in contents.lower()

    # Signoff must mention bridge
    assert "bridge" in contents.lower()
