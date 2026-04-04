def _thesis_subject(topic: str) -> str:
    cleaned = topic.strip()
    if not cleaned:
        return "This crisis"

    words = cleaned.split()
    if len(words) > 12 or " because " in cleaned.lower():
        return "The crisis"
    if cleaned.lower().startswith(("the ", "this ")):
        return cleaned
    return cleaned


def form_analysis_thesis(dossier: dict, actor_map: list[dict]) -> str:
    topic = str(dossier.get("topic") or "This crisis").strip()
    subject = _thesis_subject(topic)
    actors = [
        (
            str(actor.get("name") or "").strip(),
            str(actor.get("goal") or "").strip(),
        )
        for actor in actor_map
        if isinstance(actor, dict) and str(actor.get("goal") or "").strip()
    ]

    if len(actors) >= 2:
        name_one, goal_one = actors[0]
        name_two, goal_two = actors[1]
        return (
            f"{subject} is escalating because {name_one} wants to {goal_one} "
            f"while {name_two} is trying to {goal_two}."
        )

    if actors:
        name, goal = actors[0]
        return f"{subject} matters because {name} wants to {goal}."

    return f"{subject} matters because the visible event masks a deeper struggle over leverage."
