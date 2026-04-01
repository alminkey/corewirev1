def validate_analysis_doctrine(article: dict) -> dict:
    body = article.get("body") or article.get("full_article") or ""
    violations = []

    if not article.get("thesis"):
        violations.append("missing_thesis")
    if "because" not in body.lower() and "why" not in body.lower():
        violations.append("missing_why")
    if not article.get("actor_map"):
        violations.append("missing_actor_map")
    if not article.get("obscured_layer"):
        violations.append("missing_new_value")
    if "reader" in body.lower():
        violations.append("meta_reader_language")

    return {"passed": not violations, "violations": violations}
