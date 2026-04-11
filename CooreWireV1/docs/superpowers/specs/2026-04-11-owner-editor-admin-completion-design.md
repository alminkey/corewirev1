# Owner Editor and Admin Completion Design

**Date:** 2026-04-11
**Status:** Approved for planning
**Scope:** Complete the owner-facing CoreWire admin by turning the current article manager into a real single-page draft editor and publish workspace inside `/admin`.

## Goal

Make `/admin` good enough to operate CoreWire in day-to-day production without leaving the site admin.

This phase focuses on:

- real create/edit/save/publish workflow for owner-created drafts
- keeping the editing flow inside `/admin`
- avoiding a separate CMS route tree or a second content model

## Product Decision

The owner editor will be a `single-page workspace` inside `/admin`.

It will not use:

- `/admin/content/new`
- `/admin/content/[id]`
- modal-heavy editing
- a new standalone CMS subsystem

This keeps the owner workflow fast, visible, and aligned with the existing control-plane model.

## UX Shape

The `Article Manager` section becomes a two-column workspace.

### Left Column: Inventory

Purpose:

- choose what to edit
- understand what exists
- quickly start a new draft

Contains:

- `New Draft` action
- manual draft list
- published inventory list

Each draft row should be selectable and should load into the editor on the right.

### Right Column: Editor

Purpose:

- edit one draft at a time
- save changes
- publish when ready

Fields:

- `headline`
- `dek`
- `slug`
- `tags`
- `body`

Actions:

- `Save Draft`
- `Publish`
- `Reject` or `Archive Draft` if needed

Editor state should make it obvious:

- which draft is selected
- whether there are unsaved changes
- current draft status

## Backend Model Direction

Do not introduce a new content model.

Use the existing owner/manual draft path built on:

- `StoryCluster`
- `StoryAnalysis`
- `ArticleDraft`

Extend the current admin content endpoints rather than inventing a second write path.

That means:

- `create_manual_story_draft()` remains the entry point
- `update_manual_story_draft()` remains the owner save path
- add explicit owner publish and owner archive/reject actions on top of that same model

## API Direction

The admin content API should expose enough state for a single-page editor to work without hidden client logic.

Needed capabilities:

- list drafts and published items
- create empty or seeded manual draft
- fetch one draft in editor-ready shape
- update one draft
- publish one draft
- archive or reject one draft

The response shape should return the normalized editor document so the client can refresh local state from server truth after every mutation.

## Frontend Behavior

The editor should behave like a lightweight newsroom workspace, not a form dump.

Expected interaction flow:

1. owner opens `/admin`
2. owner clicks a draft or `New Draft`
3. editor fills with server-backed values
4. owner edits fields
5. `Save Draft` persists without leaving the page
6. `Publish` uses the same workspace and updates the inventory

Important constraints:

- no rich text editor in this phase
- simple textarea/body editing is enough
- no optimistic complexity beyond basic dirty-state feedback

## Relationship to Existing Admin Areas

This does not replace:

- review queue
- autonomy controls
- programming controls
- analytics

It completes the missing practical publishing part of the owner admin.

After this phase, the next logical admin improvement is:

- stronger programming controls with real save/apply workflow

## Non-Goals

This phase does not include:

- collaborative editing
- multi-user CMS roles
- revision history UI
- rich text/Notion-style editor
- media uploads
- direct Paperclip UI integration

## Risks and Controls

- `Editor grows into a separate CMS`
  Control: keep everything inside `/admin` and reuse the existing draft model

- `Too much client-side state drift`
  Control: every mutation returns canonical server state; refresh local editor from response

- `Publish path bypasses existing rules`
  Control: owner publish action must pass through the same compliance/publish logic used elsewhere

- `UI becomes cluttered`
  Control: inventory on the left, editor on the right, keep form fields minimal

## Release Outcome

This phase is complete when:

- the owner can create a draft from `/admin`
- select and edit an existing draft from `/admin`
- save draft updates without leaving `/admin`
- publish from the same workspace
- use the admin as a practical operational panel rather than just a dashboard
