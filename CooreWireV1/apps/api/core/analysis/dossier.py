def _normalize_text_list(values: list[object]) -> list[str]:
    normalized: list[str] = []
    for value in values:
        text = ""
        if isinstance(value, str):
            text = value
        elif isinstance(value, dict):
            text = (
                value.get("text")
                or value.get("claim")
                or value.get("statement")
                or ""
            )

        text = str(text).strip()
        if text and text not in normalized:
            normalized.append(text)

    return normalized


def build_research_dossier(candidate: dict) -> dict:
    verified_facts = []
    summary = str(candidate.get("summary") or "").strip()
    if summary:
        verified_facts.append(summary)
    verified_facts.extend(
        fact
        for fact in _normalize_text_list(candidate.get("verified_facts", []))
        if fact not in verified_facts
    )

    claims = _normalize_text_list(candidate.get("claims", []))
    unknowns = _normalize_text_list(candidate.get("unknowns", []))
    valid_sources = [
        source
        for source in candidate.get("sources", [])
        if isinstance(source, dict) and source.get("url")
    ]
    if len(valid_sources) < 2 and "Independent corroboration remains limited." not in unknowns:
        unknowns.append("Independent corroboration remains limited.")

    return {
        "topic": candidate.get("title", ""),
        "verified_facts": verified_facts,
        "claims": claims,
        "sources": candidate.get("sources", []),
        "unknowns": unknowns,
    }
