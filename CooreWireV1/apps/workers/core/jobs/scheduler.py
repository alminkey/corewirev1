def enqueue_ingest_jobs(active_sources: list[dict], queue) -> int:
    enqueued = 0
    for source in active_sources:
        queue.enqueue("ingest_source", source["id"])
        enqueued += 1
    return enqueued


def enqueue_pipeline_jobs(source_items: list[dict], queue) -> int:
    enqueued = 0
    for source_item in source_items:
        queue.enqueue("run_pipeline", source_item["id"])
        enqueued += 1
    return enqueued

