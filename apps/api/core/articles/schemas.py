from typing import TypedDict


class StoryCard(TypedDict):
    slug: str
    headline: str
    status: str
    confidence: str
    source_count: int
    updated_at: str
    dek: str


class ArticleDetail(StoryCard):
    facts: list[dict]
    analysis: list[str]
    disagreements: list[str]
    sources: list[str]

