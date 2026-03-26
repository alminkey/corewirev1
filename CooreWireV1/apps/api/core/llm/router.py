from core.config import Settings
from core.llm.profiles import MODEL_PROFILES


def get_agent_model(profile_name: str, agent_role: str) -> dict:
    try:
        return MODEL_PROFILES[profile_name][agent_role]
    except KeyError as exc:
        raise ValueError(
            f"Unknown model selection for profile={profile_name}, agent_role={agent_role}"
        ) from exc


def resolve_agent_model(agent_role: str, profile_name: str | None = None) -> dict:
    settings = Settings.from_env()
    effective_profile = profile_name or settings.model_profile
    selected_model = get_agent_model(effective_profile, agent_role).copy()

    if settings.llm_router != "openrouter":
        return selected_model

    if not settings.openrouter_api_key:
        raise ValueError("OPENROUTER_API_KEY is required when COREWIRE_LLM_ROUTER=openrouter")

    source_provider = selected_model["provider"]
    selected_model["provider"] = "openrouter"
    selected_model["model"] = _to_openrouter_model_id(
        source_provider, selected_model["model"]
    )
    selected_model["fallback_model"] = _to_openrouter_model_id(
        source_provider, selected_model["fallback_model"]
    )
    return selected_model


def _to_openrouter_model_id(provider: str, model: str) -> str:
    return f"{provider}/{model}"
