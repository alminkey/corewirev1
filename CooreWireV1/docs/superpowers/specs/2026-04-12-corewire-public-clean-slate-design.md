# CoreWire Public Clean-Slate Design

**Date:** 2026-04-12  
**Status:** Approved for planning  
**Scope:** Replace the current public frontend with a fully new visual and layout system while keeping the current routes and data flow.

## Why This Reset Exists

The current frontend has already gone through multiple redesign attempts and still reads as:

- the same homepage with different colors
- the same story modules in slightly different shells
- a restyled demo rather than a new product

That is not acceptable for the intended CoreWire outcome.

The problem is not execution capacity. The problem is that previous redesign work preserved too much of the old public structure:

- the same homepage composition
- the same hero logic
- the same feed rhythm
- the same article shell assumptions

This reset fixes that by treating the current public frontend as disposable.

## Product Decision

CoreWire public frontend should become a:

- **bright**
- **modern**
- **luxury**
- **digital product**

with a:

- **visually dominant lead story**
- **magazine-like presentation**
- **highly curated front page**

This is not a newspaper design.
This is not a broadcast grid.
This is not an editorial reskin.

It is a `clean-slate public product`.

## What Gets Preserved

Only these things are preserved:

- routes
- data fetching
- content entities
- article slugs
- existing backend responses
- monetization/newsletter hooks where useful

Everything else is open to replacement.

## What Gets Rejected

The following are explicitly rejected as design anchors:

- current homepage structure
- current hero composition
- current right rail concept
- current story grid logic
- current article page layout
- the idea that the page must feel like a classic news homepage

If a future implementation keeps the current layout and only changes styling, it has failed this spec.

## Core Visual Direction

### Identity

The public product should feel like:

- a premium digital media product
- deliberate and expensive
- visually clean
- modern rather than nostalgic

It should not feel like:

- old media heritage brand
- terminal newsroom
- tech dashboard with articles
- warm newspaper page

### Theme

The theme stays bright.

Key qualities:

- pale neutral base
- strong white surfaces
- dark ink typography
- restrained but premium accents
- enough contrast to feel sharp, not washed out

### Typography

Typography should signal luxury and clarity, not retro newspaper tradition.

Rules:

- strong modern sans for most UI and major display moments
- serif, if used at all, should be selective and rare
- headlines should feel designed, not inherited from old editorial defaults
- metadata should feel minimal and contemporary

### Images and media

Imagery becomes central to the public product.

Rules:

- large, cinematic lead image
- meaningful secondary images
- video/explainer module can remain if it fits the layout
- visuals should help establish a premium product feel immediately

## Homepage Design

### Homepage intent

The homepage should feel like a luxury digital front page with one overwhelming central story and a carefully staged supporting cast.

The page should communicate:

- authority
- curation
- strong editorial judgement
- modern product quality

### Homepage structure

The homepage is rebuilt around these zones:

1. `Minimal premium top frame`
   - restrained top metadata
   - clean logo
   - concise navigation
   - no heavy product chrome

2. `Massive lead story`
   - one dominant story only
   - large image
   - huge headline
   - dek and metadata
   - primary CTA
   - the lead must visually own the page

3. `Supporting story strip`
   - 2 to 4 supporting stories
   - visually smaller than the lead
   - clearly secondary
   - may mix image and text modules

4. `Feature block`
   - one strong thematic block
   - can be video, explainers, long-read, or signature package

5. `Curated lower feed`
   - not a dense portal wall
   - more selective, more spacious, more staged

### Homepage rules

- the lead story must be the emotional and visual center
- the page must breathe
- there must be fewer modules than before, not more
- supporting stories must not look like a generic news card grid
- the whole page should feel intentionally directed

## Article Page Design

### Intent

Article pages should feel like premium feature reading surfaces.

They should not feel like:

- a page assembled from utility blocks
- an old editorial article template
- a public version of admin panels

### Structure

The article page should be rebuilt around:

1. `Opening visual moment`
   - headline and visual framed as one premium entry moment

2. `Reading body`
   - spacious
   - elegant
   - consistent
   - clearly the center of gravity

3. `Support modules`
   - facts
   - analysis
   - disagreements
   - sources
   - should feel integrated and premium, not bolted-on utilities

### Rules

- body reading experience is the main value
- support modules must not dominate the body
- visual hierarchy must be cleaner and more luxurious than the current implementation

## Admin Position

Admin is not the focus of this reset.

Admin should only be:

- functional
- readable
- reasonably clean

It does not need to match the public frontend in ambition.
It only needs to avoid getting in the way.

## Success Criteria

This reset succeeds when:

- the homepage reads as a completely different product
- the public site no longer resembles the old demo structure
- the lead story truly dominates the front page
- the article page feels premium and deliberate
- the result clearly moves beyond reskinned cards and rails

This reset fails if:

- the old homepage skeleton is still recognizable
- the lead story does not visually own the page
- the lower page still reads like a generic portal grid
- the article page still feels like modular scaffolding in public clothing
