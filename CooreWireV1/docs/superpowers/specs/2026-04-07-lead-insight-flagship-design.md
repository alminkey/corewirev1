# Lead Insight Flagship Design

**Date:** 2026-04-07  
**Status:** Approved for planning  
**Scope:** `CoreWire Analysis` flagship writer only

> **Supersession note:** This document supplements [2026-04-01-corewire-analysis-doctrine-design.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/specs/2026-04-01-corewire-analysis-doctrine-design.md) and narrows the next product gap after [2026-04-06-flagship-insight-engine-design.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/specs/2026-04-06-flagship-insight-engine-design.md). The doctrine still governs all `CoreWire Analysis`. This document defines the next flagship requirement: every flagship article must revolve around one dominant analytical insight instead of distributing attention across multiple medium-strength observations.

## Goal

Turn flagship `CoreWire Analysis` from a structurally sound article into a piece that delivers one unmistakable `aha` moment.

The next reader value target is not:

- more length
- more elegant prose by itself
- more sections
- more even actor coverage

The next target is:

- one dominant hidden insight
- a clear contrast between visible narrative and real struggle
- a proof stack that convinces the reader that the insight is earned
- a closing consequence that makes the insight matter

## Problem Statement

The current flagship engine now does several things correctly:

- forms a thesis
- separates facts, claims, unknowns, and next moves
- adds contradiction, timing, consequence, and ending pressure layers
- rejects shallow output more aggressively

But the article still often feels:

- too symmetrical
- too system-shaped
- too explanatory
- too close to a polished analyst memo

The underlying issue is not only prose. It is composition. The article still tries to satisfy several analytical duties at once instead of making one big idea feel inevitable.

That is why the current output can be valid, intelligent, and still not satisfying.

## Recommended Approach

Use a `Lead Insight Flagship` model layered on top of the current `Flagship Insight Engine`.

The engine should continue to synthesize multiple signals internally, but before writing the article it must collapse them into one primary editorial claim:

- the one insight that most changes the reader's understanding of the story

The article then orbits that insight.

Instead of writing:

- event recap
- actor overview
- hidden layer
- consequences

as parallel obligations, the writer should now produce:

1. `Lead Insight`
2. `Known Surface`
3. `Proof Stack`
4. `Suppressed Alternative`
5. `Consequence of the Insight`
6. `Hard Ending`

## Lead Insight Contract

Every flagship article must begin from one dominant insight sentence.

That sentence should usually take one of these shapes:

- `This crisis is no longer mainly about X. It is about Y.`
- `The visible conflict masks a deeper struggle over X.`
- `What looks like a fight over X is actually a fight over Y.`
- `The public argument is about X, but the real contest is over Y.`

The lead insight must do three things at once:

- identify the hidden struggle
- replace the obvious framing with a stronger one
- create a reason to keep reading

If the sentence could fit many different stories, it is not strong enough.

## Proof Stack

The lead insight cannot stand alone. It must be earned.

Each flagship article must carry a `proof stack` of three to five concrete supports, pulled from the dossier:

- one visible fact or move
- one contradiction between public language and real objective
- one timing pressure
- one actor incentive or vulnerability
- one consequence that exposes what the mainstream frame misses

The proof stack is not a bullet list in the final article. It is the evidence path that makes the lead insight feel solid.

## Suppressed Alternative

Every flagship article must also know what it is pushing against.

That means the writer must identify the dominant but incomplete frame that most coverage is using, such as:

- a purely military frame
- a moralized frame without incentive analysis
- a market frame without power analysis
- a diplomatic frame without domestic political constraints

The article should not spend long attacking that frame. It should briefly establish it, then surpass it.

## Actor Handling Rule

Actors remain mandatory, but they are no longer the middle of the article.

The actor map now exists to prove the lead insight, not to satisfy symmetry.

That means:

- the article should spend more time on the actors that best reveal the main insight
- weaker actors should be folded into consequence or constraint paragraphs
- the article should avoid giving each actor an equally sized paragraph by default

The reader should feel that actors appear where they sharpen the main claim, not because the system is obligated to cover everyone evenly.

## Consequence Rule

The buried consequence must now answer:

- what becomes visible only if the lead insight is true

This should usually identify:

- who bends first
- what alliance, market, or institution cracks first
- what cost becomes politically intolerable first
- what strategic option becomes unavailable first

This is the part of the article most likely to create the reader's `aha`.

## Hard Ending Rule

The ending must no longer behave like a neat unresolved summary.

It must do two things:

- restate the main pressure created by the lead insight
- identify the hardest unresolved question that pressure leaves behind

The ending should feel like:

- the story has been clarified
- the risk has been sharpened
- the next move matters more now, not less

## Structural Rhythm

The new flagship rhythm should be:

1. lead insight
2. minimum necessary visible event
3. dominant public explanation
4. the article's replacement frame
5. proof stack
6. consequence
7. hard ending

Actor analysis, `why now`, contradiction, and next moves all still matter, but they should serve this rhythm instead of competing with it.

## Dossier Requirements

To support this writer shape, the dossier needs one more synthesis layer:

- `lead_insight_candidates`

Each candidate should be a possible big insight generated from existing signals:

- `core_contradictions`
- `why_now_signals`
- `buried_consequences`
- `hidden_incentives`
- `obscured_questions`

The writer should then select:

- one best `lead insight`
- one short `suppressed alternative`
- one ordered `proof stack`

This can still be deterministic in the first iteration.

## Doctrine and Evaluation Changes

The validator and scorer should eventually treat these as flagship failures:

- missing dominant lead insight
- proof stack too generic
- actor section still too symmetrical
- consequence not tied back to the main insight
- ending that does not escalate the lead insight into a real unresolved pressure

## Success Criteria

This slice is successful when a flagship article produces this reaction:

- `Now I understand what this story is really about.`

Not:

- `This is a cleaner summary.`
- `This is better written than before.`
- `This is a more structured analysis.`

The target is stronger than prose quality. It is reader recognition that the article revealed the story's hidden center of gravity.

## What Stays Stable

No change to:

- operator routing
- review flow
- publish flow
- public rendering structure
- analysis doctrine baseline
- current source quality gate

This slice changes flagship writer behavior only.
