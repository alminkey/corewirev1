# Flagship Insight Engine Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen flagship `CoreWire Analysis` so the article surfaces a core contradiction, sharper `why now`, a buried consequence, and a harder ending instead of reading like a polished internal brief.

**Architecture:** Keep the current writer-first analysis pipeline intact. Enrich the dossier with explicit insight-layer signals, then rewrite the flagship writer to compose around those signals. Tighten doctrine and evaluation only after the new writer behavior exists and is test-covered.

**Tech Stack:** Python analysis services, pytest, existing operator pipeline, Next.js public article rendering already fixed, Docker staging

---

## File Structure

- Modify: `apps/api/core/analysis/dossier.py`
- Modify: `apps/api/core/analysis/writer.py`
- Modify: `apps/api/core/analysis/doctrine.py`
- Modify: `apps/api/core/analysis/evaluation.py`
- Modify: `apps/api/tests/test_analysis_dossier.py`
- Modify: `apps/api/tests/test_analysis_writer.py`
- Modify: `apps/api/tests/test_analysis_doctrine.py`
- Modify: `apps/api/tests/test_analysis_evaluation.py`

## Chunk 1: Add Explicit Insight Signals to the Dossier

### Task 1: Synthesize contradiction, why-now, consequence, and ending-pressure signals

**Files:**
- Modify: `apps/api/core/analysis/dossier.py`
- Test: `apps/api/tests/test_analysis_dossier.py`

- [ ] **Step 1: Write the failing dossier test**

```python
def test_build_research_dossier_adds_flagship_insight_signals():
    dossier = build_research_dossier(
        {
            "title": "Hormuz crisis",
            "public_narrative": "reopening shipping and restoring deterrence",
            "real_objective": "forcing Iran into concessions before coalition discipline frays",
            "timing_pressures": ["Washington is racing against fuel pressure."],
            "stakes": ["Shipping disruption is splitting the coalition."],
            "obscured_questions": ["Whether Washington can threaten harder without losing allies."],
        }
    )
    assert dossier["core_contradictions"]
    assert dossier["why_now_signals"]
    assert dossier["buried_consequences"]
    assert dossier["hard_questions"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_dossier.py -k flagship_insight_signals -q`  
Expected: FAIL because the new dossier keys do not exist

- [ ] **Step 3: Write minimal implementation**

Add deterministic synthesis in `build_research_dossier()`:

- `core_contradictions`
  - explicit tension between `public_narrative` and `real_objective`
- `why_now_signals`
  - timing pressure lines already present in the dossier
- `buried_consequences`
  - consequence lines synthesized from `stakes` and obscured pressure
