import os

from core.config import WorkerSettings
from core.jobs.scheduler import enqueue_ingest_jobs
from core.runtime import run_loop, wait_for_dependencies


def build_scheduler() -> dict[str, object]:
    return {
        "settings": WorkerSettings(),
        "entrypoint": enqueue_ingest_jobs,
    }


def run_scheduler_loop(
    *,
    max_cycles: int | None = None,
    sleep_seconds: float = 30.0,
    wait_for_dependencies=wait_for_dependencies,
    schedule_once=None,
) -> dict[str, object]:
    runtime = build_scheduler()

    if schedule_once is None:
        schedule_once = lambda: None

    run_loop(
        max_cycles=max_cycles,
        sleep_seconds=sleep_seconds,
        wait_for_dependencies_fn=wait_for_dependencies,
        process_once=schedule_once,
        on_error=None,
    )
    return runtime


def _read_int_env(name: str) -> int | None:
    raw_value = os.getenv(name, "").strip()
    if not raw_value:
        return None
    return int(raw_value)


def _read_float_env(name: str, *, default: float) -> float:
    raw_value = os.getenv(name, "").strip()
    if not raw_value:
        return default
    return float(raw_value)


def main() -> None:
    run_scheduler_loop(
        max_cycles=_read_int_env("COREWIRE_SCHEDULER_MAX_CYCLES"),
        sleep_seconds=_read_float_env("COREWIRE_SCHEDULER_SLEEP_SECONDS", default=30.0),
    )


if __name__ == "__main__":
    main()
