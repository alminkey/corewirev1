from datetime import UTC, datetime


def record_pipeline_event(run_type: str, target_id: str, status: str) -> dict:
    return {
        "run_type": run_type,
        "target_id": target_id,
        "status": status,
        "recorded_at": datetime.now(UTC).isoformat(),
    }

