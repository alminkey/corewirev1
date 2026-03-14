def assess_prose_quality(draft: dict) -> dict:
    narrative = draft.get("narrative", "")
    narrative_lower = narrative.lower()
    issues: list[str] = []

    if narrative_lower.count("in today's world") > 1:
        issues.append("repeated_filler")
    if "meanwhile" in narrative_lower:
        issues.append("unsupported_transition")
    if narrative_lower.count("this happened") >= 2:
        issues.append("thin_summary_prose")

    return {
        "valid": not issues,
        "issues": issues,
    }
