from pathlib import Path
import sys

workers_path = str(Path(__file__).resolve().parents[2] / "apps" / "workers")
sys.path.insert(0, workers_path)
for module_name in list(sys.modules):
    if module_name == "core" or module_name.startswith("core."):
        del sys.modules[module_name]

from core.jobs.pipeline import run_pipeline
from core.jobs.scheduler import enqueue_pipeline_jobs


class RecordingQueue:
    def __init__(self):
        self.calls = []

    def enqueue(self, job_name: str, source_item_id: str):
        self.calls.append((job_name, source_item_id))
        return source_item_id


def test_scheduler_enqueues_and_worker_advances_story_to_publish_state():
    queue = RecordingQueue()
    source_items = [{"id": "source-item-1"}]
    document = {
        "id": "doc-1",
        "body_text": "CoreWire launched the pipeline on Tuesday.",
        "source_id": "source-1",
        "slug": "corewire-launched-the-pipeline",
    }
    related_documents = [
        {
            "id": "doc-2",
            "body_text": "CoreWire launched the pipeline on Tuesday.",
            "source_id": "source-2",
        }
    ]

    enqueued = enqueue_pipeline_jobs(source_items, queue)
    result = run_pipeline(
        "source-item-1",
        document=document,
        related_documents=related_documents,
    )

    assert enqueued == 1
    assert queue.calls == [("run_pipeline", "source-item-1")]
    assert result["status"] == "published"
    assert result["homepage_eligible"] is True
    assert result["audit_event"]["status"] == "published"
