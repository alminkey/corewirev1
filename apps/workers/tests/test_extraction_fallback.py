from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.extract.service import acquire_and_extract


class RecordingFetcher:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = 0

    def __call__(self, url: str):
        self.calls += 1
        if self.error is not None:
            raise self.error
        return self.result


def test_browser_fetch_runs_after_failed_simple_extraction():
    http_fetch = RecordingFetcher(error=RuntimeError("http extraction failed"))
    browser_fetch = RecordingFetcher(
        result={"url": "https://example.com/story", "body": "rendered content"}
    )

    result = acquire_and_extract(
        "https://example.com/story",
        http_fetch=http_fetch,
        browser_fetch=browser_fetch,
    )

    assert result["body"] == "rendered content"
    assert http_fetch.calls == 1
    assert browser_fetch.calls == 1
