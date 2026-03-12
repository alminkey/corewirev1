from dataclasses import dataclass

from core.config import WorkerSettings


@dataclass
class WorkerRuntime:
    settings: WorkerSettings
    job_names: list[str]


def build_worker() -> WorkerRuntime:
    settings = WorkerSettings()
    return WorkerRuntime(
        settings=settings,
        job_names=["ingest_source", "run_pipeline"],
    )
