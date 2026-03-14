# Paperclip Bridge Contract

## Operator Command Schema

CoreWire accepts authenticated operator commands through `/api/operator/commands`.

Supported command types:

- `create_story`
- `rerun_analysis`
- `publish_draft`
- `set_autonomy_mode`
- `disable_source`

Each command contains:

- `type`
- `payload`
- optional future correlation metadata

## Callback Schema

CoreWire should return callback-safe command results with:

- `type`
- `accepted`
- `payload`
- future status and article identifiers when asynchronous execution expands

Paperclip can persist these responses into ticket audit trails or transform them into webhook callbacks.

## Auth Model

Paperclip-to-CoreWire operator traffic must use the internal service token model.

- Header: `x-internal-token`
- Secret: `COREWIRE_INTERNAL_TOKEN`
- Scope: operator and internal execution endpoints only

Owner admin routes remain separate and use owner authentication, not the operator service token.

## Ticket Correlation Model

Each Paperclip task should map to a CoreWire command batch with correlation fields added in future iterations:

- `ticket_id`
- `actor_id`
- `company_id`
- `correlation_id`

These identifiers let Paperclip match outgoing commands, incoming callbacks, and final publish state changes to one newsroom ticket lifecycle.
