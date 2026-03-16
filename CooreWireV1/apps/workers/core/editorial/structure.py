def build_structure(analysis: dict) -> dict:
    verified_facts = analysis.get("verified_facts", [])
    why_analysis = analysis.get("why_analysis", "")

    headline = verified_facts[0] if verified_facts else "CoreWire update"

    return {
        "headline": headline,
        "sections": [
            {"label": "What Happened", "content": verified_facts},
            {"label": "Why It Matters", "content": [why_analysis]},
        ],
    }
