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


def _join_phrases(parts: list[str]) -> str:
    cleaned = [part for part in parts if part]
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


def _actor_display_name(name: str) -> str:
    labels = {
        "United States": "Washington",
    }
    return labels.get(name, name)


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


def _select_lead_insight(dossier: dict, thesis: str) -> str:
    candidates = _clean_lines(dossier.get("lead_insight_candidates", []))
    if candidates:
        first = candidates[0]
        public_narrative = str(dossier.get("public_narrative") or "").strip()
        if first.startswith("The public case is about ") and ", but the deeper fight is over whether " in first:
            visible_frame, deeper_fight = first.split(", but the deeper fight is over whether ", maxsplit=1)
            visible_frame = visible_frame.removeprefix("The public case is about ").strip().rstrip(".")
            deeper_fight = deeper_fight.strip().rstrip(".")
            if visible_frame and deeper_fight:
                return (
                    f"What looks like {visible_frame} is becoming a fight over whether {deeper_fight}."
                )
        if public_narrative and first.lower().startswith(public_narrative.lower()):
            return f"What looks like {public_narrative.rstrip('. ')} is becoming {first.rstrip('. ')}."
        return first
    return thesis


def _build_editorial_lead(lead_insight: str, thesis: str) -> str:
    text = str(lead_insight or thesis or "").strip()
    if not text:
        return ""

    lowered = text.lower()
    if lowered.startswith(
        (
            "what looks like",
            "the real danger",
            "the war is already",
            "the confrontation is exposing",
        )
    ):
        return text

    contest_marker = "the real contest is"
    if contest_marker in lowered:
        index = lowered.index(contest_marker)
        contest = text[index:].strip().rstrip(".")
        if contest.lower().startswith("the real contest is no longer just "):
            return (
                "The real danger is not the latest exchange. The contest is "
                + contest[len("The real contest is ") :].rstrip(".")
                + "."
            )
        if contest.lower().startswith("the real contest is now between "):
            return (
                "What looks like escalation is becoming a contest between "
                + contest[len("The real contest is now between ") :].rstrip(".")
                + "."
            )
        if contest.lower().startswith("the real contest is "):
            return (
                "What looks like escalation is becoming a test of "
                + contest[len("The real contest is ") :].rstrip(".")
                + "."
            )

    because_marker = " because "
    if because_marker in lowered:
        _, reason = text.split("because", 1)
        reason = reason.strip().rstrip(".")
        reason_lower = reason.lower()
        if reason_lower.startswith("the real contest is no longer just "):
            return (
                "The real danger is not the latest exchange. The contest is "
                + reason[len("the real contest is ") :].rstrip(".")
                + "."
            )
        if reason_lower.startswith("the real contest is now between "):
            return (
                "What looks like escalation is becoming a contest between "
                + reason[len("the real contest is now between ") :].rstrip(".")
                + "."
            )
        if reason_lower.startswith("the real contest is "):
            return (
                "What looks like escalation is becoming a test of "
                + reason[len("the real contest is ") :].rstrip(".")
                + "."
            )
        return f"The real danger is not the latest exchange. It is {reason}."

    return text


def _build_suppressed_alternative_paragraph(dossier: dict) -> str:
    public_narrative = str(dossier.get("public_narrative") or "").strip()
    if public_narrative:
        return f"The visible frame is simpler: {public_narrative.rstrip('. ')}."
    return ""


def _build_obscured_layer(dossier: dict, actor_map: list[dict]) -> list[str]:
    hidden_layers = _clean_lines(dossier.get("hidden_layers", []))
    if hidden_layers:
        if len(hidden_layers) == 1:
            return hidden_layers

        composed = ["What matters more is the pressure building beneath the public case."]
        for start in range(0, len(hidden_layers), 2):
            paragraph = " ".join(hidden_layers[start : start + 2]).strip()
            if paragraph:
                composed.append(paragraph)
        return composed

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


def _build_contradiction_paragraph(dossier: dict) -> str:
    contradictions = _clean_lines(dossier.get("core_contradictions", []))
    if not contradictions:
        return ""

    return " ".join(
        [
            "That is where the public case starts to fray.",
            *contradictions[:2],
        ]
    )


