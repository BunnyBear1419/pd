# Stage 50 — CodeWalker inspection and correction

## Purpose
Inspect exported assets in CodeWalker before deployment to catch asset, bounds, material, collision and placement issues.

## Workflow
1. Back up the last accepted Blender scene and exported resource.
2. Use the approved outputs of Stages 36–38 as review references, not as authoritative construction plans.
3. Complete the work in the real Blender/Sollumz/CodeWalker/FiveM toolchain.
4. Run applicable audits, inspect findings manually, and retain evidence.

## Acceptance checklist
- [ ] Open exported assets
- [ ] resolve missing textures and malformed assets
- [ ] review bounds, placement, collision and visibility
- [ ] triage all warnings
- [ ] Record tool versions, evidence, defects, reviewer and date.
- [ ] Do not treat CI/package success as proof of external toolchain or in-game validity.

## Status boundary
This stage defines the work package and acceptance gate. It is not complete until the real work and evidence exist. Do not claim production readiness without successful export, CodeWalker inspection and FiveM testing.

## Automated Blender preflight

Run this audit against the actual scene in Blender (not ordinary system Python):

```bash
blender --background build/pdhq_final.blend --python stage50/audit_stage50_collision_visibility.py -- --output build/stage50_collision_visibility.json
```

The report inventories meshes whose names suggest collision use, visibility-transition geometry, possible placeholder objects, missing material slots, zero scale components, loose geometry, and degenerate faces on collision-named candidates. It is read-only and writes a JSON report both to disk and to a Blender text datablock.

**Important:** the audit is a review aid, not a collision or visibility fix. It does not generate Sollumz collision, MLO rooms/portals, occlusion, or map suppression. Review the findings in Blender/Sollumz and CodeWalker, then test the exported resource in FiveM with fresh joins, respawns, reconnects, and multiple clients.
