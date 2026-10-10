# Stage 26 — Vertical-circulation geometry reconciliation

This pass addresses two obvious blockout conflicts before the detailed interior is generated:

- Full-footprint floor slabs and the roof deck would cover the stair/elevator openings.
- Solid stair-core and elevator-shaft placeholder masses would occupy the same space as the stair blockout and elevator.

The script replaces the three floor plates and roof deck with simple slab tiles around two 5 × 8 m stair openings and one 3.2 × 3.2 m elevator opening. It removes the solid core masses and creates non-solid guide empties instead. A JSON report is also written into the Blender Text datablocks.

## Run

The Stage 25 orchestrator runs Stage 26 immediately after Stage 2 and before Stage 3:

```powershell
blender -b --python stage25/build_stage25_scene.py -- --output build/pdhq_stage26_blockout.blend --log build/pdhq_stage26_build_report.json
```

To run manually, open the Stage 2 scene and run `stage26/reconcile_stage26_vertical_circulation.py` before running Stage 3.

## Important review items

- Confirm stair footprints, landing elevations, stair headroom, and floor-to-floor transitions in Blender.
- Confirm the elevator shaft, landing/door arrangement, and slab opening are appropriate.
- Inspect tile seams and wall/slab intersections; this is a simple grid-tile solution, not a finished structural slab.
- The openings are schematic and do not establish structural adequacy or accessibility compliance.
- The scene is still not a finished FiveM MLO. Sollumz asset setup/export, CodeWalker review, and actual FiveM tests remain required.