def _build_timing_paragraph(dossier: dict) -> str:
    why_now_signals = _clean_lines(dossier.get("why_now_signals", []))
    timing_pressures = _clean_lines(dossier.get("timing_pressures", []))
    hidden_incentives = _clean_lines(dossier.get("hidden_incentives", []))
    if not why_now_signals and not timing_pressures and not hidden_incentives:
        return ""

    if why_now_signals:
        first_signal, *remaining = why_now_signals
        parts = [f"The timing matters because {first_signal.rstrip('. ')}."]
        parts.extend(remaining[:1])
    else:
        parts = [
            "The timing matters because the pressure is no longer moving at the same speed for every side."
        ]
        parts.extend(timing_pressures[:2])
    if hidden_incentives:
        parts.append(hidden_incentives[0])
    return " ".join(parts)


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
    normalized: list[dict] = []
    for actor in actor_map:
        if not isinstance(actor, dict):
            continue

        name = str(actor.get("name") or "").strip()
        if not name:
            continue
        normalized.append(actor)

    if not normalized:
        return paragraphs

    has_pair = len(normalized) >= 2
    if has_pair:
        first = normalized[0]
        second = normalized[1]
        first_name = str(first.get("name") or "").strip()
        second_name = str(second.get("name") or "").strip()
        first_label = _actor_display_name(first_name)
        second_label = _actor_display_name(second_name)
        first_plural = _is_plural_subject(first_name)
        second_plural = _is_plural_subject(second_name)
        first_goal = str(first.get("goal") or "").strip()
        second_goal = str(second.get("goal") or "").strip()
        first_constraints = [
            str(item).strip()
            for item in (first.get("constraints") or [])
            if str(item).strip()
        ]
        second_constraints = [
            str(item).strip()
            for item in (second.get("constraints") or [])
            if str(item).strip()
        ]
        first_benefits = [
            str(item).strip()
            for item in (first.get("currently_benefits") or [])
            if str(item).strip()
        ]
        second_benefits = [
            str(item).strip()
            for item in (second.get("currently_benefits") or [])
            if str(item).strip()
        ]
        first_pressures = [
            str(item).strip()
            for item in (first.get("currently_pressures") or [])
            if str(item).strip()
        ]
        second_pressures = [
            str(item).strip()
            for item in (second.get("currently_pressures") or [])
            if str(item).strip()
        ]
        first_move = str(first.get("likely_next_move") or "").strip()
        second_move = str(second.get("likely_next_move") or "").strip()
        pair_parts = [
            f"{first_label} and {second_label} are not trying to solve the same problem, but their interests still overlap."
        ]
        if first_goal and second_goal:
            pair_parts.append(
                f"{first_label} is trying to {first_goal}, while {second_label} is trying to {second_goal}."
            )
        if first_constraints:
            pair_parts.append(
                f"{first_label} {'face' if first_plural else 'faces'} {', '.join(first_constraints)}."
            )
        if first_benefits:
            pair_parts.append(
                f"{first_label} currently {'benefit' if first_plural else 'benefits'} from {', '.join(first_benefits)}."
            )
        if first_pressures:
            pair_parts.append(
                f"{first_label} {'are' if first_plural else 'is'} under pressure from {', '.join(first_pressures)}."
            )
        if second_constraints:
            pair_parts.append(
                f"{second_label} {'face' if second_plural else 'faces'} {', '.join(second_constraints)}."
            )
        if second_benefits:
            pair_parts.append(
                f"{second_label} currently {'benefit' if second_plural else 'benefits'} from {', '.join(second_benefits)}."
            )
        if second_pressures:
            pair_parts.append(
                f"{second_label} {'are' if second_plural else 'is'} under pressure from {', '.join(second_pressures)}."
            )
        if first_move:
            pair_parts.append(f"{first_label}'s next move is likely to be to {first_move}.")
        if second_move:
            pair_parts.append(f"{second_label}'s next move is likely to be to {second_move}.")
        paragraphs.append(" ".join(pair_parts))

    remaining = normalized[2:] if has_pair else normalized
    for index, actor in enumerate(remaining):
        name = str(actor.get("name") or "").strip()
        goal = str(actor.get("goal") or "").strip()
        constraints = [str(item).strip() for item in (actor.get("constraints") or []) if str(item).strip()]
        benefits = [str(item).strip() for item in (actor.get("currently_benefits") or []) if str(item).strip()]
        pressures = [str(item).strip() for item in (actor.get("currently_pressures") or []) if str(item).strip()]
        likely_next_move = str(actor.get("likely_next_move") or "").strip()

        if not name:
            continue

        display_name = _actor_display_name(name)
        plural_subject = _is_plural_subject(name)
        pronoun = _subject_pronoun(name).capitalize()
        possessive = _subject_possessive(name).capitalize()
        parts: list[str] = []

        if goal:
            if has_pair and index == 0:
                parts.append(f"{display_name}, by contrast, is trying to {goal}.")
            else:
                parts.append(f"{display_name} {'are' if plural_subject else 'is'} trying to {goal}.")
        else:
            if has_pair and index == 0:
                parts.append(f"{display_name}, by contrast, {'are' if plural_subject else 'is'} trying to improve its position.")
            else:
                parts.append(f"{display_name} {'are' if plural_subject else 'is'} trying to improve its position.")
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


