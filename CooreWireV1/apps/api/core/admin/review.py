def get_review_queue() -> dict:
    return {
        "pending_drafts": [
            {"id": "draft-1", "headline": "Flagship draft awaiting owner review"}
        ],
        "low_confidence": [
            {"id": "story-1", "headline": "Developing story with limited corroboration"}
        ],
        "flagged_items": [
            {"id": "flag-1", "headline": "Story requires compliance review"}
        ],
    }
