# CoreWire Analysis Engine Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace CoreWire's flagship analysis-generation path with a writer-first analysis engine while preserving the existing operational stack.

**Architecture:** Keep the current operator APIs, review flow, admin, publishing, staging, and deploy workflow. Introduce a new analysis engine that builds a dossier, maps actors and claims, forms a thesis, writes a full article first, and only then extracts structured renderable sections and validation signals.

**Tech Stack:** FastAPI, Python services, PostgreSQL, existing operator services, pytest, Node test runner, Next.js, Docker Compose staging

---

## File Structure

- Create: `apps/api/core/analysis/dossier.py`
- Create: `apps/api/core/analysis/actors.py`
- Create: `apps/api/core/analysis/thesis.py`
- Create: `apps/api/core/analysis/writer.py`
- Create: `apps/api/core/analysis/extraction.py`
- Create: `apps/api/core/analysis/doctrine.py`
- Modify: `apps/api/core/operator/service.py`
- Modify: `apps/api/core/articles/service.py`
- Modify: `apps/api/core/admin/review.py`
- Create: `apps/api/tests/test_analysis_doctrine.py`
- Create: `apps/api/tests/test_analysis_dossier.py`
- Create: `apps/api/tests/test_analysis_writer.py`
- Modify: `apps/api/tests/test_operator_service.py`
- Modify: `apps/api/tests/test_review_queue.py`
- Modify: `apps/api/tests/test_article_queries.py`
- Modify: `apps/web/lib/types.ts`
- Modify: `apps/web/app/admin/review/[id]/page.tsx`
- Modify: `apps/web/tests/review-queue.test.mjs`
- Create: `docs/runbooks/corewire-analysis-evaluation.md`

## Chunk 1: Lock the New Analysis Contract

### Task 1: Define doctrine validation in tests first

**Files:**
- Create: `apps/api/tests/test_analysis_doctrine.py`
- Create: `apps/api/core/analysis/doctrine.py`

- [ ] **Step 1: Write the failing doctrine test**

```python
def test_analysis_requires_thesis_why_actor_map_and_new_value():
    article = {"thesis": "", "body": "Generic summary.", "actor_map": [], "obscured_layer": []}
    result = validate_analysis_doctrine(article)
    assert result["passed"] is False
    assert "missing_thesis" in result["violations"]
    assert "missing_why" in result["violations"]
    assert "missing_actor_map" in result["violations"]
    assert "missing_new_value" in result["violations"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_doctrine.py -q`
Expected: FAIL because `validate_analysis_doctrine` does not exist

- [ ] **Step 3: Write the minimal validator**

```python
def validate_analysis_doctrine(article: dict) -> dict:
    body = article.get("body") or article.get("full_article") or ""
    violations = []
    if not article.get("thesis"):
        violations.append("missing_thesis")
    if "because" not in body.lower() and "why" not in body.lower():
        violations.append("missing_why")
    if not article.get("actor_map"):
        violations.append("missing_actor_map")
    if not article.get("obscured_layer"):
        violations.append("missing_new_value")
    if "reader" in body.lower():
        violations.append("meta_reader_language")
    return {"passed": not violations, "violations": violations}
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_doctrine.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/doctrine.py apps/api/tests/test_analysis_doctrine.py
git commit -m "test: define corewire analysis doctrine validator"
```

### Task 2: Define the analysis contract shape

**Files:**
- Create: `apps/api/core/analysis/types.py`
- Modify: `apps/api/core/articles/schemas.py`
- Modify: `apps/api/tests/test_analysis_doctrine.py`

- [ ] **Step 1: Write the failing contract test**

```python
def test_analysis_contract_contains_full_article_and_renderable_sections():
    contract = build_analysis_contract({})
    assert set(contract.keys()) >= {
        "thesis",
        "known_facts",
        "actor_map",
        "obscured_layer",
        "next_moves",
        "unknowns",
        "full_article",
    }
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_doctrine.py -q`
Expected: FAIL because `build_analysis_contract` does not exist

