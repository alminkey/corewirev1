# CoreWire Analysis Evaluation Runbook

This runbook defines how to evaluate the `CoreWire Analysis` engine after writer-first changes land. It is for flagship analysis only, not for ordinary wire rewrites or short news updates.

## Purpose

Use this runbook to answer one question:

`Is CoreWire producing analysis that is genuinely better than a polished mainstream summary?`

The evaluation loop is not about:

- whether the pipeline runs
- whether JSON shape is valid
- whether an article can technically be published

It is about:

- thesis strength
- explanatory power
- actor-map quality
- ability to surface what others under-explain
- discipline around facts, claims, and uncertainty

## When to Run It

Run this evaluation loop:

- after any material change to `core.analysis.*`
- after any prompt change for flagship analysis
- after doctrine validator changes
- before increasing autonomous analysis volume
- before declaring the analysis engine ready for broader pilot use

## The 10-Topic Evaluation Loop

Each evaluation cycle uses 10 topics:

- 4 geopolitics / diplomacy / war
- 2 macroeconomy / markets / sanctions
- 2 business power / technology / regulation
- 2 institutional or governance crises

The set should include:

- at least 3 topics with strong evidence and broad coverage
- at least 3 topics where the public narrative is contested
- at least 2 topics with obvious propaganda or agenda pressure
- at least 2 topics where the most important question is not `what happened`, but `why now`

Avoid picking 10 easy consensus stories. The point is to test the engine where analysis matters.

## Evaluation Preparation

For each topic, capture:

- title of the topic
- date and time of the evaluation run
- the research dossier inputs used
- the generated thesis
- the generated full article
- structured extraction output
- doctrine result
- final reviewer judgment

Store these results in a dated evaluation note or artifact for comparison across runs.

## Core Scoring Rubric

Score each topic on a `0-3` scale.

`0`
- failed badly

`1`
- weak / generic / partial

`2`
- solid but not distinctive

`3`
- strong and clearly CoreWire-grade

### 1. Thesis Strength

Question:
- Does the article make a real causal claim, or is it just arranged information?

Strong thesis:
- explains what the conflict or event is really about
- gives a defensible central claim
- is not a generic framing sentence

Weak thesis:
- could fit almost any story
- only restates the visible event
- says nothing about motive or structure

### 2. Answer to `Why?`

Question:
- Does the article explain why this happened, why now, and why this move?

Strong result:
- identifies timing logic
- identifies motive
- distinguishes public justification from likely real purpose

Weak result:
- only describes reactions
- leaves the central causal question untouched

### 3. New Value

Question:
- Does the article add something that a smart reader would not already get from mainstream coverage?

Counts as real new value:
- exposing a hidden incentive
- connecting known facts into a sharper interpretation
- showing what coverage is missing or obscuring
- clarifying what actually matters and what is noise

Does not count:
- elegant paraphrase
- better formatting
- longer summary

### 4. Actor Map Quality

Question:
- Are all relevant actors identified and treated seriously?

Strong result:
- includes main state actors
- includes proxies, allies, institutions, markets, or intermediaries where relevant
- states what each actor wants
- states what currently helps or hurts each actor
- states likely next moves

Weak result:
- only names obvious actors
- does not map incentives
- treats motives as slogans

### 5. Fact / Claim / Assessment Discipline

Question:
- Is the article honest about what is verified, what is claimed, and what is inferred?

Strong result:
- no blurred line between evidence and interpretation
- uncertainty is explicit where needed
- propaganda is attributed and analyzed, not absorbed

Weak result:
- claims presented as facts
- agenda language treated as neutral description
- fake certainty

### 6. Agenda Resistance

Question:
- Did the article avoid becoming a vehicle for one side's narrative?

Strong result:
- no default alignment with state, bloc, or corporate messaging
- visible agendas are named
- no false balance either

Weak result:
- one narrative quietly becomes the frame of the article
- article sounds like extended strategic communications

### 7. Tone and CoreWire Identity

Question:
- Does the piece read like CoreWire, or like a generic media rewrite?

Strong result:
- precise
- calm
- sharp
- analytically confident
- no empty phrases

Weak result:
- generic “situation remains tense” energy
- padded
- performatively serious but not insightful

## Pass Threshold

A topic passes only if:

- `Thesis Strength >= 2`
- `Why >= 2`
- `New Value >= 2`
- `Actor Map >= 2`
- `Fact / Claim / Assessment >= 2`
- and no category is `0`

A run is considered healthy only if:

- at least `7/10` topics pass
- at least `3/10` topics score `3` on `New Value`
- average score for `Agenda Resistance` is at least `2`

## Strong Thesis Standard

A strong thesis is not just “X matters because Y is important”.

A strong thesis:

- names the underlying struggle
- identifies the real lever of power
- points to motive or structure
- can be argued for or against

Examples of weak theses:

- “Tensions are rising in the region.”
- “The crisis reflects growing instability.”

Examples of stronger thesis shapes:

- “The visible military escalation masks a struggle over the cost structure of regional deterrence.”
- “The policy fight is being presented as a security measure, but its real purpose is to lock in bargaining leverage before negotiations.”

## Real New Value Standard

An article has real new value if, after reading it, the evaluator can say:

- “Now I understand what this is really about.”
- “Now I see the incentive structure.”
- “Now I see what other coverage left out.”

An article does not have real new value if the best praise available is:

- “This is a clean summary.”

## Actor Map Quality Standard

To score `3`, the actor map should answer, for each major actor:

- what they want
- what they fear
- what currently benefits them
- what currently hurts them
- what constraint limits them
- what they are most likely to do next

If the article only lists actors without incentive analysis, it cannot score above `1`.

## Decision Rules

### Auto-accept for further pilot use

Use when:

- topic passes threshold
- article has clear CoreWire value
- no serious doctrine or legal concern is visible

### Request rerun

Use when:

- thesis is generic
- article explains `what` but not `why`
- actor map is thin
- article sounds too mainstream or too agenda-captured
- evidence base is good enough that a better second pass is plausible

### Review manually

Use when:

- article is promising but has one or two high-value weaknesses
- subject is sensitive and judgment matters
- legal wording needs care

### Reject outright

Use when:

- article is mostly generic summary
- article is propaganda-shaped
- article confuses facts and claims
- article has no defensible thesis
- article adds no real new value

## Common Failure Modes

Watch for:

- generic thesis that could fit any story
- heavy recap of known facts with little hidden-layer analysis
- missing “why now”
- missing practical stakes
- actor map that stops at naming sides
- agenda capture through language choices
- fake neutrality that hides obvious asymmetry
- overconfident scenario claims without evidentiary basis

## Evaluation Output Template

Use this structure per topic:

```text
Topic:
Date:

Thesis Strength: 0-3
Why: 0-3
New Value: 0-3
Actor Map: 0-3
Fact/Claim/Assessment: 0-3
Agenda Resistance: 0-3
Tone/CoreWire Identity: 0-3

Pass/Fail:
Decision: accept / rerun / review / reject

Best part:
Main weakness:
What must improve next:
```

## Exit Signal

The analysis engine is ready for wider pilot usage only when repeated runs show:

- consistent pass rate
- clear CoreWire voice
- real new value across difficult topics
- low dependence on manual rewriting for flagship output
