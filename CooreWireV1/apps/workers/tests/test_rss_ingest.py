from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.ingest.rss import InMemorySourceItemStore, ingest_feed


def test_rss_entry_creates_source_item_once_per_canonical_url():
    store = InMemorySourceItemStore()
    source_id = "source-1"
    entries = [
        {"title": "A", "link": "https://example.com/news/item#section"},
        {"title": "B", "link": "https://example.com/news/item"},
    ]

    inserted_first = ingest_feed(source_id, entries, store)
    inserted_second = ingest_feed(source_id, entries, store)

    assert inserted_first == 1
    assert inserted_second == 0
