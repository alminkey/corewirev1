def build_draft(analysis: dict) -> dict:
    verified_facts = analysis.get("verified_facts", [])
    why_analysis = analysis.get("why_analysis", "")

    fact_blocks = [
        {"text": fact, "citations": [{"source": "source-placeholder"}]}
        for fact in verified_facts
    ]

    return {
        "fact_blocks": fact_blocks,
        "analysis_blocks": [{"text": why_analysis}],
    }

