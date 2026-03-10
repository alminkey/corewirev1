# VideEditor Kling and Nanobanana Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `VideEditor` as an API-only fork of `LTX-Desktop` with Kling for video and Nanobanana for image generation and editing.

**Architecture:** Keep Electron, React, and Python backend structure, replace LTX services with provider-neutral contracts, and make the frontend capability-driven.

**Tech Stack:** Electron, React/TypeScript, Python backend, provider HTTP APIs

---

## File Structure
- Create: `F:\2026\CoreWire\VideEditor\`
- Modify: `VideEditor/backend/...`
- Modify: `VideEditor/frontend/...`
- Modify: `VideEditor/electron/...`
- Create: `VideEditor/backend/services/providers/video_provider.py`
- Create: `VideEditor/backend/services/providers/image_provider.py`
- Create: `VideEditor/backend/services/providers/kling_video_provider.py`
- Create: `VideEditor/backend/services/providers/nanobanana_image_provider.py`
- Create: `VideEditor/backend/models/job_models.py`
- Create: `VideEditor/backend/routes/capabilities.py`
- Create: `VideEditor/docs/provider-mapping.md`

## Chunk 1: Fork and Inventory

### Task 1: Bootstrap the fork
- [ ] Copy `LTX-Desktop` into `F:\2026\CoreWire\VideEditor`.
- [ ] Record upstream baseline with `git remote -v` and `git rev-parse HEAD`.
- [ ] Update `VideEditor/README.md` to describe the API-only fork.
- [ ] Commit: `chore: bootstrap VideEditor fork`

### Task 2: Inventory LTX-specific codepaths
- [ ] Run: `rg -n "LTX|ltx|CUDA|weights|download model|retake|generate-image" VideEditor`
- [ ] Document routes, handlers, settings screens, and generation panels touching video/image generation.
- [ ] Mark each path as keep, adapt, or remove in `VideEditor/docs/provider-mapping.md`.
- [ ] Commit: `docs: map LTX generation flows for provider swap`

## Chunk 2: Backend Abstractions

### Task 3: Add provider-neutral contracts
- [ ] Write failing backend tests for normalized job models and unsupported capability errors.
- [ ] Implement `video_provider.py`, `image_provider.py`, and `job_models.py`.
- [ ] Run backend tests until they pass.
- [ ] Commit: `refactor: add provider-neutral generation contracts`

### Task 4: Add capability endpoint
- [ ] Write a failing backend route test for `/api/capabilities`.
- [ ] Implement `backend/routes/capabilities.py` and route registration.
- [ ] Return configured providers and supported modes in normalized form.
- [ ] Run tests and commit: `feat: add normalized capabilities endpoint`

## Chunk 3: Provider Integrations

### Task 5: Implement `KlingVideoProvider`
- [ ] Write failing provider tests for text-to-video, image-to-video, polling normalization, and failure mapping.
- [ ] Implement `kling_video_provider.py`.
- [ ] Run tests and commit: `feat: add Kling video provider adapter`

### Task 6: Route video flows through Kling
- [ ] Write failing integration tests for existing video routes/handlers.
- [ ] Replace LTX calls with `VideoProvider` usage.
- [ ] Run tests and commit: `refactor: route video generation through Kling provider`

### Task 7: Implement `NanobananaImageProvider`
- [ ] Write failing provider tests for text-to-image, image edit, unsupported mode handling, and result normalization.
- [ ] Implement `nanobanana_image_provider.py`.
- [ ] Run tests and commit: `feat: add Nanobanana image provider adapter`

### Task 8: Route image flows through Nanobanana
- [ ] Write failing integration tests for image routes/handlers.
- [ ] Replace old image service calls with `ImageProvider` usage.
- [ ] Run tests and commit: `refactor: route image flows through Nanobanana provider`

## Chunk 4: Frontend and Cleanup

### Task 9: Replace local-runtime settings
- [ ] Write failing frontend tests asserting LTX setup UI is gone and provider API key fields exist.
- [ ] Add `Kling API Key` and `Nanobanana API Key` settings with health indicators.
- [ ] Remove local model, GPU, CUDA, and weights UI.
- [ ] Run tests and commit: `feat: replace LTX setup with provider settings`

### Task 10: Make generation UI capability-driven
- [ ] Write failing frontend tests for supported and unsupported control visibility.
- [ ] Fetch backend capabilities in the frontend.
- [ ] Hide unsupported features and show provider-not-configured states.
- [ ] Run tests and commit: `feat: gate generation UI by backend capabilities`

### Task 11: Remove obsolete local-runtime code
- [ ] Write a failing smoke test or startup assertion that the app should run without local inference prerequisites.
- [ ] Remove local LTX startup and hardware checks.
- [ ] Run smoke tests and commit: `refactor: remove local LTX runtime requirements`

### Task 12: Finalize visible rename and docs
- [ ] Run: `rg -n "LTX|ltx" VideEditor`
- [ ] Rename remaining visible LTX strings relevant to product UX.
- [ ] Run app startup smoke verification.
- [ ] Commit: `chore: finalize VideEditor branding and docs`

## Verification Checklist
- [ ] backend tests pass for provider contracts, routes, and integrations
- [ ] frontend tests pass for settings and capability gating
- [ ] app startup works without local model download or GPU setup
- [ ] video jobs use Kling configuration paths
- [ ] image jobs use Nanobanana configuration paths
- [ ] unsupported features are hidden or reported cleanly
- [ ] README explains API-only setup

Plan complete and saved to `docs/superpowers/plans/2026-03-10-videeditor-kling-nanobanana-implementation.md`. Ready to execute?