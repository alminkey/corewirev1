def score_confidence(evidence_bundle: dict) -> dict:
    evidence = evidence_bundle.get("evidence", [])
    source_ids = {item.get("source_id") for item in evidence if item.get("source_id")}
    supports = sum(1 for item in evidence if item.get("relation_type") == "supports")

    if len(source_ids) < 2 or supports < 2:
        return {"level": "low", "homepage_eligible": False}

    return {"level": "high", "homepage_eligible": True}

