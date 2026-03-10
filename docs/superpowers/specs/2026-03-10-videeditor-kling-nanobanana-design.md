# VideEditor Kling and Nanobanana Fork Design

## Scope

Fork `LTX-Desktop` into `F:\2026\CoreWire\VideEditor` as an API-only desktop app.

Provider split:
- `Kling` handles all video generation and video edit flows.
- `Nanobanana` handles all image generation and image edit flows.

Keep where practical:
- Electron shell
- React editor UX
- timeline and asset workflow
- project/session flow
- export flows not tied to local inference

Remove:
- local LTX inference
- model downloads and weights
- GPU/CUDA readiness setup
- local runtime onboarding

Sources:
- https://github.com/Lightricks/LTX-Desktop
- https://github.com/Lightricks/LTX-Desktop/blob/main/backend/architecture.md
- https://github.com/Lightricks/LTX-Desktop/blob/main/README.md

## Architecture

Keep three layers:
1. Electron shell
2. React frontend
3. Local Python backend orchestrator

The backend becomes a provider-normalization layer instead of a local inference layer.

Add two abstractions:
- `VideoProvider`
- `ImageProvider`

Concrete adapters:
- `KlingVideoProvider`
- `NanobananaImageProvider`

Routes and handlers must depend on these abstractions instead of LTX services.

## Internal Contracts

Use a provider-neutral job model with fields like:
- `job_id`
- `job_type`
- `provider`
- `status`
- `progress`
- `result_assets`
- `error`

Job types:
- `video_generate`
- `video_edit`
- `image_generate`
- `image_edit`

Statuses:
- `queued`
- `running`
- `completed`
- `failed`
- `cancelled`

## Capability-Driven UI

Frontend must read backend capabilities from an endpoint such as `/api/capabilities`.

Capabilities should include:
- provider configured flags
- supported video modes
- supported image modes
- supported aspect ratios and durations
- supported edit workflows

Frontend uses this to hide unsupported actions instead of exposing dead controls.

## Functional Mapping

`Kling` owns:
- text-to-video
- image-to-video
- any retake/edit flow only if the API truly supports an equivalent
- audio-to-video only if supported in reality

`Nanobanana` owns:
- text-to-image
- image edit
- inpaint/outpaint style edits if supported
- reference-image transformations

Unsupported LTX-only flows should be removed or hidden.

## Settings and UX

Replace LTX runtime settings with:
- `Kling API Key`
- `Nanobanana API Key`
- optional default model pickers
- provider health / connection checks

Remove all model download, GPU, CUDA, and weight-management UI.

## Risks

Main risks:
- feature mismatch between LTX and Kling/Nanobanana
- hidden LTX-specific assumptions in frontend state or project files
- async polling differences across providers
- secret handling in an API-only desktop app

Mitigations:
- strict adapter boundary
- capability endpoint
- normalized error model
- backend-owned credential handling

## Rollout

1. Fork into `VideEditor`.
2. Add provider-neutral backend contracts and capability endpoint.
3. Integrate Kling and Nanobanana.
4. Replace settings/onboarding with provider config.
5. Remove leftover LTX runtime code and finish rename cleanup.

## Acceptance Criteria

- app starts with no local inference requirements
- video flows route through Kling
- image flows route through Nanobanana
- unsupported features are hidden or reported as unsupported
- editor experience outside provider-specific controls remains intact