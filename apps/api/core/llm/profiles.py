MODEL_PROFILES = {
    "economy": {
        "research": {
            "provider": "perplexity",
            "model": "sonar",
            "fallback_model": "sonar",
        },
        "writer": {
            "provider": "anthropic",
            "model": "claude-haiku-4.5",
            "fallback_model": "claude-sonnet-4.6",
        },
        "validator": {
            "provider": "openai",
            "model": "gpt-5-mini",
            "fallback_model": "gpt-5-mini",
        },
    },
    "balanced": {
        "research": {
            "provider": "perplexity",
            "model": "sonar-pro",
            "fallback_model": "sonar",
        },
        "writer": {
            "provider": "anthropic",
            "model": "claude-sonnet-4.6",
            "fallback_model": "claude-haiku-4.5",
        },
        "validator": {
            "provider": "openai",
            "model": "gpt-5-mini",
            "fallback_model": "gpt-5-mini",
        },
    },
    "premium": {
        "research": {
            "provider": "perplexity",
            "model": "sonar-deep-research",
            "fallback_model": "sonar-pro",
        },
        "writer": {
            "provider": "anthropic",
            "model": "claude-opus-4.6",
            "fallback_model": "claude-sonnet-4.6",
        },
        "validator": {
            "provider": "openai",
            "model": "gpt-5-mini",
            "fallback_model": "gpt-5-mini",
        },
    },
}
