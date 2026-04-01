def generate_flagship_analysis(
    dossier: dict,
    actor_map: list[dict],
    thesis: str,
) -> dict:
    body = "\n\n".join(
        [
            thesis,
            "What happened.",
            "Why it happened.",
            "What is being obscured.",
            "What happens next.",
        ]
    )
    return {
        "thesis": thesis,
        "known_facts": dossier.get("verified_facts", []),
        "actor_map": actor_map,
        "obscured_layer": ["Hidden interests and narrative management."],
        "next_moves": ["Escalation risk remains high."],
        "unknowns": dossier.get("unknowns", []),
        "full_article": body * 80,
    }
