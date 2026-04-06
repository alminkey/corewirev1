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

MIN_FLAGSHIP_BODY_CHARS = 1200
MIN_HIDDEN_LAYER_ITEMS = 2
MIN_HIDDEN_LAYER_CHARS = 160
MIN_CONSEQUENCE_SIGNALS = 2
CONTRADICTION_MARKERS = (
    "deeper fight",
    "deeper contest",
    "contradiction underneath",
    "public case is about",
)
WHY_NOW_MARKERS = (
    "timing is not incidental",
    "timing matters because",
    "racing against",
)
BURIED_CONSEQUENCE_MARKERS = (
    "buried consequence",
    "first real fracture",
    "easier to miss than the headline event",
)
HARD_ENDING_MARKERS = (
    "hardest pressure point",
    "until that pressure breaks",
    "pressure point is now becoming unavoidable",
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


def _clean_lines(values: list[object]) -> list[str]:
    cleaned: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if text:
            cleaned.append(text)
    return cleaned


def _has_sufficient_hidden_layer(obscured_layer: list[object]) -> bool:
    hidden = _clean_lines(obscured_layer)
    if len(hidden) < MIN_HIDDEN_LAYER_ITEMS:
        return False
    return sum(len(item) for item in hidden) >= MIN_HIDDEN_LAYER_CHARS


def _has_sufficient_consequence_layer(article: dict) -> bool:
    stakes = _clean_lines(article.get("stakes") or [])
    next_moves = _clean_lines(article.get("next_moves") or [])
    return len(stakes) + len(next_moves) >= MIN_CONSEQUENCE_SIGNALS


def _contains_any_marker(text: str, markers: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in markers)


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
    elif not _has_sufficient_hidden_layer(article.get("obscured_layer") or []):
        violations.append("thin_hidden_layer")

    if len(body.strip()) < MIN_FLAGSHIP_BODY_CHARS:
        violations.append("thin_full_article")

    if not _has_sufficient_consequence_layer(article):
        violations.append("thin_consequence_layer")

    if not _contains_any_marker(body, CONTRADICTION_MARKERS):
        violations.append("weak_core_contradiction")

    if not _contains_any_marker(body, WHY_NOW_MARKERS):
        violations.append("weak_why_now")

    if not _contains_any_marker(body, BURIED_CONSEQUENCE_MARKERS):
        violations.append("weak_buried_consequence")

    if not _contains_any_marker(body, HARD_ENDING_MARKERS):
        violations.append("weak_hard_ending")

    if any(marker in body_lower for marker in GENERIC_LANGUAGE_MARKERS):
        violations.append("generic_analysis_language")

    if any(marker in body_lower for marker in META_LANGUAGE_MARKERS):
        violations.append("meta_reader_language")

    return {"passed": not violations, "violations": violations}
