def extract_analysis_sections(article: dict) -> dict:
    return {
        "fact_blocks": [
            {"text": fact, "citations": []}
            for fact in article.get("known_facts", [])
        ],
        "analysis_blocks": [{"text": article.get("full_article", "")[:500]}],
        "disagreements": article.get("unknowns", []),
    }
