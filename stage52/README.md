# Stage 52 — Performance profiling and optimization

## Purpose
Measure and tune the real asset in a development server, focusing on geometry, textures, collision and streaming.

## Workflow
1. Back up the last accepted Blender scene and exported resource.
2. Use the approved outputs of Stages 36–38 as review references, not as authoritative construction plans.
3. Complete the work in the real Blender/Sollumz/CodeWalker/FiveM toolchain.
4. Run applicable audits, inspect findings manually, and retain evidence.

## Acceptance checklist
- [ ] Record baseline and optimized metrics
- [ ] test low/high detail views
- [ ] fix spikes
- [ ] verify no visual, collision or streaming regressions
- [ ] Record tool versions, evidence, defects, reviewer and date.
- [ ] Do not treat CI/package success as proof of external toolchain or in-game validity.

## Status boundary
This stage defines the work package and acceptance gate. It is not complete until the real work and evidence exist. Do not claim production readiness without successful export, CodeWalker inspection and FiveM testing.


## Performance evidence validator

This stage adds a schema and sanity-check gate for a measured `build/performance_profile.json`. It validates that capture conditions, geometry/material/texture counts, baseline and optimized frame time and memory, budgets, evidence references, and notes are present and internally plausible.

Example:

```bash
python stage52/validate_stage52_performance_profile.py --profile build/performance_profile.json --output build/stage52_performance_profile_validation.json
```

Run the synthetic checker test with:

```bash
python stage52/validate_stage52_performance_profile.py --self-test
```

The fixture is synthetic and is only testing the validator. Real profile values must be collected from the actual Blender scene and a repeatable FiveM staging test, with the same route, client count, game build and measurement duration for baseline and optimized comparisons. Include profiler exports/screenshots and texture inventory in the evidence list. Do not lower geometry or texture detail blindly: validate collisions, visibility, streamed loading, garage clearance and roof/helipad behavior after every optimization.

The validator flags suspicious or over-budget values for review and always returns `production_ready: false`. A passing CI run is not a runtime benchmark.
