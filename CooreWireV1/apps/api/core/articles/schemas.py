from typing import TypedDict


class StoryCard(TypedDict):
    slug: str
    headline: str
    status: str
    confidence: str
    source_count: int
    updated_at: str
    dek: str
    story_tier: str
    requested_profile: str
    effective_profile: str


class ArticleSource(TypedDict):
    label: str
    publisher: str | None
    title: str | None
    url: str | None
    role: str


class ArticleDetail(StoryCard):
    facts: list[dict]
    analysis: list[str]
    disagreements: list[str]
    sources: list[ArticleSource]

