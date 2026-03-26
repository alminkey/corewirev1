import json
import re
import uuid
from datetime import UTC, datetime
from urllib import request

from core.config import Settings
from core.db.base import Base
from core.db.session import build_engine, build_session_factory
from core.llm.router import resolve_agent_model
from core.articles.schemas import ArticleSource
from core.repositories.articles import ArticleRepository
from core.repositories.stories import StoryRepository


class OpenRouterClient:
    api_url = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def complete_json(self, *, model: str, system_prompt: str, user_prompt: str) -> dict:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        http_request = request.Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with request.urlopen(http_request, timeout=60) as response:
            response_payload = json.loads(response.read().decode("utf-8"))

        message = response_payload["choices"][0]["message"]["content"]
        if isinstance(message, list):
            message = "".join(part.get("text", "") for part in message if isinstance(part, dict))
        return _parse_json_content(message)


def execute_operator_command(command: dict) -> dict:
    command_type = command.get("type")
    payload = command.get("payload", {})
    correlation = {
        "ticket_id": command.get("ticket_id"),
        "actor_id": command.get("actor_id"),
        "company_id": command.get("company_id"),
        "correlation_id": command.get("correlation_id"),
    }

    if command_type == "discover_trending_story":
        return {**discover_trending_story(payload), "correlation": correlation}

    if command_type == "build_story_draft":
        return {**build_story_draft(payload), "correlation": correlation}

    if command_type == "run_content_pipeline":
        return run_content_pipeline(payload, correlation=correlation)

    if command_type == "publish_preview_article":
        return publish_preview_article(payload, correlation=correlation)

    if command_type == "publish_article":
        return publish_article(payload, correlation=correlation)

    if command_type == "publish_if_eligible":
        return publish_if_eligible(payload, correlation=correlation)

    if command_type == "archive_preview_article":
        return archive_preview_article(payload, correlation=correlation)

    if command_type == "rerun_story":
        return {
            "type": "rerun_story",
            "accepted": True,
            "payload": payload,
            "correlation": correlation,
        }

    return {
        "type": command_type,
        "accepted": True,
        "payload": payload,
        "correlation": correlation,
    }


def discover_trending_story(payload: dict) -> dict:
    settings = Settings.from_env()
    research_model = resolve_agent_model("research")
    client = OpenRouterClient(settings.openrouter_api_key or "")
    result = client.complete_json(
        model=research_model["model"],
        system_prompt=(
            "You are a newsroom research agent. Return only JSON. "
            "Recommend corroborated AI, tech, or business stories suitable for a premium explain/report."
        ),
        user_prompt=(
            f"Find {payload.get('count', 3)} trending stories in the domain "
            f"{payload.get('domain', 'ai-tech-business')}. "
            "Only include candidates with at least 2-3 independent sources. "
            "Return JSON with a shortlist array. Each item must include "
            "title, summary, why_it_matters, source_count, confidence, and sources."
        ),
    )
    shortlist = []
    for candidate in result.get("shortlist", []):
        shortlist.append(
            {
                **candidate,
                "sources": [_normalize_source(source) for source in candidate.get("sources", [])],
            }
        )

    return {
        "type": "discover_trending_story",
        "accepted": True,
        "router": settings.llm_router,
        "profile": settings.model_profile,
        "models": {"research": research_model["model"]},
        "shortlist": shortlist,
    }


def build_story_draft(payload: dict) -> dict:
    settings = Settings.from_env()
    writer_model = resolve_agent_model("writer")
    validator_model = resolve_agent_model("validator")
    client = OpenRouterClient(settings.openrouter_api_key or "")
    candidate = payload.get("candidate", {})
    result = client.complete_json(
        model=writer_model["model"],
        system_prompt=(
            "You are a premium newsroom writer. Return only JSON. "
            "Write a natural, connected explain/report with clear separation between facts and analysis."
        ),
        user_prompt=(
            "Build a full_report draft from this corroborated candidate:\n"
            f"{json.dumps(candidate)}\n"
            "Return JSON with headline, dek, narrative, fact_blocks, analysis_blocks, and sources."
        ),
    )
    normalized_draft = {
        **result,
        "sources": [_normalize_source(source) for source in result.get("sources", [])],
    }
    return {
        "type": "build_story_draft",
        "accepted": True,
        "router": settings.llm_router,
        "profile": settings.model_profile,
        "models": {
            "writer": writer_model["model"],
            "validator": validator_model["model"],
        },
        "draft": normalized_draft,
    }


