# Paperclip Bridge Contract

## Roles

- **CoreWire** is the canonical owner control plane: article generation, editorial review, compliance, and publishing.
- **Paperclip** is an external orchestration environment that reads CoreWire state and sends authenticated commands. It is not a second admin UI.

## Bridge Read Endpoints

All read endpoints require the `x-internal-token` header. They return compact summaries of live CoreWire state.

| Endpoint | Returns |
|---|---|
| `GET /api/operator/bridge/status` | Health, autonomy mode, pause state, queue counts, published counts, recent activity |
| `GET /api/operator/bridge/review-queue` | Pending drafts, low-confidence items, and flagged items with totals |
| `GET /api/operator/bridge/published` | Total published count and the 10 most recent published articles |
| `GET /api/operator/bridge/autonomy` | Current autonomy mode and all publish gate flags |

## Operator Command Schema

CoreWire accepts authenticated operator commands through `POST /api/operator/commands`.

Supported command types:

- `discover_trending_story`
- `build_story_draft`
- `run_content_pipeline`
- `publish_preview_article`
- `publish_article`
- `publish_if_eligible`
- `archive_preview_article`
- `import_external_draft`
- `rerun_story`
- `set_autonomy_mode`

Each command contains:

- `type`
- `payload`
- optional correlation metadata (see Ticket Correlation Model)

`import_external_draft` accepts a Paperclip-provided draft body and routes it through CoreWire review and compliance — it never auto-publishes regardless of confidence level.

## Callback Schema

CoreWire returns callback-safe command results with:

- `type`
- `accepted`
- `payload` or `draft`, `article`, `review_item` depending on command type
- `correlation` — the full set of correlation fields echoed back

Paperclip can persist these responses into ticket audit trails or transform them into webhook callbacks.

## Auth Model

Paperclip-to-CoreWire operator traffic must use the internal service token model.

- Header: `x-internal-token`
- Secret: `COREWIRE_INTERNAL_TOKEN`
- Scope: operator bridge read endpoints and command endpoints only

Owner admin routes remain separate and use owner authentication, not the operator service token.

## Ticket Correlation Model

Each Paperclip task should map to a CoreWire command batch with these correlation fields:

- `ticket_id`
- `actor_id`
- `company_id`
- `correlation_id`
- `requested_by`

All fields are optional. CoreWire echoes them back on every command response under `correlation` so Paperclip can match outgoing commands, incoming callbacks, and final publish state changes to one newsroom ticket lifecycle.
