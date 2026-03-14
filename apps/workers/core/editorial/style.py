def polish_draft(draft: dict) -> dict:
    fact_text = draft.get("fact_blocks", [{}])[0].get("text", "")
    analysis_text = draft.get("analysis_blocks", [{}])[0].get("text", "")
    analysis_text = analysis_text.replace("Analysis: ", "")

    narrative = " ".join(part for part in [fact_text, analysis_text] if part).strip()

    return {
        **draft,
        "narrative": narrative,
    }
