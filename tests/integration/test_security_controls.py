from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

from fastapi.testclient import TestClient
import pytest

sys.path.append(str(Path(__file__).resolve().parents[2] / "apps" / "api"))

from app import app


def load_guard_module():
    path = (
        Path(__file__).resolve().parents[2]
        / "apps"
        / "workers"
        / "core"
        / "acquire"
        / "guards.py"
    )
    spec = spec_from_file_location("corewire_worker_guards", path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_internal_publish_route_requires_internal_token():
    client = TestClient(app)

    response = client.post(
        "/internal/publish",
        json={"draft": {"id": "draft-1"}, "confidence": {"level": "high"}},
    )

    assert response.status_code == 401


def test_fetch_guard_rejects_non_allowlisted_domains():
    guard_module = load_guard_module()

    with pytest.raises(ValueError):
        guard_module.validate_fetch_target("http://169.254.169.254/latest/meta-data/")
