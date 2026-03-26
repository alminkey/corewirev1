# Content Batch Runbook

Use this runbook to create the first batch of real articles through the composite operator flow.

## Prerequisites

- API running locally or on the target environment
- `COREWIRE_INTERNAL_TOKEN` available
- OpenRouter configured in the environment

## Run a batch locally

From the project root:

```bash
python scripts/content_batch_runner.py
```

Optional environment overrides:

- `COREWIRE_BATCH_SIZE`
- `COREWIRE_API_BASE_URL`
- `COREWIRE_INTERNAL_TOKEN`
- `COREWIRE_CONTENT_DOMAIN`

## Output

Each batch writes a JSON summary to:

```bash
artifacts/content-batches/content-batch-<timestamp>.json
```

The summary records:

- selected candidates
- draft metadata
- publish decisions
- published articles
- review queue items

## Operating rule

- `high confidence` stories with enough linked sources should auto-publish
- `medium/low/flagged` stories should land in the owner review queue