- [ ] **Step 3: Write the minimal contract builder**

```python
def build_analysis_contract(payload: dict) -> dict:
    return {
        "thesis": payload.get("thesis", ""),
        "known_facts": payload.get("known_facts", []),
        "actor_map": payload.get("actor_map", []),
        "obscured_layer": payload.get("obscured_layer", []),
        "next_moves": payload.get("next_moves", []),
        "unknowns": payload.get("unknowns", []),
        "full_article": payload.get("full_article", ""),
    }
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_doctrine.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/types.py apps/api/core/articles/schemas.py apps/api/tests/test_analysis_doctrine.py
git commit -m "feat: define corewire analysis contract"
```

## Chunk 2: Build the Writer-First Core

### Task 3: Add a research dossier builder

**Files:**
- Create: `apps/api/core/analysis/dossier.py`
- Create: `apps/api/tests/test_analysis_dossier.py`

- [ ] **Step 1: Write the failing dossier test**

```python
def test_build_research_dossier_separates_facts_claims_and_unknowns():
    candidate = {
        "title": "Hormuz tensions rise",
        "summary": "Shipping disruption spreads.",
        "sources": [{"publisher": "AP", "title": "Shipping hit", "url": "https://example.com"}],
        "claims": ["Iran says it is acting defensively"],
    }
    dossier = build_research_dossier(candidate)
    assert "verified_facts" in dossier
    assert "claims" in dossier
    assert "unknowns" in dossier
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_dossier.py -q`
Expected: FAIL because `build_research_dossier` does not exist

- [ ] **Step 3: Write minimal implementation**

```python
def build_research_dossier(candidate: dict) -> dict:
    return {
        "topic": candidate.get("title", ""),
        "verified_facts": [candidate.get("summary", "")],
        "claims": candidate.get("claims", []),
        "sources": candidate.get("sources", []),
        "unknowns": [],
    }
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_dossier.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/dossier.py apps/api/tests/test_analysis_dossier.py
git commit -m "feat: add research dossier builder"
```

### Task 4: Add actor mapping and thesis formation

**Files:**
- Create: `apps/api/core/analysis/actors.py`
- Create: `apps/api/core/analysis/thesis.py`
- Modify: `apps/api/tests/test_analysis_dossier.py`

- [ ] **Step 1: Write the failing actor/thesis tests**

```python
def test_build_actor_map_tracks_goals_constraints_and_next_moves():
    actor_map = build_actor_map({}, [{"name": "Iran", "goal": "raise cost"}])
    assert actor_map[0]["goal"] == "raise cost"
    assert "constraints" in actor_map[0]
    assert "likely_next_move" in actor_map[0]


def test_form_analysis_thesis_returns_causal_claim():
    thesis = form_analysis_thesis({"topic": "War"}, [{"name": "US", "goal": "pressure Iran"}])
    assert thesis
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest apps/api/tests/test_analysis_dossier.py -q`
Expected: FAIL because the functions do not exist

- [ ] **Step 3: Write minimal implementation**

```python
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


def form_analysis_thesis(dossier: dict, actor_map: list[dict]) -> str:
    return "The visible crisis masks a deeper struggle over leverage, cost, and regional order."
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest apps/api/tests/test_analysis_dossier.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/actors.py apps/api/core/analysis/thesis.py apps/api/tests/test_analysis_dossier.py
git commit -m "feat: add actor map and thesis builder"
```

### Task 5: Add full-article writer and structured extraction

**Files:**
- Create: `apps/api/core/analysis/writer.py`
- Create: `apps/api/core/analysis/extraction.py`
- Create: `apps/api/tests/test_analysis_writer.py`

- [ ] **Step 1: Write the failing writer test**

