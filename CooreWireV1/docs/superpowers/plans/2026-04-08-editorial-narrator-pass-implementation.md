# Editorial Narrator Pass Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade flagship `CoreWire Analysis` so it reads like a finished editorial article rather than a structurally strong intelligence memo.

**Architecture:** Keep the current `lead insight` and `proof stack` pipeline intact. Rewrite only the flagship surface-writing layer so the opening, middle transitions, and ending are composed as magazine-style editorial prose while preserving existing doctrine signals.

**Tech Stack:** Python analysis services, pytest, existing operator pipeline, staging article publishing flow

---

## File Structure

- Modify: `apps/api/core/analysis/writer.py`
- Modify: `apps/api/tests/test_analysis_writer.py`
- Modify: `apps/api/tests/test_analysis_doctrine.py`

## Chunk 1: Rewrite the Opening Into an Editorial Lead

### Task 1: Replace thesis-shaped opening with a true editorial lead

**Files:**
- Modify: `apps/api/core/analysis/writer.py`
- Test: `apps/api/tests/test_analysis_writer.py`

- [ ] **Step 1: Write the failing writer test**

```python
def test_generate_flagship_analysis_opens_with_editorial_lead_not_engine_thesis():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "lead_insight_candidates": [
                "The public case is about reopening the Strait of Hormuz, but the deeper fight is over coalition endurance."
            ],
            "public_narrative": "reopening the Strait of Hormuz",
        },
        [],
        "Hormuz crisis is escalating because the real contest is coalition endurance."
    )
    opening = article["full_article"].split("\\n\\n")[0]
    assert "is escalating because" not in opening
    assert opening.startswith("What looks like") or opening.startswith("The real danger")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_writer.py -k editorial_lead_not_engine_thesis -q`  
Expected: FAIL because the opening still mirrors thesis-engine phrasing too closely

- [ ] **Step 3: Write minimal implementation**

In `writer.py`:

- add `_build_editorial_lead(...)`
- keep `lead_insight` internally
- render an editorial opening sentence instead of exposing the raw thesis form

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_writer.py -k editorial_lead_not_engine_thesis -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/writer.py apps/api/tests/test_analysis_writer.py
git commit -m "feat: rewrite flagship opening as editorial lead"
```

## Chunk 2: Replace Actor Templates With Editorial Proof Paragraphs

### Task 2: Collapse actor template blocks into connected proof paragraphs

**Files:**
- Modify: `apps/api/core/analysis/writer.py`
- Test: `apps/api/tests/test_analysis_writer.py`

- [ ] **Step 1: Write the failing writer test**

```python
def test_generate_flagship_analysis_uses_editorial_proof_paragraphs_not_actor_profiles():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "lead_insight_candidates": ["The real contest is coalition endurance."],
            "core_contradictions": ["The public case is about shipping, but the deeper fight is coalition endurance."],
            "why_now_signals": ["Washington is racing against allied reluctance."],
        },
        [
            {"name": "United States", "goal": "force concessions", "currently_pressures": ["allied reluctance"]},
            {"name": "Iran", "goal": "raise costs", "currently_benefits": ["maritime leverage"]},
        ],
        "Placeholder thesis",
    )
    assert "Washington is trying to" not in article["full_article"]
    assert "Iran is trying to" not in article["full_article"]
    assert "The next problem is" in article["full_article"] or "The pressure is most visible" in article["full_article"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_writer.py -k editorial_proof_paragraphs_not_actor_profiles -q`  
Expected: FAIL because the middle still uses actor-profile wording

- [ ] **Step 3: Write minimal implementation**

In `writer.py`:

- add `_build_editorial_proof_paragraphs(...)`
- move actor data inside connected analytical paragraphs
- remove default `X is trying / X is under pressure / X next move` cadence from flagship output

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_writer.py -k editorial_proof_paragraphs_not_actor_profiles -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/writer.py apps/api/tests/test_analysis_writer.py
git commit -m "feat: replace actor profiles with editorial proof paragraphs"
```

### Task 3: Add stronger editorial transitions between flagship sections

**Files:**
- Modify: `apps/api/core/analysis/writer.py`
- Test: `apps/api/tests/test_analysis_writer.py`

- [ ] **Step 1: Write the failing writer test**

```python
def test_generate_flagship_analysis_uses_non_modular_editorial_transitions():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "lead_insight_candidates": ["The real contest is coalition endurance."],
            "core_contradictions": ["The public case is about shipping, but the deeper fight is coalition endurance."],
            "why_now_signals": ["Washington is racing against allied reluctance."],
            "buried_consequences": ["The first fracture may appear inside the coalition."],
            "hard_questions": ["Whether Washington can keep allies aligned."],
        },
        [],
        "Placeholder thesis",
    )
    assert "What matters more than the public case" not in article["full_article"]
    assert "The next phase is" not in article["full_article"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_writer.py -k non_modular_editorial_transitions -q`  
Expected: FAIL because the writer still uses obvious module-transition phrases

- [ ] **Step 3: Write minimal implementation**

In `writer.py`:

- replace repeated module markers with tighter editorial transitions
- preserve doctrine signals while hiding internal scaffolding language

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_writer.py -k non_modular_editorial_transitions -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/writer.py apps/api/tests/test_analysis_writer.py
git commit -m "feat: strengthen editorial transitions in flagship analysis"
```

## Chunk 3: Harder Closing Cadence

### Task 4: Rewrite flagship ending as an editorial close

**Files:**
- Modify: `apps/api/core/analysis/writer.py`
- Test: `apps/api/tests/test_analysis_writer.py`

- [ ] **Step 1: Write the failing writer test**

```python
def test_generate_flagship_analysis_ends_with_editorial_close_not_summary_loop():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "lead_insight_candidates": ["The real contest is coalition endurance."],
            "hard_questions": ["Whether Washington can keep allies aligned."],
            "buried_consequences": ["The first fracture may appear inside the coalition."],
        },
        [],
        "Placeholder thesis",
    )
    ending = article["full_article"].split("\\n\\n")[-1]
    assert "It remains unclear" not in ending
    assert "Until that pressure breaks" in ending or "The risk is that" in ending
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_writer.py -k editorial_close_not_summary_loop -q`  
Expected: FAIL because the ending still resolves as a system summary

- [ ] **Step 3: Write minimal implementation**

In `writer.py`:

- rewrite the closing builder so it lands on one harder editorial sentence
- keep unresolved pressure, but remove memo-like cadence

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_writer.py -k editorial_close_not_summary_loop -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/writer.py apps/api/tests/test_analysis_writer.py
git commit -m "feat: harden flagship editorial closing cadence"
```

## Chunk 4: Regression and Live Read

### Task 5: Re-run regressions and publish one fresh flagship article

**Files:**
- Modify: none unless regressions surface
- Test: existing analysis and web suites

- [ ] **Step 1: Run analysis regression suite**

Run:

```bash
pytest apps/api/tests/test_analysis_doctrine.py apps/api/tests/test_analysis_dossier.py apps/api/tests/test_analysis_writer.py apps/api/tests/test_analysis_evaluation.py apps/api/tests/test_operator_service.py apps/api/tests/test_review_queue.py apps/api/tests/test_article_queries.py -q
```

Expected: all passing

- [ ] **Step 2: Run web regression suite**

Run:

```bash
pnpm --dir apps/web test
```

Expected: all passing

- [ ] **Step 3: Publish one fresh flagship article to staging**

Use the existing analysis publish path and inspect the resulting article on the portal. Confirm that the new draft:

- opens with an editorial lead, not an engine thesis
- no longer exposes actor profile cadence in the middle
- reads as connected proof paragraphs
- lands with a harder editorial close

- [ ] **Step 4: Commit if any regression fixes were required**

```bash
git add <files>
git commit -m "fix: stabilize editorial narrator flagship regressions"
```
