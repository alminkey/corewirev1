from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from main import build_worker


def test_worker_loads_config_and_registers_pipeline_jobs():
    worker = build_worker()

    assert "ingest_source" in worker.job_names
    assert "run_pipeline" in worker.job_names
