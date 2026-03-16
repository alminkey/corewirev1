from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.jobs.scheduler import enqueue_ingest_jobs


class RecordingQueue:
    def __init__(self):
        self.calls = []

    def enqueue(self, job_name: str, source_id: str):
        self.calls.append((job_name, source_id))
        return source_id


def test_scheduler_enqueues_ingest_jobs_for_active_sources():
    queue = RecordingQueue()
    active_sources = [{"id": "source-1"}, {"id": "source-2"}]

    enqueued = enqueue_ingest_jobs(active_sources, queue)

    assert enqueued == 2
    assert queue.calls == [
        ("ingest_source", "source-1"),
        ("ingest_source", "source-2"),
    ]
