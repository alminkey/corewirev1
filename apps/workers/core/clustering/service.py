import re


def _normalize_words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def assign_story_clusters(claims: list[dict]) -> list[dict]:
    cluster_index = 1
    assigned: list[dict] = []
    seen_clusters: list[tuple[str, set[str]]] = []

    for claim in claims:
        claim_words = _normalize_words(claim.get("claim_text", ""))
        cluster_id = None
        for existing_cluster_id, existing_words in seen_clusters:
            if claim_words & existing_words:
                cluster_id = existing_cluster_id
                break
        if cluster_id is None:
            cluster_id = f"cluster-{cluster_index}"
            cluster_index += 1
            seen_clusters.append((cluster_id, claim_words))
        assigned.append({**claim, "story_cluster_id": cluster_id})

    return assigned