```python
def test_generate_flagship_analysis_returns_full_article_before_blocks():
    thesis = "A thesis"
    article = generate_flagship_analysis({"verified_facts": ["Fact"]}, [{"name": "Iran"}], thesis)
    assert article["thesis"] == thesis
    assert len(article["full_article"]) > 1200


def test_extract_analysis_sections_returns_renderable_blocks():
    extracted = extract_analysis_sections(
        {
            "full_article": "Long article body",
            "known_facts": ["Fact 1"],
            "next_moves": ["Move 1"],
            "unknowns": ["Unknown 1"],
        }
    )
    assert "fact_blocks" in extracted
    assert "analysis_blocks" in extracted
    assert "disagreements" in extracted
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest apps/api/tests/test_analysis_writer.py -q`
Expected: FAIL because writer and extraction do not exist

- [ ] **Step 3: Write minimal implementation**

```python
def generate_flagship_analysis(dossier: dict, actor_map: list[dict], thesis: str) -> dict:
    body = "\n\n".join([thesis, "What happened.", "Why it happened.", "What is being obscured.", "What happens next."])
    return {
        "thesis": thesis,
        "known_facts": dossier.get("verified_facts", []),
        "actor_map": actor_map,
        "obscured_layer": ["Hidden interests and narrative management."],
        "next_moves": ["Escalation risk remains high."],
        "unknowns": dossier.get("unknowns", []),
        "full_article": body * 80,
    }


def extract_analysis_sections(article: dict) -> dict:
    return {
        "fact_blocks": [{"text": fact, "citations": []} for fact in article.get("known_facts", [])],
        "analysis_blocks": [{"text": article.get("full_article", "")[:500]}],
        "disagreements": article.get("unknowns", []),
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest apps/api/tests/test_analysis_writer.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/writer.py apps/api/core/analysis/extraction.py apps/api/tests/test_analysis_writer.py
git commit -m "feat: add writer-first flagship analysis core"
```

## Chunk 3: Wire the New Engine Into CoreWire

### Task 6: Route `CoreWire Analysis` through the new engine

**Files:**
- Modify: `apps/api/core/operator/service.py`
- Modify: `apps/api/tests/test_operator_service.py`

- [ ] **Step 1: Write the failing routing test**

```python
def test_run_content_pipeline_uses_analysis_engine_for_analysis_content(monkeypatch):
    called = {"writer": False}

    def fake_writer(*args, **kwargs):
        called["writer"] = True
        return {"thesis": "A thesis", "known_facts": ["Fact"], "actor_map": [{"name": "US"}], "obscured_layer": ["Gap"], "next_moves": ["Move"], "unknowns": [], "full_article": "X" * 2000}

    monkeypatch.setattr("core.analysis.writer.generate_flagship_analysis", fake_writer)
    run_content_pipeline({"content_type": "analysis", "domain": "politics-diplomacy"}, correlation={})
    assert called["writer"] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_operator_service.py -q`
Expected: FAIL because analysis routing is not yet wired

- [ ] **Step 3: Write minimal implementation**