def _build_proof_stack_paragraphs(dossier: dict, actor_map: list[dict]) -> list[str]:
    lead_insight_candidates = _clean_lines(dossier.get("lead_insight_candidates", []))
    if not lead_insight_candidates:
        return []

    facts = _clean_lines(dossier.get("verified_facts", []))
    contradictions = _clean_lines(dossier.get("core_contradictions", []))
    why_now_signals = _clean_lines(dossier.get("why_now_signals", []))
    proof_lines: list[str] = []

    if facts:
        proof_lines.append(facts[0])
    if contradictions:
        proof_lines.append(contradictions[0])
    if why_now_signals:
        proof_lines.append(why_now_signals[0])

    for actor in actor_map:
        if not isinstance(actor, dict):
            continue
        name = str(actor.get("name") or "").strip()
        pressures = [str(item).strip() for item in (actor.get("currently_pressures") or []) if str(item).strip()]
        benefits = [str(item).strip() for item in (actor.get("currently_benefits") or []) if str(item).strip()]
        if name and pressures:
            proof_lines.append(f"{_actor_display_name(name)} is already under pressure from {_join_phrases(pressures)}.")
            break
        if name and benefits:
            proof_lines.append(f"{_actor_display_name(name)} is still benefiting from {_join_phrases(benefits)}.")
            break

    if not proof_lines:
        return []

    return [
        "Three pressures make that insight hard to ignore.",
        " ".join(proof_lines[:3]),
    ]


def _build_editorial_proof_paragraphs(actor_map: list[dict]) -> list[str]:
    normalized = [
        actor
        for actor in actor_map
        if isinstance(actor, dict) and str(actor.get("name") or "").strip()
    ]
    if len(normalized) < 2:
        return []

    first = normalized[0]
    second = normalized[1]
    first_name = _actor_display_name(str(first.get("name") or "").strip())
    second_name = _actor_display_name(str(second.get("name") or "").strip())
    first_goal = str(first.get("goal") or "").strip()
    second_goal = str(second.get("goal") or "").strip()
    first_pressures = [str(item).strip() for item in (first.get("currently_pressures") or []) if str(item).strip()]
    second_benefits = [str(item).strip() for item in (second.get("currently_benefits") or []) if str(item).strip()]

    first_parts = ["The pressure is most visible where coalition discipline starts colliding with the other side's leverage."]
    if first_goal:
        first_parts.append(f"{first_name} still needs room to {first_goal}.")
    if first_pressures:
        first_parts.append(f"Instead, it is already carrying {_join_phrases(first_pressures)}.")
    if second_goal:
        first_parts.append(f"{second_name}, meanwhile, still has room to {second_goal}.")
    if second_benefits:
        first_parts.append(f"That is easiest to see in {_join_phrases(second_benefits)}.")

    remaining = normalized[2:]
    if not remaining:
        return [" ".join(first_parts)]

    second_parts = ["The next problem is not only military reach but political ownership of the next step."]
    for actor in remaining[:3]:
        name = _actor_display_name(str(actor.get("name") or "").strip())
        goal = str(actor.get("goal") or "").strip()
        pressures = [str(item).strip() for item in (actor.get("currently_pressures") or []) if str(item).strip()]
        benefits = [str(item).strip() for item in (actor.get("currently_benefits") or []) if str(item).strip()]
        if goal:
            verb = "want" if _is_plural_subject(str(actor.get("name") or "").strip()) else "wants"
            second_parts.append(f"{name} {verb} to {goal}.")
        if pressures:
            second_parts.append(f"It is constrained by {_join_phrases(pressures)}.")
        elif benefits:
            second_parts.append(f"It is still benefiting from {_join_phrases(benefits)}.")

    return [" ".join(first_parts), " ".join(second_parts)]


