from dataclasses import dataclass
import os
from pathlib import Path

from core.config import WorkerSettings
from core.observability.logging import log_worker_event
from core.runtime import run_loop, wait_for_dependencies, write_dead_letter


@dataclass
class WorkerRuntime:
    settings: WorkerSettings
    job_names: list[str]
    startup_log: str


def build_worker() -> WorkerRuntime:
    settings = WorkerSettings()
    return WorkerRuntime(
        settings=settings,
        job_names=["ingest_source", "run_pipeline"],
        startup_log=log_worker_event("worker_startup", queue_name=settings.queue_name),
    )


def run_worker_loop(
    *,
    max_cycles: int | None = None,
    sleep_seconds: float = 5.0,
    wait_for_dependencies=wait_for_dependencies,
    process_once=None,
    dead_letter_path: Path | None = None,
) -> WorkerRuntime:
    runtime = build_worker()

    if process_once is None:
        process_once = lambda: None

    def on_error(exc: Exception) -> None:
        if dead_letter_path is not None:
            write_dead_letter(path=dead_letter_path, job_name="run_pipeline", error=str(exc))

    run_loop(
        max_cycles=max_cycles,
        sleep_seconds=sleep_seconds,
        wait_for_dependencies_fn=wait_for_dependencies,
        process_once=process_once,
        on_error=on_error,
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
    run_worker_loop(
        max_cycles=_read_int_env("COREWIRE_WORKER_MAX_CYCLES"),
        sleep_seconds=_read_float_env("COREWIRE_WORKER_SLEEP_SECONDS", default=5.0),
    )


if __name__ == "__main__":
    main()
