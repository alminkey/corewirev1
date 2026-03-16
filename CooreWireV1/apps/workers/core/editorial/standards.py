from core.editorial.quality import assess_prose_quality


def validate_standards(draft: dict) -> dict:
    issues: list[str] = []

    if not draft.get("fact_blocks"):
        issues.append("missing_fact_blocks")
    if not draft.get("analysis_blocks"):
        issues.append("missing_analysis_blocks")
    if not draft.get("narrative"):
        issues.append("missing_narrative")

    quality = assess_prose_quality(draft)
    issues.extend(issue for issue in quality["issues"] if issue not in issues)

    return {
        "valid": not issues,
        "issues": issues,
    }
