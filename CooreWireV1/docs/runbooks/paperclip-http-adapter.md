# Paperclip HTTP Adapter Setup

This runbook covers how to wire Paperclip to CoreWire via the HTTP adapter bridge.

## Prerequisites

- CoreWire API running and reachable (staging: `http://213.202.216.222/api`)
- `COREWIRE_INTERNAL_TOKEN` set in the Paperclip environment

## Auth

All bridge requests must include the internal service token header:

```
x-internal-token: <COREWIRE_INTERNAL_TOKEN value>
```

Without this header every bridge endpoint returns `403 Forbidden`.

## Reading CoreWire State

The four read endpoints require only the auth header — no request body.

```bash
# System status
curl -H "x-internal-token: $COREWIRE_INTERNAL_TOKEN" \
  http://<host>/api/operator/bridge/status

# Review queue
curl -H "x-internal-token: $COREWIRE_INTERNAL_TOKEN" \
  http://<host>/api/operator/bridge/review-queue

# Published articles summary
curl -H "x-internal-token: $COREWIRE_INTERNAL_TOKEN" \
  http://<host>/api/operator/bridge/published

# Autonomy state
curl -H "x-internal-token: $COREWIRE_INTERNAL_TOKEN" \
  http://<host>/api/operator/bridge/autonomy
```

## Sending Commands

Commands go to `POST /api/operator/commands` as a batch:

```json
{
  "commands": [
    {
      "type": "import_external_draft",
      "ticket_id": "PAPER-1234",
      "actor_id": "paperclip-agent",
      "company_id": "acme-corp",
      "correlation_id": "uuid-here",
      "requested_by": "editorial-workflow",
      "payload": {
        "draft": {
          "headline": "...",
          "dek": "...",
          "fact_blocks": [],
          "analysis_blocks": [],
          "sources": []
        },
        "confidence": { "level": "medium", "homepage_eligible": false }
      }
    }
  ]
}
```

CoreWire echoes back the full `correlation` object on every command result so Paperclip can match responses to outgoing tickets.

## Correlation Fields

All correlation fields are optional but recommended for audit trails:

| Field | Purpose |
|---|---|
| `ticket_id` | Paperclip ticket or task identifier |
| `actor_id` | Agent or user that initiated the command |
| `company_id` | Tenant or organisation identifier |
| `correlation_id` | Unique trace ID for this command execution |
| `requested_by` | Workflow or system that requested the action |

## Staging Smoke Flow

1. `GET /api/operator/bridge/status` — verify `health.system == "ok"`
2. `GET /api/operator/bridge/autonomy` — confirm expected autonomy mode
3. Send one `import_external_draft` command with a minimal draft
4. Confirm response has `accepted: true` and a `review_item` in the queue
5. `GET /api/operator/bridge/review-queue` — confirm the draft appears in `pending_drafts` or `flagged_items`
