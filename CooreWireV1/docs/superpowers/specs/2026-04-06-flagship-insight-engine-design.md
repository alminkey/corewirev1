# Flagship Insight Engine Design

**Date:** 2026-04-06  
**Status:** Approved for planning  
**Scope:** `CoreWire Analysis` flagship writer only

> **Supersession note:** This document supplements [2026-04-01-corewire-analysis-doctrine-design.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/specs/2026-04-01-corewire-analysis-doctrine-design.md). The 2026-04-01 doctrine remains the governing editorial baseline. This document narrows the next product problem: turning valid flagship drafts into articles that feel revealing, satisfying, and distinctively CoreWire.

## Goal

Raise flagship `CoreWire Analysis` from a structurally valid analysis draft to a piece that delivers:

- stronger depth
- stronger originality
- stronger tonal authority
- stronger structural flow
- a clear sense of earned reading value

The current engine can produce a coherent analysis skeleton. It still sounds too much like a polished internal brief. The next step is not more length by itself. The next step is an `insight engine` that forces the article to surface the hidden contradiction, the timing logic, the buried consequence, and the hard ending.

## Problem Statement

The current writer-first engine now does several things correctly:

- distinguishes facts, claims, unknowns, and next moves
- forms a thesis
- generates a full article
- extracts renderable sections
- gates shallow output

But the finished flagship article still has recurring weaknesses:

- it explains the topic instead of revealing the hidden struggle inside it
- actor coverage still feels symmetric and system-generated
- `why now` is present but not sharp enough
- consequences are legible but not yet weighty
- the ending closes neatly without delivering a real analytical jolt

This means the next quality gap is not `more prose`. The gap is `better insight composition`.

## Recommended Approach

Use a `Flagship Insight Engine` layered on top of the existing writer-first pipeline.

The pipeline remains:

- dossier
- actor map
- thesis
- full article
- extraction
- doctrine
- evaluation

What changes is the content inside the flagship writer. Before writing, the system must synthesize four mandatory insight layers:

1. **Core contradiction**  
   The main clash between the public argument and the real strategic logic.

2. **Why now**  
   The timing pressure that makes this moment different from the same story a week earlier.

3. **Buried consequence**  
   The consequence that matters most but is easiest to understate in daily coverage.

4. **Hard ending**  
   A closing passage that leaves the reader with a real unresolved strategic pressure, not just a tidy recap.

## Non-Goals

This slice does not attempt to solve:

- lower-tier rewrites
- newsletter tone
- ordinary wire briefs
- homepage design
- admin review UX
- full source-discovery redesign

This is a flagship writer problem only.

## New Insight Contract

Every flagship analysis must contain these four layers, whether or not they appear as explicit headings in the final article.

### 1. Core Contradiction

The article must answer:

- what is the public story
- what is the deeper contest
- where the public story and the real objective diverge

The contradiction must be specific. Generic lines about “pressure” or “leverage” are not enough.

### 2. Why Now

The article must explain:

- why this move happened now
- which side is under the tighter clock
- what deadline, vulnerability, or narrowing option set makes timing decisive

`Why now` should feel causal, not decorative.

### 3. Buried Consequence

The article must show:

- who pays first
- which alliance, market, institution, or subsystem bends first
- what broader consequence is hiding behind the headline event

This layer is where CoreWire should most clearly move beyond mainstream recap.

### 4. Hard Ending

The final movement of the article must end with pressure, not politeness.

It should leave the reader with:

- the hardest unresolved strategic question
- the real risk if current incentives continue
- the clearest reason the story is still moving

It must not end with generic lines such as:

- “it remains to be seen”
- “the situation remains tense”
- “the story is still unfolding”

## Structural Rules

Flagship analysis should now follow this rhythm:

1. thesis
2. minimum necessary what-happened
3. public case
4. why now
5. actor conflict
6. core contradiction
7. buried consequence
8. next phase
9. hard ending

The middle must feel like an argument unfolding, not a checklist being satisfied.

## Writer Voice Rules

The flagship writer must avoid:

- memo-like summaries
- evenly distributed actor paragraphs with identical cadence
- phrasing that sounds like a systems report
- generic geopolitical abstractions without a concrete pressure point

The flagship writer should prefer:

- sharper transitional sentences
- asymmetry where the story demands it
- concrete pressure language
- sentences that expose a hidden mechanism, not merely restate the scene

## Dossier Requirements

To support the new writer, the dossier needs stronger intermediate signals:

- `core_contradictions`
- `why_now_signals`
- `buried_consequences`
- `hard_questions`

These should be synthesized from existing inputs:

- public narrative
- real objective
- timing pressures
- hidden incentives
- stakes
- actor benefits and pressures
- obscured questions

The system does not need a separate model call for this slice. It can first synthesize these layers deterministically from the current dossier inputs.

## Doctrine and Evaluation Changes

Current doctrine catches shallow output. This slice should add more targeted failure modes for flagship analysis, such as:

- missing core contradiction
- weak why-now layer
- missing buried consequence
- weak ending pressure

Evaluation should reward:

- concrete contradiction
- real time sensitivity
- consequence specificity
- stronger closing force

## Success Criteria

This slice is successful when the next flagship article:

- feels less like a structured brief
- feels more like a finished CoreWire argument
- contains a clear hidden struggle
- explains why the moment matters now
- surfaces at least one consequence that feels non-obvious
- ends with a harder unresolved pressure than the current drafts do

## What Stays Stable

No change to:

- operator routing
- review flow
- publishing flow
- public article rendering structure
- admin
- staging deploy
- doctrine baseline from 2026-04-01

The work is focused on flagship writer behavior and the dossier signals it consumes.
