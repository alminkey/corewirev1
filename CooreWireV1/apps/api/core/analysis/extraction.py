def extract_analysis_sections(article: dict) -> dict:
    fact_blocks = []
    for fact in article.get("known_facts", []):
        text = str(fact or "").strip()
        if text:
            fact_blocks.append({"text": text, "citations": []})

    analysis_blocks = []
    for value in article.get("stakes", []):
        text = str(value or "").strip()
        if text:
            analysis_blocks.append({"text": text})
    for value in article.get("obscured_layer", []):
        text = str(value or "").strip()
        if text:
            analysis_blocks.append({"text": text})
    for value in article.get("next_moves", []):
        text = str(value or "").strip()
        if text:
            analysis_blocks.append({"text": text})

    disagreements = [
        text
        for text in (
            str(value or "").strip()
            for value in article.get("unknowns", [])
        )
        if text
    ]

    if not analysis_blocks:
        full_article = str(article.get("full_article", "") or "").strip()
        if full_article:
            analysis_blocks.append({"text": full_article[:500]})

    return {
        "fact_blocks": fact_blocks,
        "analysis_blocks": analysis_blocks,
        "disagreements": disagreements,
    }
