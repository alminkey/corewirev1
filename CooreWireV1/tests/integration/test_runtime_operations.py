from pathlib import Path


def test_runtime_backup_restore_assets_exist_and_are_documented():
    root = Path(__file__).resolve().parents[2]

    backup_script = root / "scripts" / "backup-postgres.ps1"
    restore_script = root / "scripts" / "restore-postgres.ps1"
    runbook = root / "docs" / "ops" / "production-readiness-checklist.md"

    assert backup_script.exists()
    assert restore_script.exists()

    backup_text = backup_script.read_text(encoding="utf-8")
    restore_text = restore_script.read_text(encoding="utf-8")
    runbook_text = runbook.read_text(encoding="utf-8")

    assert "docker compose" in backup_text
    assert "pg_dump" in backup_text
    assert "docker compose" in restore_text
    assert "psql" in restore_text
    assert "backup" in runbook_text.lower()
    assert "restore" in runbook_text.lower()