def enrich_candidate_sources(candidate: dict) -> dict:
    settings = Settings.from_env()
    research_model = resolve_agent_model("research")
    client = OpenRouterClient(settings.openrouter_api_key or "")

    if all(
        isinstance(source, dict) and source.get("url")
        for source in candidate.get("sources", [])
    ) and not _needs_source_enrichment_retry(
        candidate,
        [_normalize_source(source) for source in candidate.get("sources", [])]
    ):
        return candidate

    enriched_sources = _run_source_enrichment_pass(
        client=client,
        model=research_model["model"],
        source_references=candidate.get("sources", []),
        candidate_context=_candidate_context(candidate),
        strict=False,
    )

    if _needs_source_enrichment_retry(candidate, enriched_sources):
        enriched_sources = _run_source_enrichment_pass(
            client=client,
            model=research_model["model"],
            source_references=candidate.get("sources", []),
            candidate_context=_candidate_context(candidate),
            strict=True,
        )

    return {
        **candidate,
        "sources": enriched_sources,
    }


def run_content_pipeline(payload: dict, *, correlation: dict) -> dict:
    shortlist_result = discover_trending_story(
        {
            "domain": payload.get("domain", "ai-tech-business"),
            "count": payload.get("count", 3),
        }
    )
    shortlist = shortlist_result.get("shortlist", [])
    candidate_index = payload.get("candidate_index", 0)
    selected_candidate = enrich_candidate_sources(shortlist[candidate_index])

    draft_result = build_story_draft(
        {
            "candidate": selected_candidate,
            "length": payload.get("length", "full_report"),
        }
    )

    publish_result = publish_if_eligible(
        {
            "draft": draft_result["draft"],
            "confidence": {
                "level": selected_candidate.get("confidence", "medium"),
                "homepage_eligible": selected_candidate.get("confidence") == "high",
            },
            "flags": payload.get("flags", []),
            "story_tier": payload.get("story_tier", "standard"),
            "requested_profile": shortlist_result.get("profile"),
            "effective_profile": draft_result.get("profile"),
        },
        correlation=correlation,
    )

    result = {
        "type": "run_content_pipeline",
        "accepted": True,
        "shortlist": shortlist,
        "selected_candidate": selected_candidate,
        "draft": draft_result["draft"],
        "decision": publish_result["decision"],
        "correlation": correlation,
    }

    if "article" in publish_result:
        result["article"] = publish_result["article"]
    if "review_item" in publish_result:
        result["review_item"] = publish_result["review_item"]

    return result


def _parse_json_content(message: str) -> dict:
    cleaned = message.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        cleaned = cleaned.strip()
    return json.loads(cleaned)


def publish_preview_article(payload: dict, *, correlation: dict) -> dict:
    return _persist_article(payload, correlation=correlation, force_status="published")


def publish_article(payload: dict, *, correlation: dict) -> dict:
    return _persist_article(payload, correlation=correlation, force_status=None)


def publish_if_eligible(payload: dict, *, correlation: dict) -> dict:
    decision = _evaluate_publish_decision(payload)
    if decision["action"] == "auto_publish":
        published = _persist_article(payload, correlation=correlation, force_status=None)
        published["decision"] = decision
        return published

    review_item = _persist_review_item(payload)
    return {
        "type": "publish_if_eligible",
        "accepted": True,
        "decision": decision,
        "review_item": review_item,
        "correlation": correlation,
    }


def archive_preview_article(payload: dict, *, correlation: dict) -> dict:
    settings = Settings.from_env()
    engine = build_engine(_database_url(settings))
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)
    now = datetime.now(UTC)

    try:
        with session_factory() as session:
            article_repository = ArticleRepository(session)
            article = article_repository.get_published_article_by_slug(payload["slug"])
            if article is None:
                raise ValueError(f"Unknown article slug: {payload['slug']}")

            snapshot = json.loads(article.rendered_snapshot_json or "{}")
            snapshot["status"] = "superseded"
            snapshot["homepage_eligible"] = False
            snapshot["updated_at"] = now.isoformat()

            updated = article_repository.update_published_article_status(
                payload["slug"],
                status="superseded",
                homepage_eligible=False,
                rendered_snapshot_json=json.dumps(snapshot),
                updated_at=now,
            )
            session.commit()
    finally:
        engine.dispose()

    return {
        "type": "archive_preview_article",
        "accepted": True,
        "article": {
            "slug": updated.slug,
            "status": updated.status.value,
            "homepage_eligible": updated.homepage_eligible,
            "sources": [_normalize_source(source) for source in snapshot.get("sources", [])],
        },
        "correlation": correlation,
    }


