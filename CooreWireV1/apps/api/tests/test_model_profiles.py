from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.llm.router import get_agent_model


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
