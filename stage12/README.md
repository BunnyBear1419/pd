# Stage 12 — Door and Access-Point Blockout

This stage adds schematic door leaves, handles, vision panels, threshold markers, and access-reader props in a dedicated collection.

## Run order
Run Stages 2, 3, and 4 first, in the same Blender scene, then run `generate_stage12_doors_access.py`.

## Important limitations
- Door locations are based on Stage 3's current schematic opening centres.
- The current interior layout is still provisional; inspect every door against its actual opening and furniture.
- Door leaves are static geometry only. No opening animation, keycard logic, job permissions, or collision behavior is implemented.
- Reader props are visual indicators only and do not connect to FiveM scripts.
- This is not production-ready Sollumz/GTA geometry. Review collision, pivots, door swing clearance, LODs, and export behavior before release.
