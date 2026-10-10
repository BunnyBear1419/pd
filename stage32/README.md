# Stage 32 — Production Handoff Audit

Stage 32 consolidates the repository inventory and the remaining external production gates into one JSON report. It intentionally separates **source/package completeness** from **actual MLO readiness**.

## Run

From the repository root:

```bash
python stage32/final_stage32_production_handoff.py --root . --output build/stage32_production_handoff.json
```

The audit writes a report even when the Blender scene or exported resource is missing. That is an expected finding during development, not a CI packaging failure. It exits nonzero only for command-line/root errors, not for ordinary readiness blockers.

## Status meanings

- `BLOCKED_MISSING_PROJECT_FILES`: required source or handoff files are absent.
- `BLOCKED_SCENE_NOT_BUILT`: repository files exist, but the expected Blender output is missing.
- `BLOCKED_GTA_RESOURCE_NOT_EXPORTED`: a scene exists, but the expected resource manifest/stream folder is missing.
- `EXTERNAL_VALIDATION_REQUIRED`: expected files exist; Blender, Sollumz, CodeWalker, and FiveM acceptance is still required.

This is a filesystem inventory, not a Blender execution test, exporter, geometry validator, or certification. It never sets `production_ready` to true.
