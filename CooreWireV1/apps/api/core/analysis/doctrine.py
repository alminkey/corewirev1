GENERIC_THESIS_MARKERS = (
    "crisis remains complex",
    "tensions are high",
    "growing instability",
    "volatile situation",
)

GENERIC_LANGUAGE_MARKERS = (
    "the situation remains tense",
    "it remains to be seen",
    "tensions remain high",
    "complex situation",
)

META_LANGUAGE_MARKERS = (
    "reader",
    "this article",
    "for the reader",
)


def _has_meaningful_actor_map(actor_map: list[dict]) -> bool:
    meaningful_actors = 0
    for actor in actor_map:
        if not isinstance(actor, dict):
            continue
        goal = str(actor.get("goal") or "").strip()
        likely_next_move = str(actor.get("likely_next_move") or "").strip()
        if goal or likely_next_move:
            meaningful_actors += 1

    return meaningful_actors >= 1


def validate_analysis_doctrine(article: dict) -> dict:
    body = str(article.get("body") or article.get("full_article") or "")
    thesis = str(article.get("thesis") or "")
    body_lower = body.lower()
    thesis_lower = thesis.lower()
    violations = []

    if not thesis.strip():
        violations.append("missing_thesis")
    elif any(marker in thesis_lower for marker in GENERIC_THESIS_MARKERS):
        violations.append("generic_thesis")

    if "because" not in body_lower and "why" not in body_lower:
        violations.append("missing_why")

    actor_map = article.get("actor_map") or []
    if not actor_map:
        violations.append("missing_actor_map")
    elif not _has_meaningful_actor_map(actor_map):
        violations.append("thin_actor_map")

    if not article.get("obscured_layer"):
        violations.append("missing_new_value")

    if any(marker in body_lower for marker in GENERIC_LANGUAGE_MARKERS):
        violations.append("generic_analysis_language")

    if any(marker in body_lower for marker in META_LANGUAGE_MARKERS):
        violations.append("meta_reader_language")

    return {"passed": not violations, "violations": violations}
