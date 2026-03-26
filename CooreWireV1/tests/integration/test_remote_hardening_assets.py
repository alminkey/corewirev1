from pathlib import Path


def test_webtropia_remote_hardening_assets_exist_and_are_documented():
    root = Path(__file__).resolve().parents[2]

    backup_script = root / "scripts" / "backup-postgres.sh"
    restore_script = root / "scripts" / "restore-postgres.sh"
    smoke_script = root / "scripts" / "smoke-webtropia.sh"
    rollback_script = root / "scripts" / "rollback-webtropia.sh"
    env_check_script = root / "scripts" / "check-webtropia-env.sh"
    runbook = root / "docs" / "ops" / "webtropia-deploy.md"

    assert backup_script.exists()
    assert restore_script.exists()
    assert smoke_script.exists()
    assert rollback_script.exists()
    assert env_check_script.exists()

    assert "pg_dump" in backup_script.read_text(encoding="utf-8")
    assert "psql" in restore_script.read_text(encoding="utf-8")
    assert "/health" in smoke_script.read_text(encoding="utf-8")
    assert "docker compose" in rollback_script.read_text(encoding="utf-8")
    assert "OPENROUTER_API_KEY" in env_check_script.read_text(encoding="utf-8")

    runbook_text = runbook.read_text(encoding="utf-8")
    assert "smoke" in runbook_text.lower()
    assert "rollback" in runbook_text.lower()
    assert "env" in runbook_text.lower()
    assert "restore" in runbook_text.lower()
