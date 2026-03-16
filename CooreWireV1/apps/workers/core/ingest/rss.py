from dataclasses import dataclass
from urllib.parse import urlparse, urlunparse


@dataclass(frozen=True)
class SourceItemCandidate:
    source_id: str
    original_url: str
    canonical_url: str
    title: str | None


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/") or "/"
    return urlunparse((scheme, netloc, path, parsed.params, parsed.query, ""))


def normalize_entries(source_id: str, entries: list[dict]) -> list[SourceItemCandidate]:
    normalized: list[SourceItemCandidate] = []
    for entry in entries:
        url = entry.get("link") or entry.get("url")
        if not url:
            continue
        normalized.append(
            SourceItemCandidate(
                source_id=source_id,
                original_url=url,
                canonical_url=canonicalize_url(url),
                title=entry.get("title"),
            )
        )
    return normalized


class InMemorySourceItemStore:
    def __init__(self):
        self._items: dict[str, SourceItemCandidate] = {}

    def upsert_many(self, items: list[SourceItemCandidate]) -> int:
        inserted = 0
        for item in items:
            if item.canonical_url in self._items:
                continue
            self._items[item.canonical_url] = item
            inserted += 1
        return inserted


def ingest_feed(source_id: str, entries: list[dict], store: InMemorySourceItemStore) -> int:
    candidates = normalize_entries(source_id, entries)
    return store.upsert_many(candidates)

