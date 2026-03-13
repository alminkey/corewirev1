from pathlib import Path


def test_k8s_manifests_define_web_api_and_worker_deployments():
    root = Path(__file__).resolve().parents[2]

    assert (root / "infra" / "k8s" / "namespace.yaml").exists()
    assert (root / "infra" / "k8s" / "api-deployment.yaml").exists()
    assert (root / "infra" / "k8s" / "web-deployment.yaml").exists()
    assert (root / "infra" / "k8s" / "workers-deployment.yaml").exists()
    assert (root / "infra" / "k8s" / "ingress.yaml").exists()
