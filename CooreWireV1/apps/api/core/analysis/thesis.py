def form_analysis_thesis(dossier: dict, actor_map: list[dict]) -> str:
    topic = str(dossier.get("topic") or "This crisis").strip()
    goals = [
        str(actor.get("goal") or "").strip()
        for actor in actor_map
        if isinstance(actor, dict) and str(actor.get("goal") or "").strip()
    ]

    if len(goals) >= 2:
        return (
            f"{topic} is escalating because {goals[0]} now collides directly with "
            f"{goals[1]}."
        )

    if goals:
        return f"{topic} matters because the struggle is now centered on {goals[0]}."

    return f"{topic} matters because the visible event masks a deeper struggle over leverage."
