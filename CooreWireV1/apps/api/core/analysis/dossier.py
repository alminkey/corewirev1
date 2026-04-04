CLAIM_MARKERS = (
    " says ",
    " warns ",
    " claims ",
    " vowed ",
    " vows ",
    " promised ",
    " promises ",
    " denied ",
    " denies ",
)


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


def _is_claim_like(text: str) -> bool:
    lowered = f" {text.lower()} "
    return any(marker in lowered for marker in CLAIM_MARKERS)


def _is_fact_like_source_title(text: str) -> bool:
    words = [word for word in text.split() if word.strip()]
    return len(words) >= 5 or len(text) >= 40


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
    stakes = _normalize_text_list([candidate.get("why_it_matters", "")])
    valid_sources = [
        source
        for source in candidate.get("sources", [])
        if isinstance(source, dict) and source.get("url")
    ]

    source_signals = _normalize_text_list(
        [source.get("title", "") for source in valid_sources if isinstance(source, dict)]
    )
    source_signals = [
        title
        for title in source_signals
        if _is_fact_like_source_title(title) or _is_claim_like(title)
    ]

    if len(valid_sources) < 2 and "Independent corroboration remains limited." not in unknowns:
        unknowns.append("Independent corroboration remains limited.")

    return {
        "topic": candidate.get("title", ""),
        "verified_facts": verified_facts,
        "claims": claims,
        "source_signals": source_signals,
        "sources": candidate.get("sources", []),
        "stakes": stakes,
        "unknowns": unknowns,
    }
