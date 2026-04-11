from pathlib import Path
from types import SimpleNamespace
import uuid
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import core.operator.service as operator_service
from core.operator.service import execute_operator_command
from core.operator.service import OpenRouterClient


def test_execute_operator_command_discovers_trending_story_with_openrouter(monkeypatch):
    monkeypatch.setenv("COREWIRE_MODEL_PROFILE", "balanced")
    monkeypatch.setenv("COREWIRE_LLM_ROUTER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")

    class FakeOpenRouterClient:
        def __init__(self, api_key: str) -> None:
            assert api_key == "test-openrouter-key"

        def complete_json(self, *, model: str, system_prompt: str, user_prompt: str) -> dict:
            assert model == "perplexity/sonar-pro"
            assert "ai-tech-business" in user_prompt
            return {
                "shortlist": [
                    {
                        "title": "OpenAI expands enterprise coding automation",
                        "summary": "The update adds tighter review loops for enterprise teams.",
                        "why_it_matters": "It signals a more competitive AI coding market.",
                        "source_count": 3,
                        "confidence": "high",
                        "sources": [
                            {"publisher": "Reuters", "url": "https://example.com/reuters"},
                            {"publisher": "The Verge", "url": "https://example.com/verge"},
                            {"publisher": "TechCrunch", "url": "https://example.com/tc"},
                        ],
                    }
                ]
            }

    monkeypatch.setattr(
        "core.operator.service.OpenRouterClient",
        FakeOpenRouterClient,
    )

    result = execute_operator_command(
        {
            "type": "discover_trending_story",
            "payload": {"domain": "ai-tech-business", "count": 3},
        }
    )

    assert result["accepted"] is True
    assert result["router"] == "openrouter"
    assert result["profile"] == "balanced"
    assert result["models"]["research"] == "perplexity/sonar-pro"
    assert result["shortlist"][0]["confidence"] == "high"


def test_execute_operator_command_builds_story_draft_with_openrouter(monkeypatch):
    monkeypatch.setenv("COREWIRE_MODEL_PROFILE", "balanced")
    monkeypatch.setenv("COREWIRE_LLM_ROUTER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")

    class FakeOpenRouterClient:
        def __init__(self, api_key: str) -> None:
            assert api_key == "test-openrouter-key"

        def complete_json(self, *, model: str, system_prompt: str, user_prompt: str) -> dict:
            if model == "anthropic/claude-sonnet-4.6":
                assert "OpenAI expands enterprise coding automation" in user_prompt
                return {
                    "headline": "OpenAI pushes deeper into enterprise coding workflows",
                    "dek": "A fuller report assembled from corroborated reporting.",
                    "narrative": "Enterprise buyers are weighing tighter coding loops.",
                    "fact_blocks": [
                        {"text": "OpenAI described new workflow updates for enterprise teams."}
                    ],
                    "analysis_blocks": [
                        {"text": "The release increases pressure on rival coding vendors."}
                    ],
                    "sources": [
                        {"publisher": "Reuters", "url": "https://example.com/reuters"},
                    ],
                }
            raise AssertionError(f"Unexpected model {model}")

    monkeypatch.setattr(
        "core.operator.service.OpenRouterClient",
        FakeOpenRouterClient,
    )

    result = execute_operator_command(
        {
            "type": "build_story_draft",
            "payload": {
                "candidate": {
                    "title": "OpenAI expands enterprise coding automation",
                    "summary": "The update adds tighter review loops for enterprise teams.",
                    "why_it_matters": "It signals a more competitive AI coding market.",
                    "sources": [
                        {"publisher": "Reuters", "url": "https://example.com/reuters"},
                    ],
                },
                "length": "full_report",
            },
        }
    )

    assert result["accepted"] is True
    assert result["profile"] == "balanced"
    assert result["models"]["writer"] == "anthropic/claude-sonnet-4.6"
    assert result["draft"]["headline"] == (
        "OpenAI pushes deeper into enterprise coding workflows"
    )


