from dataclasses import dataclass

from core.config import WorkerSettings
from core.observability.logging import log_worker_event


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
