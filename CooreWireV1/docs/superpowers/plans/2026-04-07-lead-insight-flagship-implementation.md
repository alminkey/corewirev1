# Lead Insight Flagship Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make flagship `CoreWire Analysis` revolve around one dominant analytical insight with a proof stack, suppressed alternative, and harder consequence-driven ending.

**Architecture:** Keep the existing writer-first analysis pipeline and current `Flagship Insight Engine` layers. Add one new deterministic synthesis layer in the dossier for `lead_insight_candidates`, then rewrite the flagship writer so the article is composed around the chosen lead insight instead of evenly distributed actor exposition. Tighten doctrine and evaluation only after the new writer shape exists and is test-covered.

**Tech Stack:** Python analysis services, pytest, existing operator pipeline, staging article publishing flow

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

## Chunk 1: Synthesize a Dominant Lead Insight Before Writing

### Task 1: Add lead insight candidates to the dossier

**Files:**
- Modify: `apps/api/core/analysis/dossier.py`
- Test: `apps/api/tests/test_analysis_dossier.py`

- [ ] **Step 1: Write the failing dossier test**

```python
def test_build_research_dossier_adds_lead_insight_candidates():
    dossier = build_research_dossier(
        {
            "title": "Hormuz crisis",
            "public_narrative": "reopening shipping and restoring deterrence",
            "real_objective": "forcing Iran into concessions before coalition discipline frays",
            "timing_pressures": ["Washington is racing against fuel pressure."],
            "hidden_incentives": ["Several Gulf capitals want U.S. protection without owning escalation."],
            "obscured_questions": ["Whether Washington can threaten harder without losing allies."],
            "why_it_matters": "Shipping disruption is testing coalition discipline.",
        }
    )
    assert dossier["lead_insight_candidates"]
    assert any("public case" in candidate.lower() or "real contest" in candidate.lower() for candidate in dossier["lead_insight_candidates"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_dossier.py -k lead_insight_candidates -q`  
Expected: FAIL because the dossier does not yet emit `lead_insight_candidates`

- [ ] **Step 3: Write minimal implementation**

Add deterministic synthesis in `build_research_dossier()`:

- `_build_lead_insight_candidates(...)`
  - derive candidate insight lines from:
    - `core_contradictions`
    - `why_now_signals`
    - `hidden_incentives`
    - `buried_consequences`
