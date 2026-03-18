from pathlib import Path
import tomllib


def test_local_runtime_contract_defines_api_web_worker_start_commands():
    root = Path(__file__).resolve().parents[2]

    bootstrap_source = (root / "scripts" / "bootstrap-local.ps1").read_text()
    migrate_source = (root / "scripts" / "migrate-local.ps1").read_text()
    runbook_source = (root / "docs" / "runbooks" / "local-start.md").read_text()
    readme_source = (root / "README.md").read_text()

    assert "uvicorn app:app" in runbook_source
    assert "python apps/workers/main.py" in runbook_source
    assert "pnpm --dir apps/web dev" in runbook_source
    assert "COREWIRE_API_BASE_URL" in runbook_source
    assert "COREWIRE_SITE_URL" in runbook_source
    assert "COREWIRE_INTERNAL_TOKEN" in runbook_source
    assert "Start API" in bootstrap_source
    assert "Start workers" in bootstrap_source
    assert "Start web" in bootstrap_source
    assert "docs/runbooks/local-start.md" in readme_source
    assert "postgresql://corewire:corewire@localhost:5432/corewire" in migrate_source
    assert "sqlite:///corewire-local.db" in runbook_source


def test_api_package_declares_postgresql_driver_for_local_runtime():
    root = Path(__file__).resolve().parents[2]
    pyproject = tomllib.loads((root / "apps" / "api" / "pyproject.toml").read_text())
    dependencies = pyproject["project"]["dependencies"]

    assert any(dep.startswith("psycopg2-binary") or dep.startswith("psycopg") for dep in dependencies)
