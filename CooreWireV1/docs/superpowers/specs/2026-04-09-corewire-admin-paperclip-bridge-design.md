# CoreWire Admin Closure and Paperclip Bridge V1 Design

**Date:** 2026-04-09
**Status:** Approved for planning
**Scope:** Finish the owner-facing CoreWire site admin and define the first real Paperclip-to-CoreWire bridge without expanding Paperclip into a full agency operating system inside this phase.

## Goal

Lock CoreWire into a simple two-surface model:

- `CoreWire site admin` is the owner control plane for the news portal itself
- `Paperclip Bridge v1` is a narrow external integration layer that can read state from CoreWire and send commands into it

This keeps the product easy to reason about while preserving the larger long-term agency vision.

## Product Boundary

CoreWire and Paperclip have different jobs.

### CoreWire

CoreWire is:

- the public site
- the article engine
- the owner review and publishing console
- the place where autonomy, schedules, topics, and site operations are controlled

### Paperclip

Paperclip is:

- external to the public site
- an orchestration and governance environment
- a place that may later handle broader agency processes

For this phase, Paperclip is not a second admin UI for CoreWire. It is an external system that integrates through a bridge.

## CoreWire Site Admin V1

The site admin must become the practical owner panel for running the portal day to day.

### Required Sections

#### `Overview`

- system health
- autonomy mode
- queue depth
- recent publish/review activity
- basic source and runtime status
- basic cost and throughput signals

#### `Article Operations`

- view published articles
- view drafts
- manually create a story or draft
- edit existing draft content and metadata
- publish, reject, retract, correct, or supersede

#### `Autonomy and Programming Controls`

- global autonomy mode
- pause ingest
- pause publish
- homepage auto-publish
- developing-story auto-publish
- topic controls
- schedule or interval controls for recurring article generation

#### `Review and Compliance`

- review queue
- draft doctrine and quality diagnostics
- audit trail for owner actions

#### `Analytics`

- compact but useful operational analytics
- no enterprise BI scope in this phase

## Paperclip Bridge V1

Paperclip Bridge V1 is intentionally narrow.

It exists so that Paperclip can:

- read key operational state from CoreWire
- send a limited set of authenticated commands to CoreWire

It does not exist to reproduce the full CoreWire admin inside Paperclip.

### Read Capabilities

Paperclip should be able to read:

- overall system health
- autonomy mode and pause state
- high-level queue and published counts
- recent published stories
- review queue summary
- selected analytics summaries

### Command Capabilities

Paperclip should be able to send:

- `create_story`
- `rerun_analysis`
- `publish_draft`
- `set_autonomy_mode`
- `pause_ingest`
- `pause_publish`
- `disable_source`
- optional `import_external_draft` for a Paperclip-authored article body

### Integration Shape

The recommended first integration path is:

- Paperclip `HTTP adapter`
- CoreWire internal operator and bridge endpoints

This aligns with Paperclip's role as control plane rather than execution engine.

## Auth and Trust Boundary

Owner admin and Paperclip traffic must remain separate.

### Owner Admin

- owner-only auth
- browser-driven usage
- full site-control privileges

### Paperclip Bridge

- service-to-service auth
- `x-internal-token`
- limited operator and bridge scope
- no reuse of owner auth

## Frontend Boundary

### In CoreWire

CoreWire frontend includes:

- public site
- owner admin pages

### Not in CoreWire

CoreWire frontend does not include:

- Paperclip product UI
- marketing/finance/uprava dashboards from a broader agency OS

Those remain external and future-facing.

## Data and Correlation Model

Bridge traffic should support correlation without forcing a full workflow engine now.

Useful identifiers:

- `ticket_id`
- `actor_id`
- `company_id`
- `correlation_id`
- `requested_by`

These fields should be optional at first but preserved end to end where possible.

## Non-Goals for This Phase

This phase explicitly does not include:

- full Paperclip product implementation
- marketing operations dashboards
- finance ledgers or revenue accounting
- multi-user RBAC inside CoreWire
- a second CMS inside Paperclip
- deep two-way workflow syncing

## Architecture Direction

The architecture stays simple:

- CoreWire admin is the operational truth for the portal
- operator APIs remain the integration seam
- Paperclip uses the seam instead of reaching directly into CoreWire internals

This keeps Paperclip coupling late and reversible.

## Risks and Controls

- `Admin scope creep`
  Control: keep the site admin focused on portal operations only

- `Paperclip over-expansion`
  Control: bridge only, no full agency UI in this phase

- `Auth confusion`
  Control: strict separation between owner auth and internal service auth

- `Dual-control ambiguity`
  Control: CoreWire admin remains the canonical owner control plane; Paperclip is an external caller

- `Bridge becoming unstable`
  Control: narrow command set, explicit schemas, correlation metadata, runbooks, and smoke coverage

## Release Outcome

This phase is complete when:

- the owner can run CoreWire from the site admin without missing core portal controls
- Paperclip can read meaningful CoreWire state through stable endpoints
- Paperclip can send the first meaningful commands into CoreWire
- the separation of responsibilities stays obvious in code, docs, and UI
