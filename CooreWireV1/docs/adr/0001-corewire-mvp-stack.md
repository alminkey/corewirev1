# ADR 0001: CoreWire MVP Stack

## Status

Accepted

## Context

CoreWire needs an MVP stack that can support autonomous ingest, evidence-driven analysis, confidence-based publishing, and a premium public reading experience without introducing early operational sprawl.

## Decision

Use a modular monolith split across:

- `apps/api` for Python API and persistence models
- `apps/workers` for ingest and analysis jobs
- `apps/web` for the public web interface
- `PostgreSQL`, `Redis`, and `MinIO` for local infrastructure

Use typed contracts in `packages/contracts` to centralize shared statuses and pipeline enums.

## Consequences

- Python remains the center of gravity for extraction and analysis workflows.
- The frontend can evolve independently while preserving the command-center visual system.
- The system is easier to ship quickly than an early microservice design.
- Some runtime integration is still skeletal, so later work must connect the current service stubs to real persistence and queue infrastructure.
