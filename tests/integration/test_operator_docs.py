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