def _persist_article(payload: dict, *, correlation: dict, force_status: str | None) -> dict:
    settings = Settings.from_env()
    engine = build_engine(_database_url(settings))
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)

    draft = payload.get("draft", {})
    confidence = payload.get("confidence", {"level": "high", "homepage_eligible": True})
    now = datetime.now(UTC)
    slug = _slugify(draft.get("slug") or draft.get("headline") or str(uuid.uuid4()))
    status = force_status or ("developing_story" if confidence.get("level") == "low" else "published")
    homepage_eligible = bool(confidence.get("homepage_eligible", True)) and status == "published"

    snapshot = _build_article_snapshot(
        slug=slug,
        draft=draft,
        status=status,
        confidence_level=confidence.get("level", "high"),
        requested_profile=payload.get("requested_profile", settings.model_profile),
        effective_profile=payload.get("effective_profile", settings.model_profile),
        story_tier=payload.get("story_tier", "standard"),
        updated_at=now,
    )

    try:
        with session_factory() as session:
            story_repository = StoryRepository(session)
            article_repository = ArticleRepository(session)

            cluster = story_repository.create_cluster(
                {
                    "id": str(uuid.uuid4()),
                    "cluster_key": slug,
                    "topic_label": (draft.get("headline") or slug)[:255],
                    "status": "active",
                    "first_seen_at": now,
                    "last_updated_at": now,
                }
            )
            analysis = story_repository.create_analysis(
                {
                    "id": str(uuid.uuid4()),
                    "story_cluster_id": cluster.id,
                    "verified_facts_json": json.dumps(draft.get("fact_blocks", [])),
                    "open_questions_json": json.dumps([]),
                    "why_analysis_text": "\n\n".join(
                        block.get("analysis", "")
                        for block in draft.get("analysis_blocks", [])
                        if isinstance(block, dict)
                    ),
                    "disagreement_summary": "",
                    "overall_confidence": confidence.get("level", "high"),
                    "low_confidence_reasons_json": json.dumps([]),
                }
            )
            created_draft = article_repository.create_draft(
                {
                    "id": str(uuid.uuid4()),
                    "story_analysis_id": analysis.id,
                    "headline": (draft.get("headline") or slug)[:512],
                    "dek": (draft.get("dek") or "")[:512],
                    "body_json": json.dumps({"narrative": draft.get("narrative", "")}),
                    "facts_json": json.dumps(draft.get("fact_blocks", [])),
                    "analysis_json": json.dumps(draft.get("analysis_blocks", [])),
                    "citations_json": json.dumps(draft.get("sources", [])),
                    "validation_status": "preview_published" if force_status == "published" else "published",
                }
            )
            article = article_repository.create_published_article(
                {
                    "id": str(uuid.uuid4()),
                    "article_draft_id": created_draft.id,
                    "slug": slug[:512],
                    "status": status,
                    "homepage_eligible": homepage_eligible,
                    "published_at": now,
                    "updated_at": now,
                    "rendered_snapshot_json": json.dumps(snapshot),
                }
            )
            session.commit()
    finally:
        engine.dispose()

    return {
        "type": "publish_preview_article" if force_status == "published" else "publish_article",
        "accepted": True,
        "article": {
            "slug": article.slug,
            "status": article.status.value,
            "homepage_eligible": article.homepage_eligible,
            "sources": snapshot["sources"],
        },
        "correlation": correlation,
    }


