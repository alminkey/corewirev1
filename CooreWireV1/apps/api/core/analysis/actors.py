def _infer_likely_next_move(name: str, topic: str, goal: str) -> str:
    name_lower = name.lower()
    topic_lower = topic.lower()
    goal_lower = goal.lower()

    if "iran" in name_lower and ("shipping" in goal_lower or "hormuz" in topic_lower):
        return "keep using maritime pressure to raise costs"
    if ("united states" in name_lower or "america" in name_lower) and (
        "concession" in goal_lower or "pressure" in goal_lower
    ):
        return "increase military and diplomatic pressure"
    if "israel" in name_lower:
        return "push to extend the military phase"
    if any(marker in name_lower for marker in ("bahrain", "gulf", "saudi", "emirates", "uae")):
        return "press for shipping security without a blank-check war mandate"
    if "china" in name_lower or "russia" in name_lower:
        return "use diplomatic channels to block a wider mandate"
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
            or _infer_likely_next_move(
                str(actor.get("name") or "").strip(),
                topic,
                str(actor.get("goal") or "").strip(),
            ),
        }
        for actor in actors
    ]