def test_execute_operator_command_publishes_preview_article_and_keeps_correlation(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-preview-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    try:
        result = execute_operator_command(
            {
                "type": "publish_preview_article",
                "ticket_id": "ticket-123",
                "actor_id": "owner-1",
                "correlation_id": "corr-123",
                "payload": {
                    "draft": {
                        "headline": "Preview headline",
                        "dek": "Preview dek",
                        "fact_blocks": [
                            {"statement": "Preview fact", "sources": ["Reuters", "The Verge"]}
                        ],
                        "analysis_blocks": [{"analysis": "Preview analysis"}],
                        "sources": [{"organization": "Reuters", "url": "https://example.com"}],
                    },
                    "confidence": {"level": "high", "homepage_eligible": True},
                    "story_tier": "standard",
                    "requested_profile": "balanced",
                    "effective_profile": "balanced",
                },
            }
        )

        assert result["accepted"] is True
        assert result["type"] == "publish_preview_article"
        assert result["article"]["status"] == "published"
        assert result["article"]["homepage_eligible"] is True
        assert result["article"]["sources"] == [
            {
                "label": "Reuters",
                "publisher": "Reuters",
                "title": None,
                "url": "https://example.com",
                "role": "source",
            }
        ]
        assert result["correlation"]["ticket_id"] == "ticket-123"
        assert result["correlation"]["actor_id"] == "owner-1"
        assert result["correlation"]["correlation_id"] == "corr-123"
    finally:
        if database_path.exists():
            database_path.unlink()


def test_execute_operator_command_archives_preview_article(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-archive-{uuid.uuid4().hex}.db"
    database_url = f"sqlite+pysqlite:///{database_path}"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", database_url)

    try:
        published = execute_operator_command(
            {
                "type": "publish_preview_article",
                "payload": {
                    "draft": {
                        "headline": "Archive me",
                        "dek": "Archive dek",
                        "fact_blocks": [{"statement": "Fact", "sources": ["Reuters"]}],
                        "analysis_blocks": [{"analysis": "Analysis"}],
                        "sources": ["Reuters"],
                    },
                    "confidence": {"level": "high", "homepage_eligible": True},
                },
            }
        )

        archived = execute_operator_command(
            {
                "type": "archive_preview_article",
                "payload": {"slug": published["article"]["slug"]},
            }
        )

        assert archived["accepted"] is True
        assert archived["article"]["slug"] == published["article"]["slug"]
        assert archived["article"]["status"] == "superseded"
        assert archived["article"]["homepage_eligible"] is False
    finally:
        if database_path.exists():
            database_path.unlink()


def test_execute_operator_command_auto_publishes_high_confidence_story(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-gate-publish-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    try:
        result = execute_operator_command(
            {
                "type": "publish_if_eligible",
                "payload": {
                    "draft": {
                        "headline": "Auto publish headline",
                        "dek": "Auto publish dek",
                        "fact_blocks": [{"text": "Fact", "citations": ["Reuters", "Bloomberg", "The Verge"]}],
                        "analysis_blocks": [{"text": "Analysis"}],
                        "sources": [
                            {"publisher": "Reuters", "url": "https://example.com/reuters"},
                            {"publisher": "Bloomberg", "url": "https://example.com/bloomberg"},
                            {"publisher": "The Verge", "url": "https://example.com/verge"},
                        ],
                    },
                    "confidence": {"level": "high", "homepage_eligible": True},
                    "flags": [],
                    "story_tier": "standard",
                },
            }
        )

        assert result["accepted"] is True
        assert result["decision"]["action"] == "auto_publish"
        assert result["article"]["status"] == "published"
        assert result["decision"]["reasons"] == []
    finally:
        if database_path.exists():
            database_path.unlink()


def test_execute_operator_command_routes_medium_confidence_story_to_review_queue(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-gate-review-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    try:
        result = execute_operator_command(
            {
                "type": "publish_if_eligible",
                "payload": {
                    "draft": {
                        "headline": "Needs review headline",
                        "dek": "Needs review dek",
                        "fact_blocks": [{"text": "Fact", "citations": ["Reuters", "Bloomberg"]}],
                        "analysis_blocks": [{"text": "Analysis"}],
                        "sources": [
                            {"publisher": "Reuters", "url": "https://example.com/reuters"},
                            {"publisher": "Bloomberg", "url": "https://example.com/bloomberg"},
                        ],
                    },
                    "confidence": {"level": "medium", "homepage_eligible": False},
                    "flags": [],
                    "story_tier": "standard",
                },
            }
        )

        assert result["accepted"] is True
        assert result["decision"]["action"] == "review_required"
        assert "medium_confidence" in result["decision"]["reasons"]
        assert result["review_item"]["queue"] == "pending_drafts"
    finally:
        if database_path.exists():
            database_path.unlink()


def test_execute_operator_command_runs_composite_content_pipeline(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-composite-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    class FakeOpenRouterClient:
        def __init__(self, api_key: str) -> None:
            assert api_key == "test-openrouter-key"

        def complete_json(self, *, model: str, system_prompt: str, user_prompt: str) -> dict:
            if model == "perplexity/sonar-pro":
                return {
                    "shortlist": [
                        {
                            "title": "Enterprise AI agents move from copilots to orchestrators",
                            "summary": "Vendors are pushing AI agents into multi-step enterprise workflows.",
                            "why_it_matters": "This changes how teams buy and govern AI tooling.",
                            "source_count": 3,
                            "confidence": "high",
                            "sources": [
                                {"publisher": "Reuters", "url": "https://example.com/reuters"},
                                {"publisher": "Bloomberg", "url": "https://example.com/bloomberg"},
                                {"publisher": "The Verge", "url": "https://example.com/verge"},
                            ],
                        }
                    ]
                }
            if model == "anthropic/claude-sonnet-4.6":
                return {
                    "headline": "AI agents are moving from copilots to enterprise orchestrators",
                    "dek": "A fuller report built from corroborated reporting.",
                    "narrative": "Enterprise buyers are shifting toward multi-step orchestration.",
                    "fact_blocks": [
                        {"text": "Major vendors are expanding agents into orchestrated workflow tasks.", "citations": ["Reuters", "Bloomberg", "The Verge"]}
                    ],
                    "analysis_blocks": [
                        {"text": "The shift raises governance and procurement stakes for enterprise AI."}
                    ],
                    "sources": [
                        {"publisher": "Reuters", "url": "https://example.com/reuters"},
                        {"publisher": "Bloomberg", "url": "https://example.com/bloomberg"},
                        {"publisher": "The Verge", "url": "https://example.com/verge"},
                    ],
                }
            raise AssertionError(f"Unexpected model {model}")

    monkeypatch.setenv("COREWIRE_MODEL_PROFILE", "balanced")
    monkeypatch.setenv("COREWIRE_LLM_ROUTER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")
    monkeypatch.setattr("core.operator.service.OpenRouterClient", FakeOpenRouterClient)

    try:
        result = execute_operator_command(
            {
                "type": "run_content_pipeline",
                "payload": {
                    "domain": "ai-tech-business",
                    "count": 3,
                    "candidate_index": 0,
                    "length": "full_report",
                },
            }
        )

        assert result["accepted"] is True
        assert result["type"] == "run_content_pipeline"
        assert result["selected_candidate"]["title"] == (
            "Enterprise AI agents move from copilots to orchestrators"
        )
        assert result["draft"]["headline"] == (
            "AI agents are moving from copilots to enterprise orchestrators"
        )
        assert result["decision"]["action"] == "auto_publish"
        assert result["article"]["status"] == "published"
    finally:
        if database_path.exists():
            database_path.unlink()


def test_publish_gate_rejects_string_or_numeric_source_references(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-invalid-sources-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    try:
        result = execute_operator_command(
            {
                "type": "publish_if_eligible",
                "payload": {
                    "draft": {
                        "headline": "Invalid sources story",
                        "dek": "Dek",
                        "fact_blocks": [{"text": "Fact", "citations": ["A", "B", "C"]}],
                        "analysis_blocks": [{"text": "Analysis"}],
                        "sources": ["IBM Think[1]", 2, {"publisher": "Capgemini"}],
                    },
                    "confidence": {"level": "high", "homepage_eligible": True},
                    "flags": [],
                },
            }
        )

        assert result["decision"]["action"] == "review_required"
        assert "invalid_source_shape" in result["decision"]["reasons"]
        assert "missing_source_urls" in result["decision"]["reasons"]
    finally:
        if database_path.exists():
            database_path.unlink()


def test_publish_gate_allows_linkable_source_objects(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-valid-sources-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    try:
        result = execute_operator_command(
            {
                "type": "publish_if_eligible",
                "payload": {
                    "draft": {
                        "headline": "Valid sources story",
                        "dek": "Dek",
                        "fact_blocks": [{"text": "Fact", "citations": ["Reuters", "Bloomberg", "The Verge"]}],
                        "analysis_blocks": [{"text": "Analysis"}],
                        "sources": [
                            {
                                "label": "Reuters",
                                "publisher": "Reuters",
                                "title": "Enterprise AI report",
                                "url": "https://example.com/reuters",
                                "role": "source",
                            },
                            {
                                "label": "Bloomberg",
                                "publisher": "Bloomberg",
                                "title": "Agent market story",
                                "url": "https://example.com/bloomberg",
                                "role": "source",
                            },
                            {
                                "label": "The Verge",
                                "publisher": "The Verge",
                                "title": "Enterprise tooling piece",
                                "url": "https://example.com/verge",
                                "role": "source",
                            },
                        ],
                    },
                    "confidence": {"level": "high", "homepage_eligible": True},
                    "flags": [],
                },
            }
        )

        assert result["decision"]["action"] == "auto_publish"
        assert result["decision"]["reasons"] == []
        assert result["article"]["status"] == "published"
    finally:
        if database_path.exists():
            database_path.unlink()


def test_publish_gate_rejects_low_diversity_source_mix(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-low-diversity-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    try:
        result = execute_operator_command(
            {
                "type": "publish_if_eligible",
                "payload": {
                    "draft": {
                        "headline": "Low diversity story",
                        "dek": "Dek",
                        "fact_blocks": [{"text": "Fact", "citations": ["IBM", "IBM", "IBM"]}],
                        "analysis_blocks": [{"text": "Analysis"}],
                        "sources": [
                            {
                                "label": "IBM Think 1",
                                "publisher": "IBM",
                                "title": "Source one",
                                "url": "https://example.com/ibm-1",
                                "role": "source",
                            },
                            {
                                "label": "IBM Think 2",
                                "publisher": "IBM",
                                "title": "Source two",
                                "url": "https://example.com/ibm-2",
                                "role": "source",
                            },
                            {
                                "label": "IBM Think 3",
                                "publisher": "IBM",
                                "title": "Source three",
                                "url": "https://example.com/ibm-3",
                                "role": "source",
                            },
                        ],
                    },
                    "confidence": {"level": "high", "homepage_eligible": True},
                    "flags": [],
                },
            }
        )

        assert result["decision"]["action"] == "review_required"
        assert "insufficient_source_diversity" in result["decision"]["reasons"]
    finally:
        if database_path.exists():
            database_path.unlink()


def test_publish_gate_rejects_video_source_dependency(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-video-source-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    try:
        result = execute_operator_command(
            {
                "type": "publish_if_eligible",
                "payload": {
                    "draft": {
                        "headline": "Video dependency story",
                        "dek": "Dek",
                        "fact_blocks": [{"text": "Fact", "citations": ["YouTube", "Reuters", "Bloomberg"]}],
                        "analysis_blocks": [{"text": "Analysis"}],
                        "sources": [
                            {
                                "label": "YouTube clip",
                                "publisher": "YouTube",
                                "title": "Panel clip",
                                "url": "https://www.youtube.com/watch?v=abc",
                                "role": "source",
                            },
                            {
                                "label": "Reuters",
                                "publisher": "Reuters",
                                "title": "Source one",
                                "url": "https://example.com/reuters",
                                "role": "source",
                            },
                            {
                                "label": "Bloomberg",
                                "publisher": "Bloomberg",
                                "title": "Source two",
                                "url": "https://example.com/bloomberg",
                                "role": "source",
                            },
                        ],
                    },
                    "confidence": {"level": "high", "homepage_eligible": True},
                    "flags": [],
                },
            }
        )

        assert result["decision"]["action"] == "review_required"
        assert "video_source_dependency" in result["decision"]["reasons"]
    finally:
        if database_path.exists():
            database_path.unlink()


def test_composite_pipeline_enriches_source_references_into_linkable_objects(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-enrich-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")
    monkeypatch.setenv("COREWIRE_MODEL_PROFILE", "balanced")
    monkeypatch.setenv("COREWIRE_LLM_ROUTER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")

    class FakeOpenRouterClient:
        def __init__(self, api_key: str) -> None:
            assert api_key == "test-openrouter-key"

        def complete_json(self, *, model: str, system_prompt: str, user_prompt: str) -> dict:
            if model == "perplexity/sonar-pro" and "Find" in user_prompt:
                return {
                    "shortlist": [
                        {
                            "title": "Enterprise agents go mainstream",
                            "summary": "Vendors are pushing enterprise agent orchestration.",
                            "why_it_matters": "This shifts AI from copilots to workflow automation.",
                            "source_count": 3,
                            "confidence": "high",
                            "sources": ["Reuters[1]", "Bloomberg[2]", "The Verge[3]"],
                        }
                    ]
                }
            if model == "perplexity/sonar-pro" and "Normalize and enrich" in user_prompt:
                return {
                    "sources": [
                        {
                            "label": "Reuters",
                            "publisher": "Reuters",
                            "title": "Enterprise agents story",
                            "url": "https://example.com/reuters",
                            "role": "source",
                        },
                        {
                            "label": "Bloomberg",
                            "publisher": "Bloomberg",
                            "title": "Automation market report",
                            "url": "https://example.com/bloomberg",
                            "role": "source",
                        },
                        {
                            "label": "The Verge",
                            "publisher": "The Verge",
                            "title": "Enterprise tooling piece",
                            "url": "https://example.com/verge",
                            "role": "source",
                        },
                    ]
                }
            if model == "anthropic/claude-sonnet-4.6":
                return {
                    "headline": "Enterprise agents go mainstream",
                    "dek": "Dek",
                    "narrative": "Narrative",
                    "fact_blocks": [{"text": "Fact", "citations": ["Reuters", "Bloomberg", "The Verge"]}],
                    "analysis_blocks": [{"text": "Analysis"}],
                    "sources": [
                        {"label": "Reuters", "publisher": "Reuters", "title": "Enterprise agents story", "url": "https://example.com/reuters", "role": "source"},
                        {"label": "Bloomberg", "publisher": "Bloomberg", "title": "Automation market report", "url": "https://example.com/bloomberg", "role": "source"},
                        {"label": "The Verge", "publisher": "The Verge", "title": "Enterprise tooling piece", "url": "https://example.com/verge", "role": "source"},
                    ],
                }
            raise AssertionError(f"Unexpected model {model} with prompt: {user_prompt}")

    monkeypatch.setattr("core.operator.service.OpenRouterClient", FakeOpenRouterClient)

    try:
        result = execute_operator_command(
            {
                "type": "run_content_pipeline",
                "payload": {"domain": "ai-tech-business", "count": 1, "candidate_index": 0},
            }
        )

        assert result["decision"]["action"] == "auto_publish"
        assert result["article"]["status"] == "published"
        assert result["selected_candidate"]["sources"][0]["url"] == "https://example.com/reuters"
    finally:
        if database_path.exists():
            database_path.unlink()


def test_composite_pipeline_retries_source_enrichment_when_first_pass_is_incomplete(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-enrich-retry-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")
    monkeypatch.setenv("COREWIRE_MODEL_PROFILE", "balanced")
    monkeypatch.setenv("COREWIRE_LLM_ROUTER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")

    calls = {"enrich": 0}

    class FakeOpenRouterClient:
        def __init__(self, api_key: str) -> None:
            assert api_key == "test-openrouter-key"

        def complete_json(self, *, model: str, system_prompt: str, user_prompt: str) -> dict:
            if model == "perplexity/sonar-pro" and "Find" in user_prompt:
                return {
                    "shortlist": [
                        {
                            "title": "Enterprise AI stack matures",
                            "summary": "Enterprise AI moves toward backbone adoption.",
                            "why_it_matters": "This changes operating models.",
                            "source_count": 3,
                            "confidence": "high",
                            "sources": ["Reuters[1]", "Bloomberg[2]", "The Verge[3]"],
                        }
                    ]
                }
            if model == "perplexity/sonar-pro" and "Normalize and enrich" in user_prompt:
                calls["enrich"] += 1
                if calls["enrich"] == 1:
                    return {
                        "sources": [
                            {
                                "label": "Reuters",
                                "publisher": "Reuters",
                                "title": "Enterprise AI report",
                                "url": "https://example.com/reuters",
                                "role": "source",
                            },
                            {
                                "label": "Bloomberg",
                                "publisher": "Bloomberg",
                                "title": "Automation market report",
                                "url": None,
                                "role": "source",
                            },
                        ]
                    }
                return {
                    "sources": [
                        {
                            "label": "Reuters",
                            "publisher": "Reuters",
                            "title": "Enterprise AI report",
                            "url": "https://example.com/reuters",
                            "role": "source",
                        },
                        {
                            "label": "Bloomberg",
                            "publisher": "Bloomberg",
                            "title": "Automation market report",
                            "url": "https://example.com/bloomberg",
                            "role": "source",
                        },
                        {
                            "label": "The Verge",
                            "publisher": "The Verge",
                            "title": "Enterprise tooling piece",
                            "url": "https://example.com/verge",
                            "role": "source",
                        },
                    ]
                }
            if model == "anthropic/claude-sonnet-4.6":
                return {
                    "headline": "Enterprise AI stack matures",
                    "dek": "Dek",
                    "narrative": "Narrative",
                    "fact_blocks": [{"text": "Fact", "citations": ["Reuters", "Bloomberg", "The Verge"]}],
                    "analysis_blocks": [{"text": "Analysis"}],
                    "sources": [
                        {"label": "Reuters", "publisher": "Reuters", "title": "Enterprise AI report", "url": "https://example.com/reuters", "role": "source"},
                        {"label": "Bloomberg", "publisher": "Bloomberg", "title": "Automation market report", "url": "https://example.com/bloomberg", "role": "source"},
                        {"label": "The Verge", "publisher": "The Verge", "title": "Enterprise tooling piece", "url": "https://example.com/verge", "role": "source"},
                    ],
                }
            raise AssertionError(f"Unexpected model {model}")

    monkeypatch.setattr("core.operator.service.OpenRouterClient", FakeOpenRouterClient)

    try:
        result = execute_operator_command(
            {
                "type": "run_content_pipeline",
                "payload": {"domain": "ai-tech-business", "count": 1, "candidate_index": 0},
            }
        )

        assert calls["enrich"] == 2
        assert result["decision"]["action"] == "auto_publish"
        assert result["article"]["status"] == "published"
    finally:
        if database_path.exists():
            database_path.unlink()


def test_publish_gate_rejects_high_severity_editorial_flags(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-editorial-flags-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    try:
        result = execute_operator_command(
            {
                "type": "publish_if_eligible",
                "payload": {
                    "draft": {
                        "headline": "Mismatched source draft",
                        "dek": "Dek",
                        "fact_blocks": [{"text": "Fact", "citations": ["Reuters", "Bloomberg", "OpenAI"]}],
                        "analysis_blocks": [{"text": "Analysis"}],
                        "sources": [
                            {"label": "Reuters", "publisher": "Reuters", "title": "Enterprise AI report", "url": "https://example.com/reuters", "role": "article"},
                            {"label": "Bloomberg", "publisher": "Bloomberg", "title": "Automation market report", "url": "https://example.com/bloomberg", "role": "article"},
                            {"label": "OpenAI", "publisher": "OpenAI", "title": "Enterprise release notes", "url": "https://example.com/openai-release", "role": "official_release"},
                        ],
                        "editorial_flags": [
                            {
                                "severity": "high",
                                "message": "Sources do not corroborate the article topic.",
                            }
                        ],
                    },
                    "confidence": {"level": "high", "homepage_eligible": True},
                    "flags": [],
                    "story_tier": "standard",
                },
            }
        )

        assert result["decision"]["action"] == "review_required"
        assert "editorial_flag:high" in result["decision"]["reasons"]
        assert result["review_item"]["queue"] == "pending_drafts"
    finally:
        if database_path.exists():
            database_path.unlink()


def test_publish_gate_rejects_topically_mismatched_sources(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-source-topic-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    try:
        result = execute_operator_command(
            {
                "type": "publish_if_eligible",
                "payload": {
                    "draft": {
                        "headline": "AI Agents Are Becoming the New Enterprise Operating System",
                        "dek": "AI is shifting from copilots to enterprise orchestration.",
                        "fact_blocks": [{"text": "Fact", "citations": ["Source 1", "Source 2", "Source 3"]}],
                        "analysis_blocks": [{"text": "Analysis"}],
                        "sources": [
                            {"label": "1", "publisher": "SomaLogic", "title": "SomaScan Data Standardization and File Specification Technical Note", "url": "https://example.com/soma", "role": "article"},
                            {"label": "2", "publisher": "Psomagen", "title": "Data normalization and standardization", "url": "https://example.com/psomagen", "role": "article"},
                            {"label": "3", "publisher": "DigitalOcean", "title": "Database Normalization: 1NF, 2NF, 3NF and BCNF Examples", "url": "https://example.com/do", "role": "article"},
                        ],
                    },
                    "confidence": {"level": "high", "homepage_eligible": True},
                    "flags": [],
                    "story_tier": "standard",
                },
            }
        )

        assert result["decision"]["action"] == "review_required"
        assert "source_topic_mismatch" in result["decision"]["reasons"]
    finally:
        if database_path.exists():
            database_path.unlink()


def test_publish_gate_rejects_vendor_heavy_source_mix(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-source-authority-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    try:
        result = execute_operator_command(
            {
                "type": "publish_if_eligible",
                "payload": {
                    "draft": {
                        "headline": "Agentic AI moves into enterprise automation",
                        "dek": "Enterprises are adopting agentic AI for operations and workflow orchestration.",
                        "fact_blocks": [{"text": "Fact", "citations": ["CloudKeeper", "Beam AI", "Naviant", "Deloitte"]}],
                        "analysis_blocks": [{"text": "Analysis"}],
                        "sources": [
                            {"label": "CloudKeeper", "publisher": "CloudKeeper", "title": "Top Agentic AI Trends to Watch in 2026", "url": "https://www.cloudkeeper.com/insights/blog/top-agentic-ai-trends-watch-2026-how-ai-agents-are-redefining-enterprise-automation", "role": "source"},
                            {"label": "Beam AI", "publisher": "Beam AI", "title": "Why the Next Era of Agentic Automation Changes Everything", "url": "https://beam.ai/agentic-insights/ai-landscape-2026-why-the-era-of-agentic-automation-changes-everything", "role": "source"},
                            {"label": "Naviant", "publisher": "Naviant", "title": "2026 AI and Agentic Automation Trends", "url": "https://naviant.com/blog/ai-agentic-automation-trends/", "role": "source"},
                            {"label": "Deloitte", "publisher": "Deloitte", "title": "The agentic reality check", "url": "https://www.deloitte.com/us/en/insights/topics/technology-management/tech-trends/2026/agentic-ai-strategy.html", "role": "source"},
                        ],
                    },
                    "confidence": {"level": "high", "homepage_eligible": True},
                    "flags": [],
                    "story_tier": "standard",
                },
            }
        )

        assert result["decision"]["action"] == "review_required"
        assert "insufficient_source_authority" in result["decision"]["reasons"]
    finally:
        if database_path.exists():
            database_path.unlink()


def test_composite_pipeline_retries_when_enrichment_lacks_publisher_diversity(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-diversity-retry-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")
    monkeypatch.setenv("COREWIRE_MODEL_PROFILE", "balanced")
    monkeypatch.setenv("COREWIRE_LLM_ROUTER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")

    calls = {"enrich": 0}

    class FakeOpenRouterClient:
        def __init__(self, api_key: str) -> None:
            assert api_key == "test-openrouter-key"

        def complete_json(self, *, model: str, system_prompt: str, user_prompt: str) -> dict:
            if model == "perplexity/sonar-pro" and "Find" in user_prompt:
                return {
                    "shortlist": [
                        {
                            "title": "Enterprise AI stack matures",
                            "summary": "Enterprise AI moves toward backbone adoption.",
                            "why_it_matters": "This changes operating models.",
                            "source_count": 3,
                            "confidence": "high",
                            "sources": ["Reuters[1]", "Bloomberg[2]", "The Verge[3]"],
                        }
                    ]
                }
            if model == "perplexity/sonar-pro" and "Normalize and enrich" in user_prompt:
                calls["enrich"] += 1
                if calls["enrich"] == 1:
                    return {
                        "sources": [
                            {
                                "label": "IBM Think 1",
                                "publisher": "IBM",
                                "title": "Source one",
                                "url": "https://example.com/ibm-1",
                                "role": "source",
                            },
                            {
                                "label": "IBM Think 2",
                                "publisher": "IBM",
                                "title": "Source two",
                                "url": "https://example.com/ibm-2",
                                "role": "source",
                            },
                            {
                                "label": "IBM Think 3",
                                "publisher": "IBM",
                                "title": "Source three",
                                "url": "https://example.com/ibm-3",
                                "role": "source",
                            },
                        ]
                    }
                return {
                    "sources": [
                        {
                            "label": "Reuters",
                            "publisher": "Reuters",
                            "title": "Enterprise AI report",
                            "url": "https://example.com/reuters",
                            "role": "source",
                        },
                        {
                            "label": "Bloomberg",
                            "publisher": "Bloomberg",
                            "title": "Automation market report",
                            "url": "https://example.com/bloomberg",
                            "role": "source",
                        },
                        {
                            "label": "The Verge",
                            "publisher": "The Verge",
                            "title": "Enterprise tooling piece",
                            "url": "https://example.com/verge",
                            "role": "source",
                        },
                    ]
                }
            if model == "anthropic/claude-sonnet-4.6":
                return {
                    "headline": "Enterprise AI stack matures",
                    "dek": "Dek",
                    "narrative": "Narrative",
                    "fact_blocks": [{"text": "Fact", "citations": ["Reuters", "Bloomberg", "The Verge"]}],
                    "analysis_blocks": [{"text": "Analysis"}],
                    "sources": [
                        {"label": "Reuters", "publisher": "Reuters", "title": "Enterprise AI report", "url": "https://example.com/reuters", "role": "source"},
                        {"label": "Bloomberg", "publisher": "Bloomberg", "title": "Automation market report", "url": "https://example.com/bloomberg", "role": "source"},
                        {"label": "The Verge", "publisher": "The Verge", "title": "Enterprise tooling piece", "url": "https://example.com/verge", "role": "source"},
                    ],
                }
            raise AssertionError(f"Unexpected model {model}")

    monkeypatch.setattr("core.operator.service.OpenRouterClient", FakeOpenRouterClient)

    try:
        result = execute_operator_command(
            {
                "type": "run_content_pipeline",
                "payload": {"domain": "ai-tech-business", "count": 1, "candidate_index": 0},
            }
        )

        assert calls["enrich"] == 2
        assert result["decision"]["action"] == "auto_publish"
        assert result["article"]["status"] == "published"
        assert len({source["publisher"] for source in result["selected_candidate"]["sources"]}) == 3
    finally:
        if database_path.exists():
            database_path.unlink()


def test_composite_pipeline_retries_when_enrichment_returns_video_or_secondary_sources(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-primary-retry-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")
    monkeypatch.setenv("COREWIRE_MODEL_PROFILE", "balanced")
    monkeypatch.setenv("COREWIRE_LLM_ROUTER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")

    calls = {"enrich": 0}

    class FakeOpenRouterClient:
        def __init__(self, api_key: str) -> None:
            assert api_key == "test-openrouter-key"

        def complete_json(self, *, model: str, system_prompt: str, user_prompt: str) -> dict:
            if model == "perplexity/sonar-pro" and "Find" in user_prompt:
                return {
                    "shortlist": [
                        {
                            "title": "Enterprise AI stack matures",
                            "summary": "Enterprise AI moves toward backbone adoption.",
                            "why_it_matters": "This changes operating models.",
                            "source_count": 3,
                            "confidence": "high",
                            "sources": ["Reuters[1]", "Bloomberg[2]", "The Verge[3]"],
                        }
                    ]
                }
            if model == "perplexity/sonar-pro" and "Normalize and enrich" in user_prompt:
                calls["enrich"] += 1
                if calls["enrich"] == 1:
                    return {
                        "sources": [
                            {
                                "label": "YouTube clip",
                                "publisher": "YouTube",
                                "title": "Conference panel",
                                "url": "https://www.youtube.com/watch?v=abc",
                                "role": "source",
                            },
                            {
                                "label": "Industry blog",
                                "publisher": "Statworx",
                                "title": "AI trends report 2026",
                                "url": "https://www.statworx.com/en/content-hub/whitepaper/ai-trends-report-2026",
                                "role": "source",
                            },
                            {
                                "label": "Summit landing page",
                                "publisher": "The AI Summit",
                                "title": "Top trends",
                                "url": "https://london.theaisummit.com/news-insights/latest-news/",
                                "role": "source",
                            },
                        ]
                    }
                return {
                    "sources": [
                        {
                            "label": "Reuters",
                            "publisher": "Reuters",
                            "title": "Enterprise AI report",
                            "url": "https://example.com/reuters",
                            "role": "source",
                        },
                        {
                            "label": "Bloomberg",
                            "publisher": "Bloomberg",
                            "title": "Automation market report",
                            "url": "https://example.com/bloomberg",
                            "role": "source",
                        },
                        {
                            "label": "The Verge",
                            "publisher": "The Verge",
                            "title": "Enterprise tooling piece",
                            "url": "https://example.com/verge",
                            "role": "source",
                        },
                    ]
                }
            if model == "anthropic/claude-sonnet-4.6":
                return {
                    "headline": "Enterprise AI stack matures",
                    "dek": "Dek",
                    "narrative": "Narrative",
                    "fact_blocks": [{"text": "Fact", "citations": ["Reuters", "Bloomberg", "The Verge"]}],
                    "analysis_blocks": [{"text": "Analysis"}],
                    "sources": [
                        {"label": "Reuters", "publisher": "Reuters", "title": "Enterprise AI report", "url": "https://example.com/reuters", "role": "source"},
                        {"label": "Bloomberg", "publisher": "Bloomberg", "title": "Automation market report", "url": "https://example.com/bloomberg", "role": "source"},
                        {"label": "The Verge", "publisher": "The Verge", "title": "Enterprise tooling piece", "url": "https://example.com/verge", "role": "source"},
                    ],
                }
            raise AssertionError(f"Unexpected model {model}")

    monkeypatch.setattr("core.operator.service.OpenRouterClient", FakeOpenRouterClient)

    try:
        result = execute_operator_command(
            {
                "type": "run_content_pipeline",
                "payload": {"domain": "ai-tech-business", "count": 1, "candidate_index": 0},
            }
        )

        assert calls["enrich"] == 2
        assert result["decision"]["action"] == "auto_publish"
        assert result["article"]["status"] == "published"
        assert all("youtube.com" not in (source["url"] or "") for source in result["selected_candidate"]["sources"])
    finally:
        if database_path.exists():
            database_path.unlink()


def test_composite_pipeline_retries_when_enrichment_returns_only_secondary_sources(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-secondary-retry-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")
    monkeypatch.setenv("COREWIRE_MODEL_PROFILE", "balanced")
    monkeypatch.setenv("COREWIRE_LLM_ROUTER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")

    calls = {"enrich": 0}

    class FakeOpenRouterClient:
        def __init__(self, api_key: str) -> None:
            assert api_key == "test-openrouter-key"

        def complete_json(self, *, model: str, system_prompt: str, user_prompt: str) -> dict:
            if model == "perplexity/sonar-pro" and "Find" in user_prompt:
                return {
                    "shortlist": [
                        {
                            "title": "Enterprise AI stack matures",
                            "summary": "Enterprise AI moves toward backbone adoption.",
                            "why_it_matters": "This changes operating models.",
                            "source_count": 3,
                            "confidence": "high",
                            "sources": ["Reuters[1]", "Bloomberg[2]", "The Verge[3]"],
                        }
                    ]
                }
            if model == "perplexity/sonar-pro" and "Normalize and enrich" in user_prompt:
                calls["enrich"] += 1
                if calls["enrich"] == 1:
                    return {
                        "sources": [
                            {
                                "label": "Summit landing page",
                                "publisher": "The AI Summit",
                                "title": "Top trends",
                                "url": "https://london.theaisummit.com/news-insights/latest-news/",
                                "role": "event_page",
                            },
                            {
                                "label": "Vendor blog",
                                "publisher": "Vendor Insights",
                                "title": "AI trends for 2026",
                                "url": "https://vendor.example.com/blog/ai-trends-2026",
                                "role": "blog",
                            },
                            {
                                "label": "Newsletter recap",
                                "publisher": "Tech Briefing",
                                "title": "Weekly enterprise AI recap",
                                "url": "https://newsletter.example.com/enterprise-ai-recap",
                                "role": "newsletter",
                            },
                        ]
                    }
                return {
                    "sources": [
                        {
                            "label": "Reuters",
                            "publisher": "Reuters",
                            "title": "Enterprise AI report",
                            "url": "https://example.com/reuters",
                            "role": "article",
                        },
                        {
                            "label": "Bloomberg",
                            "publisher": "Bloomberg",
                            "title": "Automation market report",
                            "url": "https://example.com/bloomberg",
                            "role": "article",
                        },
                        {
                            "label": "OpenAI",
                            "publisher": "OpenAI",
                            "title": "Enterprise release notes",
                            "url": "https://example.com/openai-release",
                            "role": "official_release",
                        },
                    ]
                }
            if model == "anthropic/claude-sonnet-4.6":
                return {
                    "headline": "Enterprise AI stack matures",
                    "dek": "Dek",
                    "narrative": "Narrative",
                    "fact_blocks": [{"text": "Fact", "citations": ["Reuters", "Bloomberg", "OpenAI"]}],
                    "analysis_blocks": [{"text": "Analysis"}],
                    "sources": [
                        {"label": "Reuters", "publisher": "Reuters", "title": "Enterprise AI report", "url": "https://example.com/reuters", "role": "article"},
                        {"label": "Bloomberg", "publisher": "Bloomberg", "title": "Automation market report", "url": "https://example.com/bloomberg", "role": "article"},
                        {"label": "OpenAI", "publisher": "OpenAI", "title": "Enterprise release notes", "url": "https://example.com/openai-release", "role": "official_release"},
                    ],
                }
            raise AssertionError(f"Unexpected model {model}")

    monkeypatch.setattr("core.operator.service.OpenRouterClient", FakeOpenRouterClient)

    try:
        result = execute_operator_command(
            {
                "type": "run_content_pipeline",
                "payload": {"domain": "ai-tech-business", "count": 1, "candidate_index": 0},
            }
        )

        assert calls["enrich"] == 2
        assert result["decision"]["action"] == "auto_publish"
        assert result["article"]["status"] == "published"
        assert {source["role"] for source in result["selected_candidate"]["sources"]} == {
            "article",
            "official_release",
        }
    finally:
        if database_path.exists():
            database_path.unlink()


def test_composite_pipeline_retries_when_enrichment_returns_topically_mismatched_sources(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-topic-retry-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")
    monkeypatch.setenv("COREWIRE_MODEL_PROFILE", "balanced")
    monkeypatch.setenv("COREWIRE_LLM_ROUTER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")

    calls = {"enrich": 0}

    class FakeOpenRouterClient:
        def __init__(self, api_key: str) -> None:
            assert api_key == "test-openrouter-key"

        def complete_json(self, *, model: str, system_prompt: str, user_prompt: str) -> dict:
            if model == "perplexity/sonar-pro" and "Find" in user_prompt:
                return {
                    "shortlist": [
                        {
                            "title": "AI Agents Evolve into Enterprise Orchestrators",
                            "summary": "Enterprises are moving from copilots to coordinated agent systems.",
                            "why_it_matters": "This changes how software and operations are automated.",
                            "source_count": 3,
                            "confidence": "high",
                            "sources": ["1", "2", "3"],
                        }
                    ]
                }
            if model == "perplexity/sonar-pro" and "Normalize and enrich" in user_prompt:
                calls["enrich"] += 1
                if calls["enrich"] == 1:
                    return {
                        "sources": [
                            {
                                "label": "1",
                                "publisher": "SomaLogic",
                                "title": "SomaScan Data Standardization and File Specification Technical Note",
                                "url": "https://example.com/soma",
                                "role": "article",
                            },
                            {
                                "label": "2",
                                "publisher": "Psomagen",
                                "title": "Data normalization and standardization",
                                "url": "https://example.com/psomagen",
                                "role": "article",
                            },
                            {
                                "label": "3",
                                "publisher": "DigitalOcean",
                                "title": "Database Normalization: 1NF, 2NF, 3NF and BCNF Examples",
                                "url": "https://example.com/do",
                                "role": "article",
                            },
                        ]
                    }
                return {
                    "sources": [
                        {
                            "label": "Reuters",
                            "publisher": "Reuters",
                            "title": "Enterprise AI agents move from copilots to orchestrators",
                            "url": "https://example.com/reuters",
                            "role": "article",
                        },
                        {
                            "label": "Bloomberg",
                            "publisher": "Bloomberg",
                            "title": "Agentic automation enters enterprise operations",
                            "url": "https://example.com/bloomberg",
                            "role": "article",
                        },
                        {
                            "label": "OpenAI",
                            "publisher": "OpenAI",
                            "title": "Release notes for enterprise agent workflows",
                            "url": "https://example.com/openai",
                            "role": "official_release",
                        },
                    ]
                }
            if model == "anthropic/claude-sonnet-4.6":
                return {
                    "headline": "AI agents move into enterprise orchestration",
                    "dek": "Dek",
                    "narrative": "Narrative",
                    "fact_blocks": [{"text": "Fact", "citations": ["Reuters", "Bloomberg", "OpenAI"]}],
                    "analysis_blocks": [{"text": "Analysis"}],
                    "sources": [
                        {"label": "Reuters", "publisher": "Reuters", "title": "Enterprise AI agents move from copilots to orchestrators", "url": "https://example.com/reuters", "role": "article"},
                        {"label": "Bloomberg", "publisher": "Bloomberg", "title": "Agentic automation enters enterprise operations", "url": "https://example.com/bloomberg", "role": "article"},
                        {"label": "OpenAI", "publisher": "OpenAI", "title": "Release notes for enterprise agent workflows", "url": "https://example.com/openai", "role": "official_release"},
                    ],
                }
            raise AssertionError(f"Unexpected model {model}")

    monkeypatch.setattr("core.operator.service.OpenRouterClient", FakeOpenRouterClient)

    try:
        result = execute_operator_command(
            {
                "type": "run_content_pipeline",
                "payload": {"domain": "ai-tech-business", "count": 1, "candidate_index": 0},
            }
        )

        assert calls["enrich"] == 2
        assert result["decision"]["action"] == "auto_publish"
        assert result["article"]["status"] == "published"
        assert all("normalization" not in (source["title"] or "").lower() for source in result["selected_candidate"]["sources"])
    finally:
        if database_path.exists():
            database_path.unlink()


def test_composite_pipeline_retries_when_enrichment_returns_vendor_heavy_sources(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-authority-retry-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")
    monkeypatch.setenv("COREWIRE_MODEL_PROFILE", "balanced")
    monkeypatch.setenv("COREWIRE_LLM_ROUTER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")

    calls = {"enrich": 0}

    class FakeOpenRouterClient:
        def __init__(self, api_key: str) -> None:
            assert api_key == "test-openrouter-key"

        def complete_json(self, *, model: str, system_prompt: str, user_prompt: str) -> dict:
            if model == "perplexity/sonar-pro" and "Find" in user_prompt:
                return {
                    "shortlist": [
                        {
                            "title": "Agentic AI moves into enterprise automation",
                            "summary": "Agentic systems are shifting from copilots to workflow orchestration.",
                            "why_it_matters": "This changes how operations teams automate enterprise work.",
                            "source_count": 4,
                            "confidence": "high",
                            "sources": ["1", "2", "3", "4"],
                        }
                    ]
                }
            if model == "perplexity/sonar-pro" and "Normalize and enrich" in user_prompt:
                calls["enrich"] += 1
                if calls["enrich"] == 1:
                    return {
                        "sources": [
                            {"label": "CloudKeeper", "publisher": "CloudKeeper", "title": "Top Agentic AI Trends to Watch in 2026", "url": "https://www.cloudkeeper.com/insights/blog/top-agentic-ai-trends-watch-2026-how-ai-agents-are-redefining-enterprise-automation", "role": "source"},
                            {"label": "Beam AI", "publisher": "Beam AI", "title": "Why the Next Era of Agentic Automation Changes Everything", "url": "https://beam.ai/agentic-insights/ai-landscape-2026-why-the-era-of-agentic-automation-changes-everything", "role": "source"},
                            {"label": "Naviant", "publisher": "Naviant", "title": "2026 AI and Agentic Automation Trends", "url": "https://naviant.com/blog/ai-agentic-automation-trends/", "role": "source"},
                            {"label": "Deloitte", "publisher": "Deloitte", "title": "The agentic reality check", "url": "https://www.deloitte.com/us/en/insights/topics/technology-management/tech-trends/2026/agentic-ai-strategy.html", "role": "source"},
                        ]
                    }
                return {
                    "sources": [
                        {"label": "Reuters", "publisher": "Reuters", "title": "Enterprise AI agents move from copilots to orchestrators", "url": "https://example.com/reuters", "role": "article"},
                        {"label": "Bloomberg", "publisher": "Bloomberg", "title": "Agentic automation enters enterprise operations", "url": "https://example.com/bloomberg", "role": "article"},
                        {"label": "Deloitte", "publisher": "Deloitte", "title": "The agentic reality check", "url": "https://www.deloitte.com/us/en/insights/topics/technology-management/tech-trends/2026/agentic-ai-strategy.html", "role": "research_report"},
                        {"label": "OpenAI", "publisher": "OpenAI", "title": "Enterprise agent workflow release notes", "url": "https://example.com/openai", "role": "official_release"},
                    ]
                }
            if model == "anthropic/claude-sonnet-4.6":
                return {
                    "headline": "Agentic AI moves into enterprise automation",
                    "dek": "Dek",
                    "narrative": "Narrative",
                    "fact_blocks": [{"text": "Fact", "citations": ["Reuters", "Bloomberg", "Deloitte", "OpenAI"]}],
                    "analysis_blocks": [{"text": "Analysis"}],
                    "sources": [
                        {"label": "Reuters", "publisher": "Reuters", "title": "Enterprise AI agents move from copilots to orchestrators", "url": "https://example.com/reuters", "role": "article"},
                        {"label": "Bloomberg", "publisher": "Bloomberg", "title": "Agentic automation enters enterprise operations", "url": "https://example.com/bloomberg", "role": "article"},
                        {"label": "Deloitte", "publisher": "Deloitte", "title": "The agentic reality check", "url": "https://www.deloitte.com/us/en/insights/topics/technology-management/tech-trends/2026/agentic-ai-strategy.html", "role": "research_report"},
                        {"label": "OpenAI", "publisher": "OpenAI", "title": "Enterprise agent workflow release notes", "url": "https://example.com/openai", "role": "official_release"},
                    ],
                }
            raise AssertionError(f"Unexpected model {model}")

    monkeypatch.setattr("core.operator.service.OpenRouterClient", FakeOpenRouterClient)

    try:
        result = execute_operator_command(
            {
                "type": "run_content_pipeline",
                "payload": {"domain": "ai-tech-business", "count": 1, "candidate_index": 0},
            }
        )

        assert calls["enrich"] == 2
        assert result["decision"]["action"] == "auto_publish"
        assert result["article"]["status"] == "published"
        assert {source["publisher"] for source in result["selected_candidate"]["sources"]} >= {
            "Reuters",
            "Bloomberg",
            "Deloitte",
            "OpenAI",
        }
    finally:
        if database_path.exists():
            database_path.unlink()


def test_composite_pipeline_prefers_target_publishers_during_strict_enrichment(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-preferred-publishers-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")
    monkeypatch.setenv("COREWIRE_MODEL_PROFILE", "balanced")
    monkeypatch.setenv("COREWIRE_LLM_ROUTER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")

    captured_strict_prompt = {"value": ""}

    class FakeOpenRouterClient:
        def __init__(self, api_key: str) -> None:
            assert api_key == "test-openrouter-key"

        def complete_json(self, *, model: str, system_prompt: str, user_prompt: str) -> dict:
            if model == "perplexity/sonar-pro" and "Find" in user_prompt:
                return {
                    "shortlist": [
                        {
                            "title": "Agentic AI moves into enterprise automation",
                            "summary": "Agentic systems are shifting from copilots to workflow orchestration.",
                            "why_it_matters": "This changes how operations teams automate enterprise work.",
                            "source_count": 4,
                            "confidence": "high",
                            "sources": ["1", "2", "3", "4"],
                        }
                    ]
                }
            if model == "perplexity/sonar-pro" and "Normalize and enrich" in user_prompt:
                if "Return only sources with real URLs." in user_prompt:
                    captured_strict_prompt["value"] = user_prompt
                    return {
                        "sources": [
                            {"label": "Reuters", "publisher": "Reuters", "title": "Enterprise AI agents move from copilots to orchestrators", "url": "https://example.com/reuters", "role": "article"},
                            {"label": "Bloomberg", "publisher": "Bloomberg", "title": "Agentic automation enters enterprise operations", "url": "https://example.com/bloomberg", "role": "article"},
                            {"label": "Deloitte", "publisher": "Deloitte", "title": "The agentic reality check", "url": "https://www.deloitte.com/us/en/insights/topics/technology-management/tech-trends/2026/agentic-ai-strategy.html", "role": "research_report"},
                            {"label": "OpenAI", "publisher": "OpenAI", "title": "Enterprise agent workflow release notes", "url": "https://example.com/openai", "role": "official_release"},
                        ]
                    }
                return {
                    "sources": [
                        {"label": "CloudKeeper", "publisher": "CloudKeeper", "title": "Top Agentic AI Trends to Watch in 2026", "url": "https://www.cloudkeeper.com/insights/blog/top-agentic-ai-trends-watch-2026-how-ai-agents-are-redefining-enterprise-automation", "role": "source"},
                        {"label": "Beam AI", "publisher": "Beam AI", "title": "Why the Next Era of Agentic Automation Changes Everything", "url": "https://beam.ai/agentic-insights/ai-landscape-2026-why-the-era-of-agentic-automation-changes-everything", "role": "source"},
                        {"label": "Naviant", "publisher": "Naviant", "title": "2026 AI and Agentic Automation Trends", "url": "https://naviant.com/blog/ai-agentic-automation-trends/", "role": "source"},
                    ]
                }
            if model == "anthropic/claude-sonnet-4.6":
                return {
                    "headline": "Agentic AI moves into enterprise automation",
                    "dek": "Dek",
                    "narrative": "Narrative",
                    "fact_blocks": [{"text": "Fact", "citations": ["Reuters", "Bloomberg", "Deloitte", "OpenAI"]}],
                    "analysis_blocks": [{"text": "Analysis"}],
                    "sources": [
                        {"label": "Reuters", "publisher": "Reuters", "title": "Enterprise AI agents move from copilots to orchestrators", "url": "https://example.com/reuters", "role": "article"},
                        {"label": "Bloomberg", "publisher": "Bloomberg", "title": "Agentic automation enters enterprise operations", "url": "https://example.com/bloomberg", "role": "article"},
                        {"label": "Deloitte", "publisher": "Deloitte", "title": "The agentic reality check", "url": "https://www.deloitte.com/us/en/insights/topics/technology-management/tech-trends/2026/agentic-ai-strategy.html", "role": "research_report"},
                        {"label": "OpenAI", "publisher": "OpenAI", "title": "Enterprise agent workflow release notes", "url": "https://example.com/openai", "role": "official_release"},
                    ],
                }
            raise AssertionError(f"Unexpected model {model}")

    monkeypatch.setattr("core.operator.service.OpenRouterClient", FakeOpenRouterClient)

    try:
        result = execute_operator_command(
            {
                "type": "run_content_pipeline",
                "payload": {"domain": "ai-tech-business", "count": 1, "candidate_index": 0},
            }
        )

        assert result["decision"]["action"] == "auto_publish"
        assert "Reuters" in captured_strict_prompt["value"]
        assert "Bloomberg" in captured_strict_prompt["value"]
        assert "official releases" in captured_strict_prompt["value"]
        assert "research institutions" in captured_strict_prompt["value"]
    finally:
        if database_path.exists():
            database_path.unlink()


def test_openrouter_client_uses_text_response_format_for_provider_compatibility(monkeypatch):
    captured_request: dict = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return (
                b'{"choices":[{"message":{"content":"{\\"shortlist\\": []}"}}]}'
            )

    def fake_urlopen(req, timeout):
        captured_request["body"] = req.data.decode("utf-8")
        return FakeResponse()

    monkeypatch.setattr("core.operator.service.request.urlopen", fake_urlopen)

    client = OpenRouterClient("test-openrouter-key")
    client.complete_json(
        model="perplexity/sonar-pro",
        system_prompt="Return JSON.",
        user_prompt="Find AI stories.",
    )

    assert '"response_format"' not in captured_request["body"]


def test_openrouter_client_extracts_json_from_fenced_code_blocks(monkeypatch):
    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return (
                b'{"choices":[{"message":{"content":"```json\\n{\\"shortlist\\":[{\\"title\\":\\"Trend A\\"}]}\\n```"}}]}'
            )

    def fake_urlopen(req, timeout):
        return FakeResponse()

    monkeypatch.setattr("core.operator.service.request.urlopen", fake_urlopen)

    client = OpenRouterClient("test-openrouter-key")
    result = client.complete_json(
        model="perplexity/sonar-pro",
        system_prompt="Return JSON.",
        user_prompt="Find AI stories.",
    )

    assert result["shortlist"][0]["title"] == "Trend A"


def test_run_content_pipeline_uses_analysis_engine_for_analysis_content(monkeypatch):
    called = {
        "dossier": False,
        "actors": False,
        "thesis": False,
        "writer": False,
        "extract": False,
        "doctrine": False,
    }
    candidate = {
        "title": "Middle East war analysis",
        "summary": "Escalation is reshaping energy and diplomacy.",
        "why_it_matters": "The conflict is altering global risk pricing.",
        "sources": [
            {"publisher": "AP", "url": "https://example.com/ap"},
            {"publisher": "Reuters", "url": "https://example.com/reuters"},
            {"publisher": "IEA", "url": "https://example.com/iea"},
        ],
        "actors": [
            {"name": "Iran", "goal": "raise the cost of war"},
            {"name": "United States", "goal": "force strategic concessions"},
        ],
    }

    monkeypatch.setattr(
        operator_service,
        "discover_trending_story",
        lambda payload: {"shortlist": [candidate], "profile": "balanced"},
    )
    monkeypatch.setattr(operator_service, "enrich_candidate_sources", lambda selected: selected)

    def fail_legacy_draft(*args, **kwargs):
        raise AssertionError("legacy build_story_draft path should not run for analysis content")

    monkeypatch.setattr(operator_service, "build_story_draft", fail_legacy_draft)

    def fake_dossier(selected_candidate):
        called["dossier"] = True
        assert selected_candidate["title"] == candidate["title"]
        return {
            "topic": selected_candidate["title"],
            "verified_facts": [selected_candidate["summary"]],
            "claims": [],
            "sources": selected_candidate["sources"],
            "unknowns": ["Whether escalation is sustainable."],
        }

    def fake_actor_map(dossier, actors):
        called["actors"] = True
        assert actors == candidate["actors"]
        return [{"name": actor["name"], "goal": actor["goal"]} for actor in actors]

    def fake_thesis(dossier, actor_map):
        called["thesis"] = True
        return "The war is being fought to change the region's cost structure because pressure alone has failed."

    def fake_writer(dossier, actor_map, thesis):
        called["writer"] = True
        return {
            "thesis": thesis,
            "known_facts": dossier["verified_facts"],
            "actor_map": actor_map,
            "obscured_layer": ["Infrastructure coercion matters more than battlefield optics."],
            "next_moves": ["Maritime pressure is likely to continue."],
            "unknowns": dossier["unknowns"],
            "full_article": "A" * 2000,
        }

    def fake_extract(article):
        called["extract"] = True
        return {
            "fact_blocks": [{"text": "Shipping disruption is spreading.", "citations": []}],
            "analysis_blocks": [{"text": "Energy leverage has become the main theater."}],
            "disagreements": ["Whether deterrence will hold."],
        }

    def fake_doctrine(article):
        called["doctrine"] = True
        return {"passed": True, "violations": []}

    def fake_evaluation(article, doctrine):
        assert doctrine == {"passed": True, "violations": []}
        return {
            "decision": "accept",
            "passed": True,
            "scores": {
                "thesis_strength": 3,
                "why_explanation": 3,
                "new_value": 3,
                "actor_map_quality": 3,
                "fact_claim_discipline": 2,
                "agenda_resistance": 2,
                "tone_corewire_identity": 2,
            },
        }

    def fake_publish(payload, *, correlation):
        assert payload["draft"]["thesis"].startswith("The war is being fought")
        assert payload["draft"]["full_article"] == "A" * 2000
        assert payload["draft"]["fact_blocks"]
        assert payload["draft"]["analysis_blocks"]
        return {
            "type": "publish_if_eligible",
            "accepted": True,
            "decision": {"action": "auto_publish", "reasons": []},
            "article": {"slug": "analysis-slug", "status": "published"},
            "correlation": correlation,
        }

    monkeypatch.setattr(
        operator_service,
        "analysis_dossier",
        SimpleNamespace(build_research_dossier=fake_dossier),
        raising=False,
    )
    monkeypatch.setattr(
        operator_service,
        "analysis_actors",
        SimpleNamespace(build_actor_map=fake_actor_map),
        raising=False,
    )
    monkeypatch.setattr(
        operator_service,
        "analysis_thesis",
        SimpleNamespace(form_analysis_thesis=fake_thesis),
        raising=False,
    )
    monkeypatch.setattr(
        operator_service,
        "analysis_writer",
        SimpleNamespace(generate_flagship_analysis=fake_writer),
        raising=False,
    )
    monkeypatch.setattr(
        operator_service,
        "analysis_extraction",
        SimpleNamespace(extract_analysis_sections=fake_extract),
        raising=False,
    )
    monkeypatch.setattr(
        operator_service,
        "analysis_doctrine",
        SimpleNamespace(validate_analysis_doctrine=fake_doctrine),
        raising=False,
    )
    monkeypatch.setattr(
        operator_service,
        "analysis_evaluation",
        SimpleNamespace(score_analysis_output=fake_evaluation),
        raising=False,
    )
    monkeypatch.setattr(operator_service, "publish_if_eligible", fake_publish)

    result = operator_service.run_content_pipeline(
        {"content_type": "analysis", "domain": "politics-diplomacy"},
        correlation={},
    )

    assert called["dossier"] is True
    assert called["actors"] is True
    assert called["thesis"] is True
    assert called["writer"] is True
    assert called["extract"] is True
    assert called["doctrine"] is True
    assert result["draft"]["headline"] == candidate["title"]
    assert result["evaluation"]["decision"] == "accept"
    assert result["decision"]["action"] == "auto_publish"


def test_run_content_pipeline_routes_shallow_analysis_to_review(monkeypatch):
    candidate = {
        "title": "Middle East war analysis",
        "summary": "Escalation is reshaping energy and diplomacy.",
        "why_it_matters": "The conflict is altering global risk pricing.",
        "sources": [
            {"publisher": "AP", "url": "https://example.com/ap"},
            {"publisher": "Reuters", "url": "https://example.com/reuters"},
            {"publisher": "IEA", "url": "https://example.com/iea"},
        ],
        "actors": [
            {"name": "Iran", "goal": "raise the cost of war"},
            {"name": "United States", "goal": "force strategic concessions"},
        ],
    }

    monkeypatch.setattr(
        operator_service,
        "discover_trending_story",
        lambda payload: {"shortlist": [candidate], "profile": "balanced"},
    )
    monkeypatch.setattr(operator_service, "enrich_candidate_sources", lambda selected: selected)

    monkeypatch.setattr(
        operator_service,
        "analysis_dossier",
        SimpleNamespace(
            build_research_dossier=lambda selected_candidate: {
                "topic": selected_candidate["title"],
                "verified_facts": [selected_candidate["summary"]],
                "claims": [],
                "sources": selected_candidate["sources"],
                "unknowns": ["Whether escalation is sustainable."],
            }
        ),
        raising=False,
    )
    monkeypatch.setattr(
        operator_service,
        "analysis_actors",
        SimpleNamespace(
            build_actor_map=lambda dossier, actors: [
                {"name": actor["name"], "goal": actor["goal"]} for actor in actors
            ]
        ),
        raising=False,
    )
    monkeypatch.setattr(
        operator_service,
        "analysis_thesis",
        SimpleNamespace(
            form_analysis_thesis=lambda dossier, actor_map: (
                "The war is being fought to change the region's cost structure because pressure alone has failed."
            )
        ),
        raising=False,
    )
    monkeypatch.setattr(
        operator_service,
        "analysis_writer",
        SimpleNamespace(
            generate_flagship_analysis=lambda dossier, actor_map, thesis: {
                "thesis": thesis,
                "known_facts": dossier["verified_facts"],
                "actor_map": actor_map,
                "obscured_layer": ["A thin hidden-layer sentence."],
                "next_moves": ["Maritime pressure is likely to continue."],
                "unknowns": dossier["unknowns"],
                "full_article": "Short analysis body.",
            }
        ),
        raising=False,
    )
    monkeypatch.setattr(
        operator_service,
        "analysis_extraction",
        SimpleNamespace(
            extract_analysis_sections=lambda article: {
                "fact_blocks": [{"text": "Shipping disruption is spreading.", "citations": []}],
                "analysis_blocks": [{"text": "A thin hidden-layer sentence."}],
                "disagreements": ["Whether deterrence will hold."],
            }
        ),
        raising=False,
    )
    monkeypatch.setattr(
        operator_service,
        "analysis_doctrine",
        SimpleNamespace(
            validate_analysis_doctrine=lambda article: {
                "passed": False,
                "violations": ["thin_full_article", "thin_hidden_layer", "thin_consequence_layer"],
            }
        ),
        raising=False,
    )
    monkeypatch.setattr(
        operator_service,
        "analysis_evaluation",
        SimpleNamespace(
            score_analysis_output=lambda article, doctrine: {
                "decision": "rerun",
                "passed": False,
                "scores": {
                    "thesis_strength": 3,
                    "why_explanation": 2,
                    "new_value": 1,
                    "actor_map_quality": 2,
                    "fact_claim_discipline": 2,
                    "agenda_resistance": 2,
                    "tone_corewire_identity": 1,
                },
            }
        ),
        raising=False,
    )

    def fake_publish(payload, *, correlation):
        assert "doctrine:thin_full_article" in payload["flags"]
        assert "doctrine:thin_hidden_layer" in payload["flags"]
        assert "doctrine:thin_consequence_layer" in payload["flags"]
        return {
            "type": "publish_if_eligible",
            "accepted": True,
            "decision": {
                "action": "review_required",
                "reasons": [
                    "flag:doctrine:thin_full_article",
                    "flag:doctrine:thin_hidden_layer",
                    "flag:doctrine:thin_consequence_layer",
                ],
            },
            "review_item": {"id": "review-1", "headline": candidate["title"], "queue": "pending_drafts"},
            "correlation": correlation,
        }

    monkeypatch.setattr(operator_service, "publish_if_eligible", fake_publish)

    result = operator_service.run_content_pipeline(
        {"content_type": "analysis", "domain": "politics-diplomacy"},
        correlation={},
    )

    assert result["doctrine"]["violations"] == [
        "thin_full_article",
        "thin_hidden_layer",
        "thin_consequence_layer",
    ]
    assert result["evaluation"]["decision"] == "rerun"
    assert result["decision"]["action"] == "review_required"


def test_operator_command_preserves_paperclip_correlation_metadata(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-corr-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    try:
        result = execute_operator_command(
            {
                "type": "publish_preview_article",
                "ticket_id": "ticket-456",
                "actor_id": "paperclip-agent-1",
                "company_id": "acme-corp",
                "correlation_id": "corr-abc",
                "requested_by": "editorial-workflow",
                "payload": {
                    "draft": {
                        "headline": "Correlation test article",
                        "dek": "Testing correlation fields",
                        "fact_blocks": [{"statement": "Fact", "sources": ["Reuters"]}],
                        "analysis_blocks": [{"analysis": "Analysis"}],
                        "sources": [{"organization": "Reuters", "url": "https://reuters.com/test"}],
                    },
                    "confidence": {"level": "high", "homepage_eligible": True},
                    "story_tier": "standard",
                    "requested_profile": "balanced",
                    "effective_profile": "balanced",
                },
            }
        )

        assert result["accepted"] is True
        assert result["correlation"]["ticket_id"] == "ticket-456"
        assert result["correlation"]["actor_id"] == "paperclip-agent-1"
        assert result["correlation"]["company_id"] == "acme-corp"
        assert result["correlation"]["correlation_id"] == "corr-abc"
        assert result["correlation"]["requested_by"] == "editorial-workflow"
    finally:
        if database_path.exists():
            database_path.unlink()


def test_operator_command_import_external_draft_routes_to_review(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-operator-import-{uuid.uuid4().hex}.db"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    try:
        result = execute_operator_command(
            {
                "type": "import_external_draft",
                "ticket_id": "ticket-ext-1",
                "actor_id": "paperclip-agent-2",
                "requested_by": "content-bridge",
                "payload": {
                    "draft": {
                        "headline": "External draft headline",
                        "dek": "Imported from Paperclip",
                        "fact_blocks": [{"statement": "External fact", "sources": ["AP"]}],
                        "analysis_blocks": [{"analysis": "External analysis"}],
                        "sources": [
                            {"organization": "AP", "url": "https://apnews.com/test"},
                            {"organization": "Reuters", "url": "https://reuters.com/test2"},
                            {"organization": "BBC", "url": "https://bbc.com/test3"},
                        ],
                    },
                    "confidence": {"level": "medium", "homepage_eligible": False},
                },
            }
        )

        assert result["type"] == "import_external_draft"
        assert result["accepted"] is True
        assert "review_item" in result
        assert result["review_item"]["queue"] in ("pending_drafts", "flagged_items")
        assert result["correlation"]["ticket_id"] == "ticket-ext-1"
        assert result["correlation"]["requested_by"] == "content-bridge"
    finally:
        if database_path.exists():
            database_path.unlink()
