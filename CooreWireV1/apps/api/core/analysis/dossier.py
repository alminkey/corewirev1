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


def _normalize_text(value: object) -> str:
    return str(value or "").strip()


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

        text = _normalize_text(text)
        if text and text not in normalized:
            normalized.append(text)

    return normalized


def _is_claim_like(text: str) -> bool:
    lowered = f" {text.lower()} "
    return any(marker in lowered for marker in CLAIM_MARKERS)


def _is_fact_like_source_title(text: str) -> bool:
    words = [word for word in text.split() if word.strip()]
    return len(words) >= 5 or len(text) >= 40


def _build_hidden_layers(
    *,
    public_narrative: str,
    real_objective: str,
    timing_pressures: list[str],
    hidden_incentives: list[str],
    obscured_questions: list[str],
) -> list[str]:
    hidden_layers: list[str] = []
    if public_narrative and real_objective:
        hidden_layers.append(
            f"The public argument centers on {public_narrative.rstrip('. ')}, "
            f"but the deeper objective is {real_objective.rstrip('. ')}."
        )

    for value in (*timing_pressures, *hidden_incentives, *obscured_questions):
        text = _normalize_text(value)
        if text and text not in hidden_layers:
            hidden_layers.append(text)

    return hidden_layers


def build_research_dossier(candidate: dict) -> dict:
    verified_facts = []
    summary = _normalize_text(candidate.get("summary"))
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
    public_narrative = _normalize_text(candidate.get("public_narrative"))
    real_objective = _normalize_text(candidate.get("real_objective"))
    timing_pressures = _normalize_text_list(candidate.get("timing_pressures", []))
    hidden_incentives = _normalize_text_list(candidate.get("hidden_incentives", []))
    obscured_questions = _normalize_text_list(candidate.get("obscured_questions", []))
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

    hidden_layers = _build_hidden_layers(
        public_narrative=public_narrative,
        real_objective=real_objective,
        timing_pressures=timing_pressures,
        hidden_incentives=hidden_incentives,
        obscured_questions=obscured_questions,
    )

    return {
        "topic": candidate.get("title", ""),
        "verified_facts": verified_facts,
        "claims": claims,
        "source_signals": source_signals,
        "sources": candidate.get("sources", []),
        "stakes": stakes,
        "unknowns": unknowns,
        "public_narrative": public_narrative,
        "real_objective": real_objective,
        "timing_pressures": timing_pressures,
        "hidden_incentives": hidden_incentives,
        "obscured_questions": obscured_questions,
        "hidden_layers": hidden_layers,
    }