def _persist_review_item(payload: dict) -> dict:
    settings = Settings.from_env()
    engine = build_engine(_database_url(settings))
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)

    draft = payload.get("draft", {})
    confidence = payload.get("confidence", {"level": "medium"})
    reasons = _evaluate_publish_decision(payload)["reasons"]
    validation_status = "flagged" if any(reason.startswith("flag:") for reason in reasons) else "review_required"
    now = datetime.now(UTC)
    slug = _slugify(draft.get("slug") or draft.get("headline") or str(uuid.uuid4()))

    try:
        with session_factory() as session:
            story_repository = StoryRepository(session)
            article_repository = ArticleRepository(session)

            cluster = story_repository.create_cluster(
                {
                    "id": str(uuid.uuid4()),
                    "cluster_key": slug,
                    "topic_label": (draft.get("headline") or slug)[:255],
                    "status": "active",
                    "first_seen_at": now,
                    "last_updated_at": now,
                }
            )
            analysis = story_repository.create_analysis(
                {
                    "id": str(uuid.uuid4()),
                    "story_cluster_id": cluster.id,
                    "verified_facts_json": json.dumps(draft.get("fact_blocks", [])),
                    "open_questions_json": json.dumps([]),
                    "why_analysis_text": "\n\n".join(
                        block.get("analysis", "") or block.get("text", "")
                        for block in draft.get("analysis_blocks", [])
                        if isinstance(block, dict)
                    ),
                    "disagreement_summary": "",
                    "overall_confidence": confidence.get("level", "medium"),
                    "low_confidence_reasons_json": json.dumps(reasons),
                }
            )
            created_draft = article_repository.create_draft(
                {
                    "id": str(uuid.uuid4()),
                    "story_analysis_id": analysis.id,
                    "headline": (draft.get("headline") or slug)[:512],
                    "dek": (draft.get("dek") or "")[:512],
                    "body_json": json.dumps({"narrative": draft.get("narrative", "")}),
                    "facts_json": json.dumps(draft.get("fact_blocks", [])),
                    "analysis_json": json.dumps(draft.get("analysis_blocks", [])),
                    "citations_json": json.dumps(draft.get("sources", [])),
                    "validation_status": validation_status,
                }
            )
            session.commit()
    finally:
        engine.dispose()

    queue = "flagged_items" if validation_status == "flagged" else "pending_drafts"
    return {
        "id": created_draft.id,
        "headline": created_draft.headline,
        "queue": queue,
    }


def _database_url(settings: Settings) -> str:
    return settings.corewire_database_url or settings.database_url or "sqlite:///corewire-local.db"


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:180]


def _build_article_snapshot(
    *,
    slug: str,
    draft: dict,
    status: str,
    confidence_level: str,
    requested_profile: str,
    effective_profile: str,
    story_tier: str,
    updated_at: datetime,
) -> dict:
    normalized_sources = [_normalize_source(source) for source in draft.get("sources", [])]
    return {
        "slug": slug,
        "headline": draft.get("headline", ""),
        "status": status,
        "confidence": confidence_level,
        "source_count": len(draft.get("sources", [])),
        "updated_at": updated_at.isoformat(),
        "dek": draft.get("dek", ""),
        "story_tier": story_tier,
        "requested_profile": requested_profile,
        "effective_profile": effective_profile,
        "facts": [
            {
                "text": block.get("text") or block.get("statement", ""),
                "citations": block.get("citations") or block.get("sources", []),
            }
            for block in draft.get("fact_blocks", [])
            if isinstance(block, dict)
        ],
        "analysis": [
            block.get("text") or block.get("analysis", "")
            for block in draft.get("analysis_blocks", [])
            if isinstance(block, dict)
        ],
        "disagreements": draft.get("disagreements", []),
        "sources": normalized_sources,
    }


def _evaluate_publish_decision(payload: dict) -> dict:
    confidence = payload.get("confidence", {})
    flags = payload.get("flags", [])
    draft = payload.get("draft", {})
    sources = draft.get("sources", [])
    reasons: list[str] = []

    if confidence.get("level") != "high":
        reasons.append(f"{confidence.get('level', 'unknown')}_confidence")

    if len(sources) < 3:
        reasons.append("insufficient_sources")

    if any(not isinstance(source, dict) for source in sources):
        reasons.append("invalid_source_shape")

    if any(isinstance(source, dict) and not source.get("url") for source in sources):
        reasons.append("missing_source_urls")

    if any(
        isinstance(source, dict)
        and not (source.get("publisher") or source.get("label"))
        for source in sources
    ):
        reasons.append("invalid_source_shape")

    quality_reasons = _evaluate_source_quality(sources)
    reasons.extend(quality_reasons)
    if _has_topical_source_mismatch(_draft_context(draft), sources):
        reasons.append("source_topic_mismatch")
    reasons.extend(_evaluate_editorial_flags(draft.get("editorial_flags", [])))

    reasons = list(dict.fromkeys(reasons))

    for flag in flags:
        reasons.append(f"flag:{flag}")

    action = "auto_publish" if not reasons else "review_required"
    return {"action": action, "reasons": reasons}


