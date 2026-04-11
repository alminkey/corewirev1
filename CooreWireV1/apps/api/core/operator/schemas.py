from typing import TypedDict


class OperatorCorrelation(TypedDict, total=False):
    ticket_id: str | None
    actor_id: str | None
    company_id: str | None
    correlation_id: str | None
    requested_by: str | None


class OperatorCommand(TypedDict):
    type: str
    payload: dict


# ---------------------------------------------------------------------------
# Paperclip Bridge V1 read response contracts
# ---------------------------------------------------------------------------


class BridgeHealth(TypedDict):
    system: str


class BridgeAutonomy(TypedDict):
    mode: str
    allowed_modes: list[str]
    homepage_auto_publish: bool
    developing_story_auto_publish: bool
    pause_ingest: bool
    pause_publish: bool


class BridgePauseState(TypedDict):
    ingest: bool
    publish: bool


class BridgeQueueCounts(TypedDict):
    review: int
    pending_drafts: int
    low_confidence: int
    flagged_items: int


class BridgePublishedCounts(TypedDict):
    total: int


class BridgeRecentActivityItem(TypedDict):
    type: str
    headline: str
    slug: str
    updated_at: str


class StatusSummaryResponse(TypedDict):
    type: str
    health: BridgeHealth
    autonomy: BridgeAutonomy
    pause_state: BridgePauseState
    queue: BridgeQueueCounts
    published: BridgePublishedCounts
    recent_activity: list[BridgeRecentActivityItem]


class ReviewQueueTotals(TypedDict):
    pending_drafts: int
    low_confidence: int
    flagged_items: int
    review: int


class ReviewQueueItems(TypedDict):
    pending_drafts: list[dict]
    low_confidence: list[dict]
    flagged_items: list[dict]


class ReviewQueueSummaryResponse(TypedDict):
    type: str
    totals: ReviewQueueTotals
    items: ReviewQueueItems


class PublishedRecentItem(TypedDict):
    slug: str
    headline: str
    status: str
    confidence: str
    updated_at: str


class PublishedSummaryResponse(TypedDict):
    type: str
    total: int
    recent: list[PublishedRecentItem]


class AutonomyStateResponse(TypedDict):
    type: str
    mode: str
    allowed_modes: list[str]
    homepage_auto_publish: bool
    developing_story_auto_publish: bool
    pause_ingest: bool
    pause_publish: bool
