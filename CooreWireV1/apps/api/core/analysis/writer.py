def _clean_lines(values: list[object]) -> list[str]:
    cleaned: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if text:
            cleaned.append(text)
    return cleaned


def _join_names(names: list[str]) -> str:
    cleaned = [name for name in names if name]
    if not cleaned:
        return ""
    if len(cleaned) == 1:
        return cleaned[0]
    if len(cleaned) == 2:
        return f"{cleaned[0]} and {cleaned[1]}"
    return f"{', '.join(cleaned[:-1])}, and {cleaned[-1]}"


def _subject_verb(subject: str) -> str:
    lowered = subject.lower()
    if lowered == "united states":
        return "is"
    if " and " in lowered or lowered.endswith("states"):
        return "are"
    return "is"


def _is_plural_subject(subject: str) -> bool:
    return _subject_verb(subject) == "are"


def _subject_pronoun(subject: str) -> str:
    return "they" if _is_plural_subject(subject) else "it"


def _subject_possessive(subject: str) -> str:
    return "their" if _is_plural_subject(subject) else "its"


def _goal_as_activity(goal: str) -> str:
    known_verbs = {
        "force",
        "degrade",
        "raise",
        "restore",
        "prevent",
        "keep",
        "slow",
        "change",
        "reduce",
        "expand",
        "block",
        "stabilize",
    }

    def _verb_to_ing(verb: str) -> str:
        lowered = verb.lower()
        irregular = {
            "force": "forcing",
            "degrade": "degrading",
            "raise": "raising",
            "restore": "restoring",
            "prevent": "preventing",
            "keep": "keeping",
            "slow": "slowing",
        }
        verb_form = irregular.get(lowered)
        if verb_form is None:
            if lowered.endswith("e") and len(lowered) > 2:
                verb_form = f"{lowered[:-1]}ing"
            else:
                verb_form = f"{lowered}ing"
        return verb_form

    text = str(goal or "").strip()
    if not text:
        return "changing the balance"

    segments = []
    for segment in text.split(" and "):
        words = segment.split(maxsplit=1)
        verb = words[0]
        rest = words[1] if len(words) > 1 else ""
        if verb.lower() in known_verbs:
            segments.append(f"{_verb_to_ing(verb)} {rest}".strip())
        else:
            segments.append(segment.strip())

    return " and ".join(segments)


def _topic_subject(topic: str) -> str:
    cleaned = str(topic or "").strip()
    if not cleaned:
        return "The crisis"

    words = cleaned.split()
    if len(words) > 12 or " because " in cleaned.lower():
        return "The crisis"
    return cleaned


def _build_lead_paragraph(topic_subject: str, facts: list[str]) -> str:
    fact_text = " ".join(facts[:2]).strip()
    subject = topic_subject
    if topic_subject.lower().startswith("the "):
        subject = topic_subject[0].lower() + topic_subject[1:]
    lead = f"At its core, {subject} is no longer just about the latest exchange."
    if fact_text:
        return f"{lead} {fact_text}"
    return lead


def _build_obscured_layer(dossier: dict, actor_map: list[dict]) -> list[str]:
    claims = _clean_lines(dossier.get("claims", []))
    actor_goals = [
        (
            str(actor.get("name") or "").strip(),
            str(actor.get("goal") or "").strip(),
        )
        for actor in actor_map
        if isinstance(actor, dict) and str(actor.get("goal") or "").strip()
    ]

    if claims and len(actor_goals) >= 2:
        actor_one, goal_one = actor_goals[0]
        actor_two, goal_two = actor_goals[1]
        return [
            f"Behind the public language, the deeper contest is over whether {actor_one} can {goal_one} "
            f"before {actor_two} can {goal_two}."
        ]
    if actor_goals:
        actor, goal = actor_goals[0]
        return [f"Behind the visible event, the real struggle is over whether {actor} can {goal}."]
    return ["The visible event obscures a deeper struggle over leverage and cost."]


def _build_next_moves(actor_map: list[dict]) -> list[str]:
    grouped_moves: dict[str, list[str]] = {}
    for actor in actor_map:
        if not isinstance(actor, dict):
            continue
        name = str(actor.get("name") or "").strip()
        likely_next_move = str(actor.get("likely_next_move") or "").strip()
        goal = str(actor.get("goal") or "").strip()

        if likely_next_move:
            grouped_moves.setdefault(likely_next_move, [])
            if name:
                grouped_moves[likely_next_move].append(name)
        elif name and goal:
            fallback_move = f"keep pushing to {goal}"
            grouped_moves.setdefault(fallback_move, []).append(name)

    if grouped_moves:
        next_moves: list[str] = []
        for move, names in grouped_moves.items():
            subject = _join_names(names)
            verb = "are" if len(names) > 1 else _subject_verb(subject)
            next_moves.append(f"{subject} {verb} likely to {move}.")
        return next_moves

    return ["Escalation risk remains high."]


