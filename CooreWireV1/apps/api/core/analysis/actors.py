def _infer_likely_next_move(topic: str, goal: str) -> str:
    topic_lower = topic.lower()
    goal_lower = goal.lower()

    if "shipping" in goal_lower or "hormuz" in topic_lower:
        return "maintain pressure on maritime flows"
    if "concession" in goal_lower or "pressure" in goal_lower:
        return "increase coercive pressure"
    if goal:
        return f"keep pushing to {goal}"
    return ""


def build_actor_map(dossier: dict, actors: list[dict]) -> list[dict]:
    topic = str(dossier.get("topic") or "").strip()
    return [
        {
            "name": actor["name"],
            "goal": actor.get("goal", ""),
            "constraints": actor.get("constraints", []),
            "currently_benefits": actor.get("current_advantages", []),
            "currently_pressures": actor.get("current_pressures", []),
            "likely_next_move": actor.get("likely_next_move", "")
            or _infer_likely_next_move(topic, str(actor.get("goal") or "").strip()),
        }
        for actor in actors
    ]
