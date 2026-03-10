def extract_claims(document: dict) -> list[dict]:
    body_text = (document.get("body_text") or "").strip()
    if not body_text:
        return []

    return [
        {
            "claim_text": body_text,
            "supporting_quote": body_text,
            "claim_type": "statement",
        }
    ]

