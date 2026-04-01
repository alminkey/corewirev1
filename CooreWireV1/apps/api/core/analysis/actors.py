def build_actor_map(dossier: dict, actors: list[dict]) -> list[dict]:
    return [
        {
            "name": actor["name"],
            "goal": actor.get("goal", ""),
            "constraints": actor.get("constraints", []),
            "likely_next_move": actor.get("likely_next_move", ""),
        }
        for actor in actors
    ]