def _build_actor_paragraphs(actor_map: list[dict]) -> list[str]:
    if not actor_map:
        return []

    paragraphs = ["The strategic problem now looks different for each actor."]
    for actor in actor_map:
        if not isinstance(actor, dict):
            continue

        name = str(actor.get("name") or "").strip()
        goal = str(actor.get("goal") or "").strip()
        constraints = [str(item).strip() for item in (actor.get("constraints") or []) if str(item).strip()]
        benefits = [str(item).strip() for item in (actor.get("currently_benefits") or []) if str(item).strip()]
        pressures = [str(item).strip() for item in (actor.get("currently_pressures") or []) if str(item).strip()]
        likely_next_move = str(actor.get("likely_next_move") or "").strip()
        if not name:
            continue

        plural_subject = _is_plural_subject(name)
        pronoun = _subject_pronoun(name).capitalize()
        possessive = _subject_possessive(name).capitalize()
        parts: list[str] = []

        if goal:
            parts.append(f"For {name}, the crisis is now about {_goal_as_activity(goal)}.")
        else:
            parts.append(f"{name} {'are' if plural_subject else 'is'} trying to improve its position.")
        if constraints:
            parts.append(f"{pronoun} {'face' if plural_subject else 'faces'} {', '.join(constraints)}.")
        if benefits:
            parts.append(f"{pronoun} currently {'benefit' if plural_subject else 'benefits'} from {', '.join(benefits)}.")
        if pressures:
            parts.append(f"{pronoun} {'are' if plural_subject else 'is'} under pressure from {', '.join(pressures)}.")
        if likely_next_move:
            parts.append(f"{possessive} next move is likely to be to {likely_next_move}.")

        paragraphs.append(" ".join(parts))

    return paragraphs


def _build_next_phase_paragraph(next_moves: list[str]) -> str:
    clean_moves = [move for move in next_moves if str(move or "").strip()]
    if not clean_moves:
        return ""
    return " ".join(
        [
            "The next phase is likely to follow a few predictable tracks.",
            *clean_moves,
        ]
    )


def _build_unknowns_paragraph(unknowns: list[str]) -> str:
    clean_unknowns = [item for item in unknowns if str(item or "").strip()]
    if not clean_unknowns:
        return ""
    return " ".join(
        [
            "The hardest questions are still open.",
            *clean_unknowns,
            "Until those questions are resolved, the crisis will keep spilling costs beyond the battlefield.",
        ]
    )


def generate_flagship_analysis(
    dossier: dict,
    actor_map: list[dict],
    thesis: str,
) -> dict:
    topic = str(dossier.get("topic") or "This crisis").strip()
    topic_subject = _topic_subject(topic)
    facts = _clean_lines(dossier.get("verified_facts", []))
    claims = _clean_lines(dossier.get("claims", []))
    stakes = _clean_lines(dossier.get("stakes", []))
    unknowns = _clean_lines(dossier.get("unknowns", []))
    obscured_layer = _build_obscured_layer(dossier, actor_map)
    next_moves = _build_next_moves(actor_map)
    actor_paragraphs = _build_actor_paragraphs(actor_map)

    body_parts = [
        thesis,
        _build_lead_paragraph(topic_subject, facts),
        (
            f"The public case for the confrontation is straightforward. {' '.join(claims[:2])}"
            if claims
            else "The public case for the confrontation is still being shaped by competing narratives."
        ),
        " ".join(stakes) if stakes else "",
        *actor_paragraphs,
        " ".join(obscured_layer),
        _build_next_phase_paragraph(next_moves),
        _build_unknowns_paragraph(unknowns),
    ]
    body = "\n\n".join(part for part in body_parts if part).strip()

    filler_sentences = [
        f"That is why {topic.lower()} is becoming a contest over endurance, cost absorption, and political will rather than a story that can be measured only in battlefield damage.",
        f"The central question is no longer whether pressure exists, but which side can convert pressure into a durable change in the political balance before the wider system pushes back.",
        f"As long as the costs spill outward into shipping, energy, and alliance cohesion, the conflict will keep reshaping far more than the immediate battlefield.",
    ]
    filler_index = 0
    while len(body) < 1400:
        body = "\n\n".join(
            [
                body,
                filler_sentences[filler_index % len(filler_sentences)],
            ]
        )
        filler_index += 1

    return {
        "thesis": thesis,
        "known_facts": facts,
        "actor_map": actor_map,
        "stakes": stakes,
        "obscured_layer": obscured_layer,
        "next_moves": next_moves,
        "unknowns": unknowns,
        "full_article": body,
    }
