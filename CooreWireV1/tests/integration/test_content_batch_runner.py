from pathlib import Path
import json
import sys
import uuid

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from content_batch_runner import run_content_batch


def test_run_content_batch_writes_summary_and_counts_results(monkeypatch):
    output_path = ROOT / f"content-batch-{uuid.uuid4().hex}.json"
    calls: list[dict] = []

    responses = [
        {
            "type": "run_content_pipeline",
            "accepted": True,
            "selected_candidate": {"title": "Story One"},
            "decision": {"action": "auto_publish", "reasons": []},
            "article": {"slug": "story-one", "status": "published"},
        },
        {
            "type": "run_content_pipeline",
            "accepted": True,
            "selected_candidate": {"title": "Story Two"},
            "decision": {"action": "review_required", "reasons": ["medium_confidence"]},
            "review_item": {"id": "draft-2", "queue": "pending_drafts"},
        },
    ]

    def fake_post_operator_command(*, api_base_url: str, internal_token: str, command: dict) -> dict:
        calls.append(command)
        return responses[len(calls) - 1]

    monkeypatch.setattr("content_batch_runner.post_operator_command", fake_post_operator_command)

    try:
        summary = run_content_batch(
            batch_size=2,
            api_base_url="http://localhost:8000/api",
            internal_token="corewire-internal-token",
            output_path=output_path,
            domain="ai-tech-business",
        )

        assert summary["requested"] == 2
        assert summary["processed"] == 2
        assert summary["published_count"] == 1
        assert summary["review_required_count"] == 1
        assert calls[0]["type"] == "run_content_pipeline"
        assert calls[0]["payload"]["domain"] == "ai-tech-business"

        written = json.loads(output_path.read_text(encoding="utf-8"))
        assert written["results"][0]["selected_candidate"]["title"] == "Story One"
        assert written["results"][1]["decision"]["action"] == "review_required"
    finally:
        if output_path.exists():
            output_path.unlink()