def _run_source_enrichment_pass(*, client: OpenRouterClient, model: str, source_references: list, candidate_context: str, strict: bool) -> list[ArticleSource]:
    strict_line = (
        "Return only sources with real URLs. Do not include placeholders, bracket references, or sources without URLs. "
        "Return at least 3 sources from 2 or more different publishers when possible, and avoid duplicate publishers if alternative relevant sources exist. "
        "Prefer primary reporting, official releases, filings, and original research reports. "
        "Prefer stronger publishers and institutions such as Reuters, Bloomberg, AP, FT, WSJ, official company releases, and major research institutions when relevant sources exist. "
        "Avoid videos, event pages, recap pages, newsletters, landing pages, and generic blogs when stronger primary sources exist."
        if strict
        else "Prefer sources with real URLs."
    )
    result = client.complete_json(
        model=model,
        system_prompt=(
            "You are a newsroom source normalization agent. Return only JSON."
        ),
        user_prompt=(
            "Normalize and enrich these source references into linkable source objects. "
            "Return JSON with a sources array. Each source must include label, publisher, title, url, and role. "
            "The sources must be topically relevant to this story context:\n"
            f"{candidate_context}\n"
            f"{strict_line}\n{json.dumps(source_references)}"
        ),
    )
    return [_normalize_source(source) for source in result.get("sources", [])]


def _count_valid_source_urls(sources: list[ArticleSource]) -> int:
    return sum(1 for source in sources if source.get("url"))


def _count_unique_publishers(sources: list[ArticleSource]) -> int:
    publishers = {
        (source.get("publisher") or source.get("label") or "").strip().lower()
        for source in sources
        if (source.get("publisher") or source.get("label"))
    }
    return len({publisher for publisher in publishers if publisher})


def _needs_source_enrichment_retry(candidate: dict, sources: list[ArticleSource]) -> bool:
    return (
        _count_valid_source_urls(sources) < 3
        or _count_unique_publishers(sources) < 2
        or _has_secondary_source_dependency(sources)
        or _has_topical_source_mismatch(_candidate_context(candidate), sources)
        or _has_insufficient_source_authority(sources)
    )


def _evaluate_source_quality(sources: list[dict]) -> list[str]:
    reasons: list[str] = []

    publishers = [
        (source.get("publisher") or source.get("label") or "").strip().lower()
        for source in sources
        if isinstance(source, dict)
    ]
    publishers = [publisher for publisher in publishers if publisher]

    unique_publishers = set(publishers)
    if len(unique_publishers) < 2:
        reasons.append("insufficient_source_diversity")
    elif publishers:
        max_count = max(publishers.count(publisher) for publisher in unique_publishers)
        if max_count > len(publishers) / 2:
            reasons.append("insufficient_source_diversity")

    if any(
        isinstance(source, dict)
        and isinstance(source.get("url"), str)
        and "youtube.com" in source["url"].lower()
        for source in sources
    ):
        reasons.append("video_source_dependency")

    if _has_insufficient_source_authority(sources):
        reasons.append("insufficient_source_authority")

    return reasons


def _evaluate_editorial_flags(editorial_flags: list[dict]) -> list[str]:
    reasons: list[str] = []
    for flag in editorial_flags:
        if not isinstance(flag, dict):
            continue
        severity = str(flag.get("severity") or "").strip().lower()
        if severity == "high":
            reasons.append("editorial_flag:high")
    return reasons


def _candidate_context(candidate: dict) -> str:
    return " ".join(
        str(candidate.get(field) or "")
        for field in ("title", "summary", "why_it_matters")
    ).strip()


def _draft_context(draft: dict) -> str:
    return " ".join(
        str(draft.get(field) or "")
        for field in ("headline", "dek", "narrative")
    ).strip()


def _has_secondary_source_dependency(sources: list[ArticleSource]) -> bool:
    return any(_is_secondary_source(source) for source in sources)


def _has_topical_source_mismatch(context: str, sources: list[ArticleSource]) -> bool:
    keywords = _extract_topic_keywords(context)
    if not keywords or not sources:
        return False

    domain_markers = {
        "ai",
        "agent",
        "agents",
        "agentic",
        "enterprise",
        "orchestrator",
        "orchestrators",
        "workflow",
        "workflows",
        "automation",
        "copilot",
        "copilots",
        "software",
        "operations",
        "business",
        "tech",
    }
    if not (keywords & domain_markers):
        return False

    matching_sources = 0
    comparable_sources = 0
    for source in sources:
        if not isinstance(source, dict):
            continue
        source_text = str(source.get("title") or "").lower()
        if not source_text.strip():
            continue
        comparable_sources += 1
        if any(keyword in source_text for keyword in keywords):
            matching_sources += 1

    if comparable_sources < 2:
        return False

    return matching_sources < min(2, comparable_sources)