- `hard_questions`
  - strongest unresolved strategic questions derived from `unknowns` and `obscured_questions`

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_dossier.py -k flagship_insight_signals -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/dossier.py apps/api/tests/test_analysis_dossier.py
git commit -m "feat: add flagship insight signals to analysis dossier"
```

## Chunk 2: Rewrite the Flagship Writer Around the Insight Layers

### Task 2: Make the writer compose around contradiction and why-now instead of actor symmetry

**Files:**
- Modify: `apps/api/core/analysis/writer.py`
- Test: `apps/api/tests/test_analysis_writer.py`

- [ ] **Step 1: Write the failing writer test**

```python
def test_generate_flagship_analysis_surfaces_core_contradiction_and_why_now():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": ["Washington says pressure is needed."],
            "core_contradictions": [
                "The public case is about reopening shipping, but the deeper fight is over whether Washington can keep its coalition aligned while forcing concessions."
            ],
            "why_now_signals": [
                "Washington is racing against fuel-price pressure and allied reluctance."
            ],
            "buried_consequences": [],
            "hard_questions": ["Whether coalition discipline can hold."]
        },
        [],
        "The crisis is escalating because the real contest is no longer just military."
    )
    assert "What matters more than the public case is the contradiction underneath it." in article["full_article"]
    assert "The timing is not incidental." in article["full_article"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_writer.py -k contradiction_and_why_now -q`  
Expected: FAIL because the writer does not yet compose around the new signal layers

- [ ] **Step 3: Write minimal implementation**

In `generate_flagship_analysis()`:

- add a contradiction paragraph helper driven by `core_contradictions`
- sharpen the timing paragraph from `why_now_signals`
- reduce symmetric actor exposition if contradiction/timing already carry the section

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_writer.py -k contradiction_and_why_now -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/writer.py apps/api/tests/test_analysis_writer.py
git commit -m "feat: center flagship writer on contradiction and timing"
```

### Task 3: Add a buried-consequence paragraph and a hard ending

**Files:**
- Modify: `apps/api/core/analysis/writer.py`
- Test: `apps/api/tests/test_analysis_writer.py`

- [ ] **Step 1: Write the failing writer test**

```python
def test_generate_flagship_analysis_adds_buried_consequence_and_hard_ending():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": [],
            "core_contradictions": [],
            "why_now_signals": [],
            "buried_consequences": [
                "The first real fracture may appear inside the coalition, not at sea."
            ],
            "hard_questions": [
                "Whether Washington can keep pressure rising without forcing allies to pull back."
            ],
        },
        [],
        "The crisis is escalating because the real contest is now political as much as military."
    )
    assert "The buried consequence is easier to miss than the headline event." in article["full_article"]
    assert "The article should end under pressure, not with a neutral recap." not in article["full_article"]
    assert "The hardest pressure point is now becoming unavoidable." in article["full_article"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_writer.py -k buried_consequence_and_hard_ending -q`  
Expected: FAIL because the writer still ends as a neat unresolved summary

- [ ] **Step 3: Write minimal implementation**

Add:

- `_build_buried_consequence_paragraph()`
- `_build_hard_ending_paragraph()`

Use:

- `buried_consequences`
- `hard_questions`
- existing `stakes`
- existing `unknowns`

The ending should escalate unresolved pressure, not simply restate uncertainty.

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_writer.py -k buried_consequence_and_hard_ending -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/writer.py apps/api/tests/test_analysis_writer.py
git commit -m "feat: add consequence and hard-ending flagship passes"
```

## Chunk 3: Tighten Doctrine and Evaluation Around Insight Quality

### Task 4: Add doctrine failures for weak contradiction, weak why-now, weak consequence, and weak ending

**Files:**
- Modify: `apps/api/core/analysis/doctrine.py`
- Test: `apps/api/tests/test_analysis_doctrine.py`

- [ ] **Step 1: Write the failing doctrine test**

```python
def test_validate_analysis_doctrine_flags_missing_insight_layers():
    contract = {
        "thesis": "A thesis",
        "full_article": "A long but generic article body.",
        "actor_map": [{"name": "US", "goal": "pressure Iran"}],
        "obscured_layer": ["Generic pressure line."],
        "stakes": ["Costs are rising."],
        "next_moves": ["US is likely to increase pressure."],
        "unknowns": ["It remains unclear what comes next."],
    }
    result = validate_analysis_doctrine(contract)
    assert "weak_core_contradiction" in result["violations"]
    assert "weak_why_now" in result["violations"]
    assert "weak_buried_consequence" in result["violations"]
    assert "weak_hard_ending" in result["violations"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_doctrine.py -k missing_insight_layers -q`  
Expected: FAIL because the validator does not yet score the new insight layers

- [ ] **Step 3: Write minimal implementation**

Add heuristics that fail when flagship analysis lacks:

- an explicit contradiction
- a timing-pressure layer
- a concrete consequence layer
- a pressured ending

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_doctrine.py -k missing_insight_layers -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/doctrine.py apps/api/tests/test_analysis_doctrine.py
git commit -m "feat: add insight-layer doctrine checks"
```

### Task 5: Penalize weak insight layers in evaluation

**Files:**
- Modify: `apps/api/core/analysis/evaluation.py`
- Test: `apps/api/tests/test_analysis_evaluation.py`

- [ ] **Step 1: Write the failing evaluation test**

```python
def test_score_analysis_output_penalizes_missing_flagship_insight_layers():
    doctrine = {
        "passed": False,
        "violations": [
            "weak_core_contradiction",
            "weak_why_now",
            "weak_buried_consequence",
            "weak_hard_ending",
        ],
    }
    score = score_analysis_output({"full_article": "X" * 1500}, doctrine)
    assert score["decision"] == "rerun"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_evaluation.py -k insight_layers -q`  
Expected: FAIL because evaluation does not yet punish these new doctrine violations

- [ ] **Step 3: Write minimal implementation**

Lower:

- `new_value`
- `why_explanation`
- `tone_corewire_identity`

when the new doctrine violations are present, and force `rerun` for multiple weak flagship insight layers.

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_evaluation.py -k insight_layers -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/evaluation.py apps/api/tests/test_analysis_evaluation.py
git commit -m "feat: score flagship insight weakness as rerun"
```

## Chunk 4: Full Regression and Live Evaluation

### Task 6: Re-run the analysis suite and generate a new flagship article for inspection

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

Use the existing operator/publish path and inspect the resulting article on the portal. Confirm that the new draft:

- contains a contradiction paragraph
- contains a sharpened `why now`
- contains a buried consequence
- ends with pressure, not neat summary

- [ ] **Step 4: Commit if any regression fixes were required**

```bash
git add <files>
git commit -m "fix: stabilize flagship insight engine regressions"
```

Plan complete and saved to `docs/superpowers/plans/2026-04-06-flagship-insight-engine-implementation.md`. Ready to execute?
