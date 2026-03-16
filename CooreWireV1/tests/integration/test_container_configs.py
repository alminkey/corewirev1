from pathlib import Path


def test_all_runtime_services_have_dockerfiles_and_prod_compose_entries():
    root = Path(__file__).resolve().parents[2]

    assert (root / "apps" / "api" / "Dockerfile").exists()
    assert (root / "apps" / "workers" / "Dockerfile").exists()
    assert (root / "apps" / "web" / "Dockerfile").exists()
    assert (root / "infra" / "docker" / "docker-compose.prod.yml").exists()
