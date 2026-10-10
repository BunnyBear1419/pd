# Stage 35 — Floor-by-Floor Architectural Coordination

Stage 35 adds a non-destructive Blender-side coordination pass for the schematic police HQ. It checks the expected elevations of floor slab tiles, verifies that tile bounds do not intrude into the planned stair/elevator opening footprints, checks the circulation guide empties, and screens the helipad platform against the nominal roof footprint.

## Run

```powershell
blender -b build/pdhq_stage34_blockout.blend --python stage35/audit_stage35_floor_coordination.py
```

The report is written to Blender's Text datablock `PDHQ_STAGE35_FLOOR_COORDINATION_REPORT`. The Stage 25 orchestrator runs it after Stage 34 as part of the full audit sequence and writes the updated build to `build/pdhq_stage35_blockout.blend` by default.

## How to use the results

1. Open the saved scene in Blender and inspect the report.
2. Inspect each flagged slab tile and opening in top and side views.
3. Confirm stairs, landings, elevator shaft, doors, roof access and slab edges line up in all floors.
4. Confirm the helipad fits the roof plan, then separately inspect obstacles, safe approach and edge protection.
5. Record intentional overlaps or guide mismatches before detailed modeling.

## Limitations

This is coordinate/AABB screening for the current schematic, not exact mesh-intersection testing, architectural approval, structural engineering, accessibility or fire-code certification, or a FiveM MLO validator. It does not modify geometry or generate final collision, portals, occlusion, LODs, archetypes or Sollumz assets. Blender review, Sollumz/CodeWalker checks and multiplayer FiveM tests remain mandatory.
