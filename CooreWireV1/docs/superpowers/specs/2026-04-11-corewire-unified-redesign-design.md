# CoreWire Unified Redesign Design

**Date:** 2026-04-11  
**Status:** Approved for planning  
**Scope:** Redesign the public frontend and owner admin so they share one modern CoreWire visual system while using different layouts for editorial reading and operational control.

## Goal

Replace the current retro, terminal-heavy, scroll-heavy presentation with a modern CoreWire product language that feels:

- premium
- readable
- operationally clear
- modern without looking generic

This redesign has two surfaces:

- `public frontend`: premium editorial/news product
- `owner admin`: modern app/dashboard workspace

Both surfaces must share the same brand system while optimizing for different tasks.

## Product Decision

CoreWire will use a `single unified design system` with `separate layout models`.

That means:

- same colors
- same typography families
- same card language
- same button/input language
- same spacing and motion principles

But:

- the frontend uses editorial hierarchy and story browsing
- the admin uses an app shell and task-oriented workspace

This avoids the current failure mode where:

- the frontend feels like a retro prototype
- the admin feels like a long blog page instead of a control panel

## Visual Direction

The new CoreWire look should be:

- light and warm, not dark-terminal
- premium editorial, not template-magazine
- modern operational, not SaaS-generic
- subtle in motion, not flashy

### Core palette

- warm off-white / paper-like page background
- dark ink text for headlines and body
- muted stone/brown UI neutrals
- copper / rust accent for actions and small signal markers

### Typography

- serif for major headlines, article titles, and strong editorial moments
- clean sans for navigation, metadata, admin labels, and inputs
- monospace becomes optional and secondary, not the default identity

### Brand motif

The existing `signal / dispatch` idea stays, but in a reduced form:

- small dispatch labels
- thin accent lines
- subtle signal dots/bars
- restrained separators

The interface should no longer look like a command-center skin.

## Motion Direction

Motion should be `subtle and premium`.

Allowed:

- panel and card reveal on load
- soft hover elevation
- focus and active state transitions
- section change transitions in admin

Not allowed:

- loud parallax
- gimmicky scroll effects
- constant motion or animated noise

The system should leave room for stronger motion later where it adds value.

## Public Frontend

### Frontend intent

The public site must feel like a serious modern news service:

- readable
- image-capable
- premium
- clearly clickable
- able to carry flagship analysis and shorter story cards

### Homepage structure

The homepage should move to a cleaner editorial structure:

1. `top header`
   - brand
   - primary navigation
   - edition/meta strip

2. `lead hero`
   - strong image-backed lead card
   - clear lead headline
   - readable dek
   - obvious click target

3. `supporting rail`
   - compact latest/dispatch stack
   - easier scanning than the current dense list

4. `story grid`
   - image-led or thumbnail-led cards
   - more breathing room
   - stronger visual hierarchy

5. `optional feature media block`
   - placeholder for embedded YouTube or major visual story unit

### Article pages

Article pages should keep the improved analysis output readable:

- same header language as homepage
- stronger title hierarchy
- better body measure and paragraph rhythm
- cleaner facts/source sections
- less visual clutter around the article body

### Public imagery

For this phase, placeholder images may use safe public stock/Unsplash-style assets purely to prove layout and feel.

The system should be ready for:

- hero imagery
- story card thumbnails
- embedded video block

## Owner Admin

### Admin intent

The admin must stop behaving like a long stacked landing page.

It should become:

- one owner workspace
- faster to navigate
- easier to scan
- task-oriented
- closer to a WordPress-style control panel adapted to CoreWire workflows

### Admin structure

The admin should become an `app shell`.

#### Left sidebar

Persistent navigation for:

- Overview
- Review Queue
- Drafts
- Published
- Programming
- Analytics

#### Top utility bar

Compact status and quick context:

- system health
- publish mode
- queue count
- quick actions where useful

#### Main canvas

Task-oriented content area:

- top stat cards
- active workspace below
- reduced duplication
- less unnecessary scrolling

### Admin content model

The current single-page draft editor stays, but inside a better shell.

The admin must center practical workflows:

- review queue
- manual drafts
- published inventory
- programming controls

The editor workspace should remain inside `/admin`, not split into a CMS route tree.

### Admin UX rules

- editor workspace must feel central
- inventory and editing must be visually coordinated
- published inventory should not appear in multiple confusing places
- overview should summarize, not duplicate deeper sections
- panels should feel like dashboard tools, not article cards

## Shared System Components

The redesign should converge both surfaces on shared primitives:

- typography tokens
- color tokens
- panel/card primitives
- buttons
- form fields
- badges/eyebrows
- list rows
- hover/focus/active states

This reduces drift between admin and frontend and makes the product feel intentional.

## Accessibility and Responsiveness

The redesign must preserve:

- readable contrast
- obvious links/buttons
- keyboard-visible focus states
- usable mobile layouts

On mobile:

- public homepage stacks gracefully
- admin sidebar may collapse into a top drawer or compact nav
- editor remains usable without horizontal overflow

## Non-Goals

This redesign does not include:

- full new CMS architecture
- rich text editor
- image upload pipeline
- frontend personalization
- Paperclip UI redesign
- animation-heavy storytelling features

## Risks and Controls

- `Too much magazine styling hurts admin productivity`
  Control: shared design language, different layout models

- `Admin remains long and duplicated`
  Control: move to sidebar + canvas shell and reduce repeated lists

- `Frontend becomes generic media template`
  Control: keep CoreWire signal/dispatch motif in restrained form

- `Placeholder imagery distorts final expectations`
  Control: use it only to validate layout and hierarchy

- `Motion becomes visual noise`
  Control: keep animation subtle and purposeful

## Release Outcome

This redesign phase is complete when:

- the homepage feels modern, readable, and premium
- articles read cleanly and feel like a serious service
- the admin feels like an operational dashboard, not a stacked blog page
- both surfaces clearly belong to the same product
- the design leaves room for later polish without needing another full reset
