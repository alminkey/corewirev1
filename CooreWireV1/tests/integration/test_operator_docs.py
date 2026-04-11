from pathlib import Path


def test_paperclip_bridge_doc_covers_commands_callbacks_auth_and_ticket_correlation():
    doc_path = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "ops"
        / "paperclip-bridge.md"
    )

    assert doc_path.exists()

    contents = doc_path.read_text(encoding="utf-8")

    assert "operator command schema" in contents.lower()
    assert "callback schema" in contents.lower()
    assert "auth model" in contents.lower()
    assert "ticket correlation model" in contents.lower()


def test_paperclip_bridge_docs_cover_read_endpoints_http_adapter_and_auth():
    bridge_doc = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "ops"
        / "paperclip-bridge.md"
    )
    adapter_doc = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "runbooks"
        / "paperclip-http-adapter.md"
    )

    assert bridge_doc.exists(), "docs/ops/paperclip-bridge.md must exist"
    assert adapter_doc.exists(), "docs/runbooks/paperclip-http-adapter.md must exist"

    bridge_contents = bridge_doc.read_text(encoding="utf-8")
    adapter_contents = adapter_doc.read_text(encoding="utf-8")

    # Bridge doc must cover V1 read endpoints
    assert "/operator/bridge/status" in bridge_contents
    assert "/operator/bridge/review-queue" in bridge_contents
    assert "/operator/bridge/published" in bridge_contents
    assert "/operator/bridge/autonomy" in bridge_contents

    # Adapter runbook must cover setup, auth, and correlation
    assert "x-internal-token" in adapter_contents.lower()
    assert "http adapter" in adapter_contents.lower()
    assert "requested_by" in adapter_contents