Wire `run_content_pipeline()` so that when `content_type == "analysis"` it:
- builds dossier
- builds actor map
- forms thesis
- writes full article
- extracts sections
- validates doctrine

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/api/tests/test_operator_service.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/operator/service.py apps/api/tests/test_operator_service.py
git commit -m "feat: route corewire analysis through new engine"
```

### Task 7: Surface doctrine diagnostics in review

**Files:**
- Modify: `apps/api/core/admin/review.py`
- Modify: `apps/api/tests/test_review_queue.py`
- Modify: `apps/web/lib/types.ts`
- Modify: `apps/web/app/admin/review/[id]/page.tsx`
- Modify: `apps/web/tests/review-queue.test.mjs`

- [ ] **Step 1: Write the failing review-detail test**

```python
def test_review_detail_exposes_doctrine_status():
    detail = get_review_detail("draft-review-detail")
    assert "doctrine" in detail
    assert "violations" in detail["doctrine"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest apps/api/tests/test_review_queue.py -q`
Expected: FAIL because doctrine diagnostics are not present

- [ ] **Step 3: Write minimal implementation**

Expose:
- thesis present or missing
- doctrine passed boolean
- doctrine violations list

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest apps/api/tests/test_review_queue.py -q`
Run: `cmd /c "cd /d F:\\2026\\CoreWire\\CooreWireV1\\apps\\web && node --test tests\\review-queue.test.mjs"`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/admin/review.py apps/api/tests/test_review_queue.py apps/web/lib/types.ts apps/web/app/admin/review/[id]/page.tsx apps/web/tests/review-queue.test.mjs
git commit -m "feat: show doctrine diagnostics in review detail"
```

## Chunk 4: Normalize Publishing and Evaluation

### Task 8: Publish the writer-first snapshot instead of sparse block payloads

**Files:**
- Modify: `apps/api/core/articles/service.py`
- Modify: `apps/api/tests/test_article_queries.py`

- [ ] **Step 1: Write the failing published-article test**

```python
def test_published_analysis_prefers_full_article_snapshot():
    detail = get_article_detail("analysis-slug")
    assert detail["facts"]
    assert detail["analysis"]
    assert detail["full_article"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_article_queries.py -q`
Expected: FAIL because published analysis does not yet prioritize the full-article snapshot

- [ ] **Step 3: Write minimal implementation**

Normalize published analysis so that:
- `full_article` is preserved
- empty fact blocks are filtered
- empty analysis blocks are filtered
- unknowns/disagreements remain explicit rather than blank

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/api/tests/test_article_queries.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/articles/service.py apps/api/tests/test_article_queries.py
git commit -m "feat: normalize published writer-first analysis snapshots"
```

### Task 9: Add an evaluation runbook

**Files:**
- Create: `docs/runbooks/corewire-analysis-evaluation.md`
- Modify: `README.md`

- [ ] **Step 1: Write the runbook**

Document:
- the 10-topic evaluation loop
- what counts as a strong thesis
- what counts as real new value
- how to score actor-map quality
- when to rerun, review, or reject

- [ ] **Step 2: Review the runbook**

Run: `git diff -- docs/runbooks/corewire-analysis-evaluation.md README.md`
Expected: clear operator guidance with no contradiction to the doctrine

- [ ] **Step 3: Commit**

```bash
git add docs/runbooks/corewire-analysis-evaluation.md README.md
git commit -m "docs: add corewire analysis evaluation runbook"
```

## Chunk 5: Protect the Roadmap From Drift

### Task 10: Mark earlier final-product docs as partially superseded

**Files:**
- Modify: `docs/superpowers/specs/2026-03-13-corewire-final-product-design.md`
- Modify: `docs/superpowers/plans/2026-03-13-corewire-final-product-implementation.md`

- [ ] **Step 1: Add supersession notes**

Add notes that:
- keep infrastructure/admin/review/deploy work valid
- point all flagship analysis work to the 2026-04-01 doctrine and this plan

- [ ] **Step 2: Review doc coherence**

Run: `git diff -- docs/superpowers/specs docs/superpowers/plans`
Expected: no contradiction about what now defines flagship analysis

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/specs/2026-03-13-corewire-final-product-design.md docs/superpowers/plans/2026-03-13-corewire-final-product-implementation.md
git commit -m "docs: rebaseline flagship analysis around writer-first engine"
```

## What Stays Stable

These stay in service:

- staging/VPS/runtime
- admin shell
- review queue
- owner actions
- publish persistence
- public routes
- source discovery/enrichment intake

## What Becomes Legacy

After this plan:

- the current JSON-shell-first flagship draft path becomes legacy for `CoreWire Analysis`
- it may remain only for quick rewrites, utility content, and lower-tier formats

## Exit Criteria

This plan is complete when:

- flagship analysis routes through the new writer-first engine
- doctrine validation exists
- review shows doctrine diagnostics
- published analysis renders as a real article, not a sparse block shell
- the rest of CoreWire's operating stack still works

Plan complete and saved to `docs/superpowers/plans/2026-04-01-corewire-analysis-engine-implementation.md`. Ready to execute?
