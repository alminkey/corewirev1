from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from urllib import request


def post_operator_command(*, api_base_url: str, internal_token: str, command: dict) -> dict:
    payload = json.dumps({"commands": [command]}).encode("utf-8")
    http_request = request.Request(
        f"{api_base_url.rstrip('/')}/operator/commands",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-internal-token": internal_token,
        },
        method="POST",
    )
    with request.urlopen(http_request, timeout=120) as response:
        body = json.loads(response.read().decode("utf-8"))
    return body["results"][0]


def run_content_batch(
    *,
    batch_size: int,
    api_base_url: str,
    internal_token: str,
    output_path: Path | None = None,
    domain: str = "ai-tech-business",
    count: int = 3,
    candidate_index: int = 0,
    length: str = "full_report",
) -> dict:
    results: list[dict] = []

    for _ in range(batch_size):
        command = {
            "type": "run_content_pipeline",
            "payload": {
                "domain": domain,
                "count": count,
                "candidate_index": candidate_index,
                "length": length,
            },
        }
        results.append(
            post_operator_command(
                api_base_url=api_base_url,
                internal_token=internal_token,
                command=command,
            )
        )

    summary = {
        "requested": batch_size,
        "processed": len(results),
        "published_count": sum(
            1 for result in results if result.get("decision", {}).get("action") == "auto_publish"
        ),
        "review_required_count": sum(
            1 for result in results if result.get("decision", {}).get("action") == "review_required"
        ),
        "results": results,
    }

    target_path = output_path or _default_output_path()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def _default_output_path() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return Path("artifacts") / "content-batches" / f"content-batch-{timestamp}.json"


if __name__ == "__main__":
    summary = run_content_batch(
        batch_size=int(os.getenv("COREWIRE_BATCH_SIZE", "10")),
        api_base_url=os.getenv("COREWIRE_API_BASE_URL", "http://localhost:8000/api"),
        internal_token=os.getenv("COREWIRE_INTERNAL_TOKEN", "corewire-internal-token"),
        domain=os.getenv("COREWIRE_CONTENT_DOMAIN", "ai-tech-business"),
    )
    print(json.dumps(summary, indent=2))
