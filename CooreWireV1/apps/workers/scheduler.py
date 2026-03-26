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
