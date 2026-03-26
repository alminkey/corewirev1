from pathlib import Path
import json
import sys
import uuid

sys.path.append(str(Path(__file__).resolve().parents[1]))

from main import run_worker_loop
from scheduler import run_scheduler_loop


def test_worker_loop_waits_for_dependencies_and_processes_one_cycle():
    state = {"ready_calls": 0, "job_calls": 0}
    dead_letter_path = Path(__file__).resolve().parents[3] / f"dead-letter-{uuid.uuid4().hex}.jsonl"

    try:
        def fake_wait_for_dependencies(*, max_attempts: int, delay_seconds: float) -> None:
            state["ready_calls"] += 1
            assert max_attempts >= 1

        def fake_process_once() -> None:
            state["job_calls"] += 1

        run_worker_loop(
            max_cycles=1,
            sleep_seconds=0,
            wait_for_dependencies=fake_wait_for_dependencies,
            process_once=fake_process_once,
            dead_letter_path=dead_letter_path,
        )

        assert state["ready_calls"] == 1
        assert state["job_calls"] == 1
        assert not dead_letter_path.exists()
    finally:
        if dead_letter_path.exists():
            dead_letter_path.unlink()


def test_worker_loop_writes_dead_letter_after_unhandled_failure():
    dead_letter_path = Path(__file__).resolve().parents[3] / f"dead-letter-{uuid.uuid4().hex}.jsonl"

    try:
        def fake_wait_for_dependencies(*, max_attempts: int, delay_seconds: float) -> None:
            return None

        def fake_process_once() -> None:
            raise RuntimeError("pipeline failed")

        run_worker_loop(
            max_cycles=1,
            sleep_seconds=0,
            wait_for_dependencies=fake_wait_for_dependencies,
            process_once=fake_process_once,
            dead_letter_path=dead_letter_path,
        )

        payload = json.loads(dead_letter_path.read_text(encoding="utf-8").strip())
        assert payload["job_name"] == "run_pipeline"
        assert payload["error"] == "pipeline failed"
    finally:
        if dead_letter_path.exists():
            dead_letter_path.unlink()


def test_scheduler_loop_waits_for_dependencies_and_runs_one_cycle():
    state = {"ready_calls": 0, "enqueue_calls": 0}

    def fake_wait_for_dependencies(*, max_attempts: int, delay_seconds: float) -> None:
        state["ready_calls"] += 1

    def fake_schedule_once() -> None:
        state["enqueue_calls"] += 1

    run_scheduler_loop(
        max_cycles=1,
        sleep_seconds=0,
        wait_for_dependencies=fake_wait_for_dependencies,
        schedule_once=fake_schedule_once,
    )

    assert state["ready_calls"] == 1
    assert state["enqueue_calls"] == 1
