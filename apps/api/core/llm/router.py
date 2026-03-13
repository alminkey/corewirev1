from core.llm.profiles import MODEL_PROFILES


def get_agent_model(profile_name: str, agent_role: str) -> dict:
    try:
        return MODEL_PROFILES[profile_name][agent_role]
    except KeyError as exc:
        raise ValueError(
            f"Unknown model selection for profile={profile_name}, agent_role={agent_role}"
        ) from exc
