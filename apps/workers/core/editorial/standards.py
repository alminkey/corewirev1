def validate_standards(draft: dict) -> dict:
    issues: list[str] = []

    if not draft.get("fact_blocks"):
        issues.append("missing_fact_blocks")
    if not draft.get("analysis_blocks"):
        issues.append("missing_analysis_blocks")
    if not draft.get("narrative"):
        issues.append("missing_narrative")

    return {
        "valid": not issues,
        "issues": issues,
    }
