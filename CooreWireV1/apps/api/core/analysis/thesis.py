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


def _thesis_actor_label(name: str) -> str:
    normalized = name.strip()
    aliases = {
        "United States": "the U.S.",
    }
    return aliases.get(normalized, normalized)


def _goal_argument_phrase(goal: str) -> str:
    text = goal.strip()
    if not text:
        return "effort to shift the balance"

    verb = text.split(maxsplit=1)[0].lower()
    if verb == "raise":
        return f"bid to {text}"
    if verb == "force":
        return f"drive to {text}"
    return f"effort to {text}"


def _actor_argument(name: str, goal: str) -> str:
    label = _thesis_actor_label(name)
    if label.startswith("the "):
        return f"{label} {_goal_argument_phrase(goal)}"
    return f"{label}'s {_goal_argument_phrase(goal)}"


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
            f"{subject} is escalating because the real contest is now between "
            f"{_actor_argument(name_one, goal_one)} and {_actor_argument(name_two, goal_two)}."
        )

    if actors:
        name, goal = actors[0]
        return (
            f"{subject} matters because the real contest is now about "
            f"{_actor_argument(name, goal)}."
        )

    return f"{subject} matters because the visible event masks a deeper struggle over leverage."
