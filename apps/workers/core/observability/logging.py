import json
from datetime import UTC, datetime


def log_worker_event(event: str, **fields) -> str:
    payload = {
        "timestamp": datetime.now(UTC).isoformat(),
        "service": "corewire-workers",
        "event": event,
        **fields,
    }
    return json.dumps(payload, sort_keys=True)
