def enqueue_ingest_jobs(active_sources: list[dict], queue) -> int:
    enqueued = 0
    for source in active_sources:
        queue.enqueue("ingest_source", source["id"])
        enqueued += 1
    return enqueued

