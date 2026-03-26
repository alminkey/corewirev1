from pathlib import Path


def test_github_delivery_assets_exist():
    repo_root = Path(__file__).resolve().parents[3]

    assert (repo_root / ".github" / "CODEOWNERS").exists()
    assert (repo_root / ".github" / "dependabot.yml").exists()
    assert (repo_root / ".github" / "workflows" / "ci.yml").exists()
    assert (repo_root / ".github" / "workflows" / "deploy-staging.yml").exists()
    assert (repo_root / ".github" / "workflows" / "deploy-prod.yml").exists()
    assert (repo_root / ".github" / "workflows" / "security.yml").exists()


def test_webtropia_deployment_assets_exist_and_cover_runtime():
    root = Path(__file__).resolve().parents[2]

    compose_path = root / "infra" / "docker" / "docker-compose.prod.yml"
    caddyfile_path = root / "infra" / "docker" / "Caddyfile"
    deploy_script_path = root / "scripts" / "deploy-webtropia.ps1"
    deploy_script_linux = root / "scripts" / "deploy-webtropia.sh"
    runbook_path = root / "docs" / "ops" / "webtropia-deploy.md"

    assert compose_path.exists()
    assert caddyfile_path.exists()
    assert deploy_script_path.exists()
    assert deploy_script_linux.exists()
    assert runbook_path.exists()

    compose_text = compose_path.read_text(encoding="utf-8")
    assert "caddy:" in compose_text
    assert "scheduler:" in compose_text
    assert "postgres:" in compose_text
    assert "redis:" in compose_text
    assert "minio:" in compose_text

    caddyfile_text = caddyfile_path.read_text(encoding="utf-8")
    assert "reverse_proxy web:3000" in caddyfile_text
    assert "reverse_proxy api:8000" in caddyfile_text

    deploy_ps1_text = deploy_script_path.read_text(encoding="utf-8")
    deploy_sh_text = deploy_script_linux.read_text(encoding="utf-8")
    assert "docker-compose.prod.yml" in deploy_ps1_text
    assert "docker-compose.yml" not in deploy_ps1_text
    assert "docker-compose.prod.yml" in deploy_sh_text
    assert "docker-compose.yml" not in deploy_sh_text


def test_webtropia_runbook_documents_dns_tls_and_rollbacks():
    root = Path(__file__).resolve().parents[2]
    runbook_text = (root / "docs" / "ops" / "webtropia-deploy.md").read_text(
        encoding="utf-8"
    )

    assert "Webtropia" in runbook_text
    assert "DNS" in runbook_text
    assert "TLS" in runbook_text
    assert "rollback" in runbook_text.lower()
    assert "docker compose" in runbook_text
