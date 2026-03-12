from core.config import WorkerSettings
from core.jobs.scheduler import enqueue_ingest_jobs


def build_scheduler() -> dict[str, object]:
    return {
        "settings": WorkerSettings(),
        "entrypoint": enqueue_ingest_jobs,
    }
