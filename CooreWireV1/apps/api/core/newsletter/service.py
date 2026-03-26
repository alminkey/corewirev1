def subscribe_newsletter(payload: dict) -> dict:
    email = payload.get("email", "").strip()
    source = payload.get("source", "").strip()

    if not email or "@" not in email:
        raise ValueError("A valid email is required")
    if not source:
        raise ValueError("A source is required")

    return {
        "accepted": True,
        "provider": "beehiiv",
        "list_id": "corewire-main",
        "email": email,
        "source": source,
        "topic_preferences": payload.get("topic_preferences", []),
    }
