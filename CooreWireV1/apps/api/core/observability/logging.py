import json
from datetime import UTC, datetime


def log_event(service: str, event: str, **fields) -> str:
    payload = {
        "timestamp": datetime.now(UTC).isoformat(),
        "service": service,
        "event": event,
        **fields,
    }
    return json.dumps(payload, sort_keys=True)
