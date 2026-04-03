def _score_thesis(article: dict, doctrine: dict) -> int:
    thesis = str(article.get("thesis") or "").strip()
    if not thesis or "missing_thesis" in doctrine.get("violations", []):
        return 0
    if "generic_thesis" in doctrine.get("violations", []):
        return 1
    if "because" in thesis.lower():
        return 3
    return 2


def _score_why(article: dict, doctrine: dict) -> int:
    body = str(article.get("full_article") or "").lower()
    if "missing_why" in doctrine.get("violations", []):
        return 0
    if "because" in body or "why" in body:
        return 3
    return 2


def _score_new_value(article: dict, doctrine: dict) -> int:
    obscured = [str(item or "").strip() for item in article.get("obscured_layer", []) if str(item or "").strip()]
    stakes = [str(item or "").strip() for item in article.get("stakes", []) if str(item or "").strip()]
    if "missing_new_value" in doctrine.get("violations", []):
        return 0
    if obscured and stakes:
        return 3
    if obscured:
        return 2
    return 1


def _score_actor_map(article: dict, doctrine: dict) -> int:
    actor_map = article.get("actor_map") or []
    if "missing_actor_map" in doctrine.get("violations", []):
        return 0
    if "thin_actor_map" in doctrine.get("violations", []):
        return 1

    strong_actors = 0
    for actor in actor_map:
        if not isinstance(actor, dict):
            continue
        if (
            str(actor.get("goal") or "").strip()
            and str(actor.get("likely_next_move") or "").strip()
        ):
            strong_actors += 1

    if strong_actors >= 2:
        return 3
    if strong_actors >= 1:
        return 2
    return 1


def _score_fact_claim_discipline(article: dict) -> int:
    facts = [item for item in article.get("known_facts", []) if str(item or "").strip()]
    claims = [item for item in article.get("claims", []) if str(item or "").strip()]
    unknowns = [item for item in article.get("unknowns", []) if str(item or "").strip()]
    if not facts:
        return 0
    if facts and claims and unknowns:
        return 3
    if facts and (claims or unknowns):
        return 2
    return 1


def _score_agenda_resistance(doctrine: dict) -> int:
    violations = set(doctrine.get("violations", []))
    if "meta_reader_language" in violations:
        return 1
    if "generic_analysis_language" in violations:
        return 2
    return 3


def _score_tone(doctrine: dict, article: dict) -> int:
    violations = set(doctrine.get("violations", []))
    body = str(article.get("full_article") or "").strip()
    if "generic_analysis_language" in violations:
        return 1
    if len(body) > 1000 and "meta_reader_language" not in violations:
        return 3
    return 2


def score_analysis_output(article: dict, doctrine: dict) -> dict:
    scores = {
        "thesis_strength": _score_thesis(article, doctrine),
        "why_explanation": _score_why(article, doctrine),
        "new_value": _score_new_value(article, doctrine),
        "actor_map_quality": _score_actor_map(article, doctrine),
        "fact_claim_discipline": _score_fact_claim_discipline(article),
        "agenda_resistance": _score_agenda_resistance(doctrine),
        "tone_corewire_identity": _score_tone(doctrine, article),
    }
    core_metrics = (
        "thesis_strength",
        "why_explanation",
        "new_value",
        "actor_map_quality",
        "fact_claim_discipline",
    )
    passed = all(scores[metric] >= 2 for metric in core_metrics) and all(
        scores[metric] > 0 for metric in scores
    )

    if any(scores[metric] == 0 for metric in core_metrics):
        decision = "reject"
    elif not passed:
        decision = "rerun"
    elif doctrine.get("violations"):
        decision = "review"
    else:
        decision = "accept"

    return {
        "scores": scores,
        "passed": passed,
        "decision": decision,
    }
