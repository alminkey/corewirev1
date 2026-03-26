from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.config import Settings
from core.llm.router import get_agent_model
from core.llm.router import resolve_agent_model


def test_balanced_profile_maps_writer_and_research_agents_to_expected_models():
    research_model = get_agent_model("balanced", "research")
    writer_model = get_agent_model("balanced", "writer")
    validator_model = get_agent_model("balanced", "validator")

    assert research_model["provider"] == "perplexity"
    assert research_model["model"] == "sonar-pro"
    assert writer_model["provider"] == "anthropic"
    assert writer_model["model"] == "claude-sonnet-4.6"
    assert validator_model["provider"] == "openai"
    assert validator_model["model"] == "gpt-5-mini"


def test_premium_and_economy_profiles_expose_fallbacks():
    premium_writer = get_agent_model("premium", "writer")
    economy_research = get_agent_model("economy", "research")

    assert premium_writer["fallback_model"] == "claude-sonnet-4.6"
    assert economy_research["fallback_model"] == "sonar"


def test_settings_default_to_balanced_openrouter_from_env(monkeypatch):
    monkeypatch.setenv("COREWIRE_MODEL_PROFILE", "balanced")
    monkeypatch.setenv("COREWIRE_LLM_ROUTER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")
    monkeypatch.setenv("COREWIRE_DATABASE_URL", "sqlite:///corewire-test.db")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///fallback.db")

    settings = Settings.from_env()

    assert settings.model_profile == "balanced"
    assert settings.llm_router == "openrouter"
    assert settings.openrouter_api_key == "test-openrouter-key"
    assert settings.corewire_database_url == "sqlite:///corewire-test.db"
    assert settings.database_url == "sqlite:///fallback.db"


def test_resolve_agent_model_uses_openrouter_when_enabled(monkeypatch):
    monkeypatch.setenv("COREWIRE_MODEL_PROFILE", "balanced")
    monkeypatch.setenv("COREWIRE_LLM_ROUTER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")

    research_model = resolve_agent_model("research")
    writer_model = resolve_agent_model("writer")
    validator_model = resolve_agent_model("validator")

    assert research_model["provider"] == "openrouter"
    assert research_model["model"] == "perplexity/sonar-pro"
    assert writer_model["provider"] == "openrouter"
    assert writer_model["model"] == "anthropic/claude-sonnet-4.6"
    assert validator_model["provider"] == "openrouter"
    assert validator_model["model"] == "openai/gpt-5-mini"