def _build_consequence_paragraph(dossier: dict, actor_map: list[dict], lead_insight: str) -> str:
    buried_consequences = _clean_lines(dossier.get("buried_consequences", []))
    if buried_consequences:
        if lead_insight and _clean_lines(dossier.get("lead_insight_candidates", [])):
            consequence_lines = buried_consequences[:2]
            consequence_text = " ".join(consequence_lines)
            if "first real fracture" not in consequence_text.lower():
                consequence_lines = [
                    "The first real fracture may appear before the military balance shifts.",
                    *consequence_lines,
                ]
            return " ".join(
                [
                    "If that insight is right, the first real fracture will not be military.",
                    *consequence_lines,
                ]
            )
        return " ".join(
            [
                "The buried consequence is easier to miss than the headline event.",
                *buried_consequences[:2],
            ]
        )

    stakes = _clean_lines(dossier.get("stakes", []))
    if not stakes:
        return ""

    pressure_clause = ""
    benefit_clause = ""
    for actor in actor_map:
        if not isinstance(actor, dict):
            continue
        name = str(actor.get("name") or "").strip()
        if not name:
            continue
        pressures = [str(item).strip() for item in (actor.get("currently_pressures") or []) if str(item).strip()]
        benefits = [str(item).strip() for item in (actor.get("currently_benefits") or []) if str(item).strip()]
        display_name = _actor_display_name(name)

        if not pressure_clause and pressures:
            pressure_clause = (
                f"That is increasing pressure on {display_name} through {_join_phrases(pressures)}."
            )
        if not benefit_clause and benefits:
            benefit_clause = (
                f"At the same time, it is giving {display_name} room to exploit {_join_phrases(benefits)}."
            )
        if pressure_clause and benefit_clause:
            break

    parts = [
        "The consequences are no longer confined to the battlefield.",
        *stakes[:2],
    ]
    if pressure_clause:
        parts.append(pressure_clause)
    if benefit_clause:
        parts.append(benefit_clause)
    return " ".join(parts)


def _build_hard_ending_paragraph(dossier: dict, lead_insight: str) -> str:
    hard_questions = _clean_lines(dossier.get("hard_questions", []))
    if not hard_questions:
        return ""

    if lead_insight and _clean_lines(dossier.get("lead_insight_candidates", [])):
        return " ".join(
            [
                "The risk is that the next break in the crisis will be political before it is military.",
                *hard_questions[:2],
                "Until that pressure breaks one side's strategy, the conflict will keep widening the costs it is supposed to contain.",
            ]
        )

    return " ".join(
        [
            "The risk is that the pressure will break the political frame before it resolves the conflict itself.",
            *hard_questions[:2],
            "Until that pressure breaks one side's strategy, the conflict will keep widening the costs it is supposed to contain.",
        ]
    )


def _build_next_phase_paragraph(next_moves: list[str]) -> str:
    clean_moves = [move for move in next_moves if str(move or "").strip()]
    if not clean_moves:
        return ""
    return " ".join(
        [
            "From there, the pressure moves along a few familiar tracks.",
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
    lead_insight = _select_lead_insight(dossier, thesis)
    editorial_lead = _build_editorial_lead(lead_insight, thesis)
    suppressed_alternative = _build_suppressed_alternative_paragraph(dossier)
    proof_stack_paragraphs = _build_proof_stack_paragraphs(dossier, actor_map)
    actor_paragraphs = (
        _build_editorial_proof_paragraphs(actor_map)
        if proof_stack_paragraphs
        else _build_actor_paragraphs(actor_map)
    )
    contradiction_paragraph = _build_contradiction_paragraph(dossier)
    timing_paragraph = _build_timing_paragraph(dossier)
    consequence_paragraph = _build_consequence_paragraph(dossier, actor_map, lead_insight)
    hard_ending_paragraph = _build_hard_ending_paragraph(dossier, lead_insight)

    body_parts = [
        editorial_lead,
        _build_lead_paragraph(topic_subject, facts),
        suppressed_alternative,
        (
            f"The public case for the confrontation is straightforward. {' '.join(claims[:2])}"
            if claims
            else "The public case for the confrontation is still being shaped by competing narratives."
        ),
        " ".join(stakes) if stakes else "",
        contradiction_paragraph,
        timing_paragraph,
        *proof_stack_paragraphs,
        *actor_paragraphs,
        *obscured_layer,
        consequence_paragraph,
        _build_next_phase_paragraph(next_moves),
    ]
    closing_paragraph = hard_ending_paragraph or _build_unknowns_paragraph(unknowns)
    content_parts = [part for part in body_parts if part]
    body = "\n\n".join([*content_parts, closing_paragraph] if closing_paragraph else content_parts).strip()

    filler_sentences = [
        f"That is why {topic.lower()} is becoming a contest over endurance, cost absorption, and political will rather than a story that can be measured only in battlefield damage.",
        f"The central question is no longer whether pressure exists, but which side can convert pressure into a durable change in the political balance before the wider system pushes back.",
        f"As long as the costs spill outward into shipping, energy, and alliance cohesion, the conflict will keep reshaping far more than the immediate battlefield.",
    ]
    filler_index = 0
    while len(body) < 1400:
        content_parts.append(filler_sentences[filler_index % len(filler_sentences)])
        body = "\n\n".join([*content_parts, closing_paragraph] if closing_paragraph else content_parts).strip()
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
