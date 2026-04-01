def build_research_dossier(candidate: dict) -> dict:
    return {
        "topic": candidate.get("title", ""),
        "verified_facts": [candidate.get("summary", "")],
        "claims": candidate.get("claims", []),
        "sources": candidate.get("sources", []),
        "unknowns": [],
    }
