def render_metrics() -> str:
    lines = [
        "# HELP corewire_http_requests_total Total HTTP requests served by CoreWire",
        "# TYPE corewire_http_requests_total counter",
        "corewire_http_requests_total 1",
        "# HELP corewire_pipeline_runs_total Total pipeline runs observed by CoreWire",
        "# TYPE corewire_pipeline_runs_total counter",
        "corewire_pipeline_runs_total 1",
    ]
    return "\n".join(lines)
