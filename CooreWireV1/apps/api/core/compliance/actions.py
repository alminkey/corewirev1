ACTION_STATUS_MAP = {
    "approve": "published",
    "reject": "rejected",
    "retract": "retracted",
    "correct": "corrected",
    "supersede": "superseded",
}


def apply_article_action(article: dict, action: str, actor: str) -> dict:
    status = ACTION_STATUS_MAP[action]
    return {
        **article,
        "status": status,
        "audit": {
            "actor": actor,
            "action": action,
        },
    }
