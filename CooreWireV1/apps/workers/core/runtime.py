from __future__ import annotations

import json
import os
import socket
import time
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse


def wait_for_dependencies(*, max_attempts: int = 10, delay_seconds: float = 1.0) -> None:
    database_url = os.getenv("COREWIRE_DATABASE_URL", "")
    redis_url = os.getenv("COREWIRE_REDIS_URL", "redis://localhost:6379/0")

    for attempt in range(1, max_attempts + 1):
        db_ready = not database_url or _check_database_ready(database_url)
        redis_ready = _check_redis_ready(redis_url)
        if db_ready and redis_ready:
            return
        if attempt < max_attempts:
            time.sleep(delay_seconds)

    raise RuntimeError("Worker dependencies are not ready")


def write_dead_letter(*, path: Path, job_name: str, error: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"job_name": job_name, "error": error}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _check_database_ready(database_url: str) -> bool:
    parsed = urlparse(database_url)
    if parsed.scheme.startswith("sqlite"):
        return True
    if not parsed.hostname or not parsed.port:
        return False
    return _can_connect(parsed.hostname, parsed.port)


def _check_redis_ready(redis_url: str) -> bool:
    parsed = urlparse(redis_url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 6379
    return _can_connect(host, port)


def _can_connect(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False


def run_loop(
    *,
    max_cycles: int | None,
    sleep_seconds: float,
    wait_for_dependencies_fn: Callable[..., None],
    process_once: Callable[[], None],
    on_error: Callable[[Exception], None] | None = None,
) -> None:
    wait_for_dependencies_fn(max_attempts=10, delay_seconds=1.0)

    cycles = 0
    while max_cycles is None or cycles < max_cycles:
        try:
            process_once()
        except Exception as exc:  # pragma: no cover - covered through callback assertions
            if on_error is not None:
                on_error(exc)
        cycles += 1
        if max_cycles is None or cycles < max_cycles:
            time.sleep(sleep_seconds)