- return `lead_insight_candidates` on the dossier

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_dossier.py -k lead_insight_candidates -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/dossier.py apps/api/tests/test_analysis_dossier.py
git commit -m "feat: add lead insight candidates to analysis dossier"
```

## Chunk 2: Rewrite the Flagship Writer Around One Big Insight

### Task 2: Make the writer choose a lead insight and a suppressed alternative

**Files:**
- Modify: `apps/api/core/analysis/writer.py`
- Test: `apps/api/tests/test_analysis_writer.py`

- [ ] **Step 1: Write the failing writer test**

```python
def test_generate_flagship_analysis_centers_one_lead_insight():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": ["Washington says stronger pressure is needed."],
            "lead_insight_candidates": [
                "The public case is about reopening shipping, but the real contest is over whether Washington can force concessions before coalition discipline breaks."
            ],
            "core_contradictions": [
                "The public case is about reopening shipping, but the deeper fight is over whether Washington can keep allies aligned while forcing concessions."
            ],
            "why_now_signals": ["Washington is racing against fuel-price pressure and allied reluctance."],
            "buried_consequences": ["The first real fracture may appear inside the coalition, not at sea."],
            "hard_questions": ["Whether Washington can keep pressure rising without forcing allies to pull back."],
        },
        [],
        "Placeholder thesis"
    )
    assert "The article turns on one central insight." in article["full_article"]
    assert "Most coverage is treating the crisis as" in article["full_article"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_writer.py -k one_lead_insight -q`  
Expected: FAIL because the writer does not yet compose around a chosen lead insight or suppressed alternative

- [ ] **Step 3: Write minimal implementation**

In `generate_flagship_analysis()`:

- add `_select_lead_insight(dossier, thesis)`
- add `_build_suppressed_alternative_paragraph(dossier)`
- replace the old opening flow with:
  - lead insight
  - minimum visible frame
  - suppressed alternative

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_writer.py -k one_lead_insight -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/writer.py apps/api/tests/test_analysis_writer.py
git commit -m "feat: center flagship writing on one lead insight"
```

### Task 3: Replace symmetric actor exposition with a proof stack

**Files:**
- Modify: `apps/api/core/analysis/writer.py`
- Test: `apps/api/tests/test_analysis_writer.py`

- [ ] **Step 1: Write the failing writer test**

```python
def test_generate_flagship_analysis_uses_proof_stack_not_symmetric_actor_blocks():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": ["Washington says stronger pressure is needed."],
            "lead_insight_candidates": ["The real contest is coalition endurance, not only military pressure."],
            "core_contradictions": ["The public case is about shipping, but the deeper fight is coalition endurance."],
            "why_now_signals": ["Washington is racing against allied reluctance."],
            "buried_consequences": ["The first fracture may appear inside the coalition."],
            "hard_questions": ["Whether Washington can keep pressure rising without losing allies."],
        },
        [
            {"name": "United States", "goal": "force concessions", "likely_next_move": "increase pressure", "currently_pressures": ["allied reluctance"]},
            {"name": "Iran", "goal": "raise global costs", "likely_next_move": "maintain maritime pressure", "currently_benefits": ["maritime leverage"]},
        ],
        "Placeholder thesis"
    )
    assert "Three pressures make that insight hard to ignore." in article["full_article"]
    assert "The strategic problem now looks different for each actor." not in article["full_article"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_writer.py -k proof_stack_not_symmetric -q`  
Expected: FAIL because the writer still relies on the current actor-led middle

- [ ] **Step 3: Write minimal implementation**

Add:

- `_build_proof_stack_paragraphs(dossier, actor_map)`
  - facts/timing/constraints/benefits become proof lines for the lead insight
- reduce actor paragraphs to only what the proof stack cannot carry
- remove the default symmetric actor section when proof stack is available

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_writer.py -k proof_stack_not_symmetric -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/writer.py apps/api/tests/test_analysis_writer.py
git commit -m "feat: replace symmetric flagship middle with proof stack"
```

### Task 4: Tie consequence and ending back to the lead insight

**Files:**
- Modify: `apps/api/core/analysis/writer.py`
- Test: `apps/api/tests/test_analysis_writer.py`

- [ ] **Step 1: Write the failing writer test**

```python
def test_generate_flagship_analysis_ties_consequence_and_ending_to_lead_insight():
    article = generate_flagship_analysis(
        {
            "topic": "Hormuz crisis",
            "verified_facts": ["Shipping disruption is spreading."],
            "claims": [],
            "lead_insight_candidates": ["The real contest is coalition endurance, not only military pressure."],
            "core_contradictions": ["The public case is about shipping, but the deeper fight is coalition endurance."],
            "buried_consequences": ["The first fracture may appear inside the coalition, not at sea."],
            "hard_questions": ["Whether Washington can keep pressure rising without forcing allies to pull back."],
        },
        [],
        "Placeholder thesis"
    )
    assert "If that insight is right, the first real rupture will not be military." in article["full_article"]
    assert "If that pressure keeps building, the hardest question is no longer abstract." in article["full_article"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_writer.py -k consequence_and_ending_to_lead_insight -q`  
Expected: FAIL because the consequence and ending are not explicitly tied back to the chosen insight

- [ ] **Step 3: Write minimal implementation**

Update:

- `_build_consequence_paragraph(...)`
- `_build_hard_ending_paragraph(...)`

So both reference the selected lead insight and restate why that insight changes the stakes.

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_writer.py -k consequence_and_ending_to_lead_insight -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/writer.py apps/api/tests/test_analysis_writer.py
git commit -m "feat: tie flagship consequence and ending to lead insight"
```

## Chunk 3: Tighten Doctrine and Evaluation Around Lead Insight Quality

### Task 5: Detect weak lead insight, weak proof stack, and unresolved symmetry

**Files:**
- Modify: `apps/api/core/analysis/doctrine.py`
- Test: `apps/api/tests/test_analysis_doctrine.py`

- [ ] **Step 1: Write the failing doctrine test**

```python
def test_validate_analysis_doctrine_flags_missing_lead_insight_shape():
    contract = {
        "thesis": "A generic thesis.",
        "full_article": "A long article that still reads like a clean summary.",
        "actor_map": [{"name": "US", "goal": "pressure Iran"}],
        "obscured_layer": ["A generic hidden layer."],
        "stakes": ["Costs are rising."],
        "next_moves": ["US is likely to increase pressure."],
        "unknowns": ["It remains unclear what comes next."],
    }
    result = validate_analysis_doctrine(contract)
    assert "weak_lead_insight" in result["violations"]
    assert "weak_proof_stack" in result["violations"]
    assert "symmetric_actor_middle" in result["violations"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_doctrine.py -k lead_insight_shape -q`  
Expected: FAIL because the validator does not yet know these new flagship failures

- [ ] **Step 3: Write minimal implementation**

Add heuristics that fail when flagship analysis:

- does not establish one dominant insight early
- lacks a proof-like middle
- still leans on symmetrical actor exposition

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_doctrine.py -k lead_insight_shape -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/doctrine.py apps/api/tests/test_analysis_doctrine.py
git commit -m "feat: detect weak lead-insight flagship structure"
```

### Task 6: Penalize weak lead-insight flagship structure in evaluation

**Files:**
- Modify: `apps/api/core/analysis/evaluation.py`
- Test: `apps/api/tests/test_analysis_evaluation.py`

- [ ] **Step 1: Write the failing evaluation test**

```python
def test_score_analysis_output_reruns_weak_lead_insight_flagship():
    doctrine = {
        "passed": False,
        "violations": [
            "weak_lead_insight",
            "weak_proof_stack",
            "symmetric_actor_middle",
        ],
    }
    score = score_analysis_output({"full_article": "X" * 1600}, doctrine)
    assert score["decision"] == "rerun"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_analysis_evaluation.py -k weak_lead_insight_flagship -q`  
Expected: FAIL because evaluation does not yet punish these new flagship failures

- [ ] **Step 3: Write minimal implementation**

Lower:

- `new_value`
- `tone_corewire_identity`
- `actor_map_quality`

when the new violations are present, and force `rerun` when multiple lead-insight failures appear together.

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest apps/api/tests/test_analysis_evaluation.py -k weak_lead_insight_flagship -q`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analysis/evaluation.py apps/api/tests/test_analysis_evaluation.py
git commit -m "feat: score weak lead-insight flagship output as rerun"
```

## Chunk 4: Regression and Live Evaluation

### Task 7: Re-run regression suites and publish one new flagship article

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

- states one dominant lead insight early
- contains a proof stack instead of a symmetric actor middle
- ties the buried consequence back to the main insight
- ends with pressure anchored to that same insight

- [ ] **Step 4: Commit if any regression fixes were required**

```bash
git add <files>
git commit -m "fix: stabilize lead-insight flagship regressions"
```
