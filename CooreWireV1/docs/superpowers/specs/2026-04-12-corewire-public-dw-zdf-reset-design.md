# CoreWire Public DW/ZDF Reset Design

**Date:** 2026-04-12  
**Status:** Approved for planning  
**Scope:** Replace the current public frontend direction with a denser, more active international news-service layout using `dw.com` as the primary structural reference and `zdfheute.de` header/navigation discipline as the secondary reference.

## Why This Reset Exists

The previous public clean-slate rewrite solved the old problem only partially:

- it stopped looking like the exact original demo shell
- but it still did not read as a truly different, fully formed product
- it felt too sparse, too staged, and too much like a polished mockup

The user wants CoreWire to behave visually like a serious, active, international news service, not a landing page with a large hero and too little editorial density.

This reset replaces the previous public direction.

## Product Decision

CoreWire public frontend should become:

- **bright**
- **modern**
- **active**
- **international**
- **news-service driven**

with:

- a **dominant lead story**
- a **denser homepage rhythm**
- **clear editorial zones**
- a **strong navigation frame**
- a **modern product feel without retro newsroom styling**

This is not:

- a luxury landing page
- a retro editorial newspaper
- a sparse product showcase
- a dashboard pretending to be a news site

It is a **modern international news portal with premium discipline**.

## Reference Direction

### Primary reference: `dw.com`

What to inherit:

- active modular homepage rhythm
- strong international-news hierarchy
- multiple editorial zones on the homepage
- clear visual prioritization of top stories
- homepage that feels alive and current instead of decorative

### Secondary reference: `zdfheute.de`

What to inherit:

- header/navigation model
- compact but strong top structure
- clear thematic entry points
- useful utility access patterns
- faster, more deliberate section switching behavior

The header should lean closer to `ZDFheute`.
The homepage body structure should lean closer to `DW`.

## What Gets Preserved

Only these things remain stable:

- routes
- backend data contracts
- article slugs
- API client usage
- newsletter/monetization hooks where still useful

Everything about the current public presentation is replaceable.

## What Gets Rejected

The previous `clean-slate luxury landing` direction is no longer the target.

Explicitly rejected:

- sparse homepage with too much empty space
- lead story without enough surrounding editorial density
- support strip made of tiny secondary cards
- article pages that look too staged or decorative
- any attempt to keep the current public shell and only restyle it

## Core Visual Direction

### Identity

The public product should feel like:

- a global information service
- modern and deliberate
- active and current
- editorially serious
- digitally native

It should not feel like:

- nostalgic print media
- a demo template
- a thin startup landing page
- a dark terminal newsroom

### Theme

The theme remains bright.

Key properties:

- pale neutral base
- crisp white and off-white surfaces
- strong dark typography
- selective accent color for active states and signals
- cleaner, higher-contrast sections

### Typography

Typography should prioritize modern information clarity first.

Rules:

- modern sans as the main system
- display serif may be used selectively, but must not define the whole product
- headlines should feel news-driven, not retro editorial
- metadata and utility text should feel concise and structured

### Imagery

Imagery stays important, but no longer acts alone.

Rules:

- lead image remains strong
- secondary modules should use meaningful supporting imagery
- video and explainer modules are welcome
- imagery must support an active portal, not a gallery-like landing page

## Header Design

The header must be rebuilt in the spirit of `ZDFheute`.

### Structure

1. `Utility row`
   - date
   - lightweight edition/status label
   - search/newsletter/admin/video utility actions

2. `Primary brand/navigation row`
   - strong CoreWire brand anchor
   - concise section navigation
   - compact active-state treatment

### Rules

- header must feel tighter and more functional than the previous attempts
- it must not look ornamental
- it must support fast movement through sections
- it should remain sticky on desktop

## Homepage Design

### Intent

The homepage should feel like a living, edited international front page.

It should communicate:

- immediacy
- authority
- clear hierarchy
- editorial volume
- modern product discipline

### Homepage structure

1. `Strong header frame`
   - ZDF-like navigation shell

2. `Lead cluster`
   - one dominant lead story
   - adjacent live/latest desk or companion rail
   - stronger support around the lead than in the previous attempt

3. `Top secondary band`
   - 3 to 5 significant secondary stories
   - not tiny cards
   - enough surface area to matter

4. `Analysis/feature zone`
   - one major analysis or explainer band
   - can include video or issue packaging

5. `Sectioned editorial blocks`
   - world
   - security
   - economy
   - analysis
   - each as a visually coherent section, not just more of the same cards

6. `Lower live/current feed`
   - denser than previous attempts
   - still controlled and readable

### Homepage rules

- the homepage must feel clearly denser than the previous rewrite
- the lead story still dominates, but the surrounding editorial structure must feel real
- supporting stories must have enough weight to make the page feel alive
- lower sections must feel like purposeful zones, not repeated generic cards
- the result should read as an active portal, not a staged showcase

## Article Page Design

### Intent

Article pages should feel like modern, readable, international-news feature pages.

They should not feel like:

- decorative landing modules
- old editorial templates
- utility stacks with premium paint

### Structure

1. `Article hero frame`
   - headline
   - dek
   - media
   - metadata

2. `Reading column`
   - highly readable body width
   - strong paragraph rhythm
   - better hierarchy between body and side/support content

3. `Support zone`
   - facts
   - analysis
   - sources
   - related or current context

### Rules

- article reading experience must feel more practical and less theatrical
- support modules should feel integrated into a serious news page
- the article should visually belong to the same product as the homepage

## Admin Position

Admin is not the design focus of this reset.

Admin should remain:

- functional
- readable
- structurally clean

Only usability issues should be addressed as part of this frontend reset.

## Success Criteria

This reset succeeds when:

- the homepage feels like a real active news portal
- the header clearly reads differently from earlier attempts
- the page density is closer to `DW` than to a sparse landing page
- the site no longer feels like the same demo with a bigger hero
- the public site looks suitable for a serious modern international service

This reset fails if:

- the homepage remains sparse
- secondary stories still feel tiny or cosmetic
- the body still reads like the previous clean-slate landing attempt
- the header does not meaningfully improve navigation and product feel