def _has_insufficient_source_authority(sources: list[ArticleSource]) -> bool:
    authoritative_count = 0
    vendor_like_count = 0
    comparable_sources = 0

    for source in sources:
        if not isinstance(source, dict) or not source.get("url"):
            continue
        comparable_sources += 1
        if _is_authoritative_source(source):
            authoritative_count += 1
        if _is_vendor_like_source(source):
            vendor_like_count += 1

    if comparable_sources < 3:
        return False

    if authoritative_count >= 2:
        return False

    return vendor_like_count > comparable_sources / 2


def _is_authoritative_source(source: ArticleSource) -> bool:
    role = str(source.get("role") or "").strip().lower()
    publisher = str(source.get("publisher") or "").strip().lower()
    url = str(source.get("url") or "").strip().lower()

    if role in {"official_release", "research_report", "filing", "article"} and (
        publisher in {
            "reuters",
            "bloomberg",
            "associated press",
            "ap",
            "financial times",
            "wall street journal",
            "wsj",
            "the verge",
            "deloitte",
            "openai",
            "anthropic",
            "google",
            "microsoft",
            "meta",
        }
        or any(
            domain in url
            for domain in (
                "reuters.com",
                "bloomberg.com",
                "apnews.com",
                "ft.com",
                "wsj.com",
                "theverge.com",
                "deloitte.com",
                "openai.com",
                "anthropic.com",
                "blog.google",
                "microsoft.com",
                "about.fb.com",
            )
        )
    ):
        return True

    return False


def _is_vendor_like_source(source: ArticleSource) -> bool:
    url = str(source.get("url") or "").strip().lower()
    role = str(source.get("role") or "").strip().lower()

    if role in {"official_release", "research_report", "filing"}:
        return False

    return any(
        marker in url
        for marker in (
            "/blog/",
            "/blogs/",
            "/insights/blog/",
            "/insights/",
            "/agentic-insights/",
        )
    )


def _is_secondary_source(source: ArticleSource) -> bool:
    role = str(source.get("role") or "").strip().lower()
    url = str(source.get("url") or "").strip().lower()
    title = str(source.get("title") or "").strip().lower()
    label = str(source.get("label") or "").strip().lower()

    secondary_roles = {
        "blog",
        "newsletter",
        "event_page",
        "landing_page",
        "recap",
        "video",
        "podcast",
    }
    if role in secondary_roles:
        return True

    secondary_url_markers = (
        "youtube.com",
        "/blog/",
        "/blogs/",
        "/news-insights/",
        "/newsletter",
        "/recap",
    )
    if any(marker in url for marker in secondary_url_markers):
        return True

    secondary_text_markers = ("summit", "conference panel", "weekly recap", "newsletter")
    return any(marker in title or marker in label for marker in secondary_text_markers)


def _extract_topic_keywords(text: str) -> set[str]:
    stopwords = {
        "auto",
        "publish",
        "headline",
        "dek",
        "story",
        "valid",
        "the",
        "and",
        "for",
        "with",
        "into",
        "from",
        "that",
        "this",
        "will",
        "are",
        "how",
        "why",
        "what",
        "when",
        "where",
        "report",
        "fuller",
        "built",
        "move",
        "moves",
        "new",
        "year",
        "becoming",
    }
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return {
        token
        for token in tokens
        if len(token) >= 4 and token not in stopwords
    }


def _normalize_source(source: object) -> ArticleSource:
    if isinstance(source, str):
        return {
            "label": source,
            "publisher": None,
            "title": None,
            "url": None,
            "role": "source_reference",
        }

    if isinstance(source, dict):
        publisher = source.get("publisher") or source.get("organization") or source.get("label")
        title = source.get("title") or source.get("type")
        url = source.get("url")
        label = source.get("label") or publisher or title or "Unknown source"
        return {
            "label": str(label),
            "publisher": str(publisher) if publisher else None,
            "title": str(title) if title else None,
            "url": str(url) if url else None,
            "role": str(source.get("role") or "source"),
        }

    return {
        "label": str(source),
        "publisher": None,
        "title": None,
        "url": None,
        "role": "source_reference",
    }
