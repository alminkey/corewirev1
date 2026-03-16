from dataclasses import dataclass, field


@dataclass
class WorkerSettings:
    queue_name: str = "corewire-default"
    job_names: list[str] = field(
        default_factory=lambda: ["ingest_source", "run_pipeline"]
    )
