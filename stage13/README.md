# Stage 13 — Garage Circulation and Vehicle Clearance

Adds a separate guide collection for three nominal vehicle bays, bay floor markings, a drive-aisle review volume, a pedestrian path strip, and clearance volumes aligned to Stage 4's vehicle proxy locations.

## Run order
1. Run Stages 2, 3, and 4 in one Blender scene.
2. Run `generate_stage13_garage_circulation.py`.
3. Inspect `PDHQ_GARAGE_CIRCULATION_GUIDES` and compare with actual room boundaries.

## Important
The current garage location and circulation paths are provisional. This script intentionally does not move previous furniture or structure objects. Wireframe volumes and floor marks are planning aids, not proof of vehicle fit or walkable navigation. Check turning paths for patrol sedans, SUVs, and larger tactical vehicles; verify pedestrian separation, door openings, ramp/entrance geometry, slab clearance, and collision in the actual scene. Remove or replace review-only volumes before production export.
