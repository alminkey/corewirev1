def match_evidence(claim: dict, related_documents: list[dict]) -> list[dict]:
    claim_text = claim.get("claim_text", "")
    evidence = []

    for document in related_documents:
        body_text = document.get("body_text", "")
        relation_type = "context"
        if body_text == claim_text:
            relation_type = "supports"
        elif "did not" in body_text.lower():
            relation_type = "contradicts"

        evidence.append(
            {
                "relation_type": relation_type,
                "evidence_quote": body_text,
            }
        )

    return evidence

