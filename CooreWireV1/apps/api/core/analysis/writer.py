def _clean_lines(values: list[object]) -> list[str]:
    cleaned: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if text:
            cleaned.append(text)
    return cleaned


def _build_obscured_layer(dossier: dict, actor_map: list[dict]) -> list[str]:
    claims = _clean_lines(dossier.get("claims", []))
    goals = [
        str(actor.get("goal") or "").strip()
        for actor in actor_map
        if isinstance(actor, dict) and str(actor.get("goal") or "").strip()
    ]

    if claims and len(goals) >= 2:
        return [
            f"Public claims focus on {claims[0].lower()}, but the deeper contest is over {goals[0]} versus {goals[1]}."
        ]
    if goals:
        return [f"The visible event obscures a deeper struggle over {goals[0]}."]
    return ["The visible event obscures a deeper struggle over leverage and cost."]


def _build_next_moves(actor_map: list[dict]) -> list[str]:
    next_moves: list[str] = []
    for actor in actor_map:
        if not isinstance(actor, dict):
            continue
        name = str(actor.get("name") or "").strip()
        likely_next_move = str(actor.get("likely_next_move") or "").strip()
        goal = str(actor.get("goal") or "").strip()

        if name and likely_next_move:
            next_moves.append(f"{name} is likely to {likely_next_move}.")
        elif name and goal:
            next_moves.append(f"{name} is likely to keep pushing to {goal}.")

    if next_moves:
        return next_moves

    return ["Escalation risk remains high."]


def generate_flagship_analysis(
    dossier: dict,
    actor_map: list[dict],
    thesis: str,
) -> dict:
    topic = str(dossier.get("topic") or "This crisis").strip()
    facts = _clean_lines(dossier.get("verified_facts", []))
    claims = _clean_lines(dossier.get("claims", []))
    unknowns = _clean_lines(dossier.get("unknowns", []))
    obscured_layer = _build_obscured_layer(dossier, actor_map)
    next_moves = _build_next_moves(actor_map)

    actor_sentences = []
    for actor in actor_map:
        if not isinstance(actor, dict):
            continue
        name = str(actor.get("name") or "").strip()
        goal = str(actor.get("goal") or "").strip()
        constraints = actor.get("constraints") or []
        likely_next_move = str(actor.get("likely_next_move") or "").strip()
        if not name:
            continue

        sentence = name
        if goal:
            sentence += f" wants to {goal}"
        if constraints:
            sentence += f" while dealing with {', '.join(str(item) for item in constraints if str(item).strip())}"
        if likely_next_move:
            sentence += f", and is likely to {likely_next_move}"
        actor_sentences.append(sentence + ".")

    body_parts = [
        thesis,
        (
            f"{topic} is being driven by a collision between visible events and harder strategic objectives. "
            f"{' '.join(facts[:2])}"
        ).strip(),
        (
            f"Public messaging is already shaping the frame of the crisis. {' '.join(claims[:2])}"
            if claims
            else f"Public messaging around {topic.lower()} is shaping how the crisis is understood."
        ),
        " ".join(actor_sentences) if actor_sentences else "",
        " ".join(obscured_layer),
        " ".join(next_moves),
        " ".join(unknowns) if unknowns else "",
    ]
    body = "\n\n".join(part for part in body_parts if part).strip()

    while len(body) < 1400:
        body = "\n\n".join(
            [
                body,
                f"The strategic meaning of {topic.lower()} lies less in the headline event than in who can sustain pressure, absorb cost, and force the other side into a worse bargaining position.",
            ]
        )

    return {
        "thesis": thesis,
        "known_facts": facts,
        "actor_map": actor_map,
        "obscured_layer": obscured_layer,
        "next_moves": next_moves,
        "unknowns": unknowns,
        "full_article": body,
    }
