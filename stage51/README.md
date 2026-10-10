# Stage 51 — FiveM resource assembly

## Purpose
Assemble the actual resource with fxmanifest.lua, stream assets, metadata and installation notes; do not ship templates as finished assets.

## Workflow
1. Back up the last accepted Blender scene and exported resource.
2. Use the approved outputs of Stages 36–38 as review references, not as authoritative construction plans.
3. Complete the work in the real Blender/Sollumz/CodeWalker/FiveM toolchain.
4. Run applicable audits, inspect findings manually, and retain evidence.

## Acceptance checklist
- [ ] Manifest paths match real files
- [ ] dependencies are declared
- [ ] no placeholder template remains
- [ ] resource starts cleanly
- [ ] install/rollback steps work
- [ ] Record tool versions, evidence, defects, reviewer and date.
- [ ] Do not treat CI/package success as proof of external toolchain or in-game validity.

## Status boundary
This stage defines the work package and acceptance gate. It is not complete until the real work and evidence exist. Do not claim production readiness without successful export, CodeWalker inspection and FiveM testing.
