# CoreWire Analysis Doctrine Design

**Date:** 2026-04-01
**Status:** Approved for planning
**Scope:** `CoreWire Analysis` only

> **Supersession note:** For flagship analysis generation, this document supersedes the article-generation assumptions in [2026-03-13-corewire-final-product-design.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/specs/2026-03-13-corewire-final-product-design.md). Earlier design work remains valid for infrastructure, deploy, admin, review, and future Paperclip preparation.

## Goal

Redefine CoreWire around writer-first political, diplomatic, security, geo-economic, and business analysis that explains what happened, why it happened, who benefits, what is being obscured, and what likely comes next.

## Rebaseline

CoreWire has already proven:

- source intake
- operator orchestration
- review workflow
- publish flow
- staging deploy
- admin operations

Those remain.

What changes is the center of the system:

- **Old center:** structured draft validity
- **New center:** high-quality flagship analysis

CoreWire is no longer optimized around "can it generate a publishable payload?" It is optimized around "can it produce analysis worth publishing under the CoreWire name?"

## Product Definition

CoreWire Analysis is not:

- a rewrite of mainstream coverage
- a neutralized average of public talking points
- a JSON-first writing exercise
- a vehicle for state, corporate, or activist agenda capture

CoreWire Analysis is:

- writer-first
- evidence-seeking
- motive-seeking
- explicit about uncertainty
- hostile to propaganda and narrative laundering

## Editorial Mission

CoreWire Analysis exists to improve understanding of events that materially affect power, security, prosperity, rights, and daily life.

Its values are:

- truth over convenience
- clarity over noise
- justice over propaganda
- long-term human flourishing over factional manipulation

## Truth Model

Every analysis must preserve the distinction between:

1. **Verified facts**
2. **Claims**
3. **Assessment**
4. **Unknowns**
5. **Scenarios**

Nothing may be silently upgraded from claim to fact or from inference to proof.

## Core Rules

Every CoreWire Analysis must:

- have one clear central thesis
- answer `why`
- map the relevant actors
- show what each actor wants
- surface what is being obscured
- separate known facts from claims and assessment
- make the consequences legible
- offer real analytical value beyond mainstream recap

If a text has no thesis, no `why`, no actor map, and no new value, it is not a finished CoreWire Analysis.

## Writing Rule

CoreWire Analysis follows:

- **10-20%** known facts
- **50-60%** motives, contradictions, obscured layers, incentives, and underexplained dynamics
- **20-30%** scenarios, consequences, and unknowns

This is the `known brief, hidden deep` rule.

## Actor Map Rule

Every serious analysis must identify the relevant actors, including non-obvious ones:

- states
- leaders
- militaries
- proxy networks
- regulators
- corporations
- markets
- alliance blocs
- intermediaries

For each important actor, the article should establish where possible:

- what they want
- what they fear
- what helps them now
- what hurts them now
- what public story they tell
- what private logic likely drives them
- what they are likely to do next

## Agenda Rule

CoreWire does not adopt any side's agenda as the default narrative frame.

That includes:

- Western state agendas
- Eastern state agendas
- corporate PR agendas
- intelligence spins
- legacy-media consensus as automatic truth

When agenda is visible, CoreWire names it and analyzes it.

## Allowed Judgment

CoreWire is allowed to conclude that:

- a legal rationale is weak or contested
- a public justification hides a different objective
- a narrative frame is selective
- an actor's stated motive conflicts with observed behavior

But those judgments must be:

- evidence-based
- explicit
- legally careful
- intellectually honest

## Prohibited Patterns

CoreWire Analysis must not include:

- meta-commentary about what the reader should know
- commentary about what serious media should do
- commentary about how the article is structured
- generic filler
- false balance
- propaganda tone
- generic AI phrasing

## Tone

The tone must be:

- calm
- sharp
- precise
- unsentimental
- authoritative

The text must feel like a finished editorial product, not an explanation of itself.

## Standard Structure

Every CoreWire Analysis should contain:

1. the thesis
2. the minimum necessary account of what happened
3. the causal explanation
4. the actor and motive map
5. the obscured or underexplained layer
6. the practical and strategic consequences
7. the likely next moves
8. the remaining unknowns

## Evidence Hierarchy

Priority order:

1. primary documents and direct evidence
2. official data and public records
3. strong field or agency reporting
4. specialist analysis
5. secondary media synthesis

Headline consensus alone is never enough for flagship analysis.

## Legal Safety

CoreWire Analysis must:

- keep a hard line between fact and claim
- avoid unsupported motive imputation
- attribute serious allegations
- preserve evidence discipline
- remain defensible without becoming timid

## Technical Implication

The current schema-first path is no longer sufficient for flagship analysis.

The new architecture must move from:

- `research -> structured draft -> normalize -> publish`

to:

- `research dossier -> claims map -> actor map -> thesis -> full article -> structured extraction -> doctrine validation -> review/publish`

## What Remains Valid

These existing investments remain useful:

- operator APIs
- review flow
- admin
- persistence
- public routes
- staging deploy
- source discovery and enrichment as intake

## What Becomes Secondary

The current JSON-shell-first draft generation path becomes secondary or legacy for:

- quick rewrites
- lower-tier content
- utility publishing

It no longer defines flagship `CoreWire Analysis`.

## Success Condition

CoreWire Analysis succeeds when the finished article:

- explains why something happened
- maps incentives and interests
- surfaces what is obscured
- distinguishes fact, claim, and inference
- provides scenario value
- sounds like CoreWire, not like a polished aggregate

