# Stage 21 — Geometry cleanup and export preparation

Stage 21 adds a non-destructive Blender scene audit before detailed export preparation.

## Files

- `audit_stage21_geometry_cleanup.py` — runs against the active Blender scene.
- `GEOMETRY_CLEANUP_AND_EXPORT_CHECKLIST.md` — manual review checklist.

## Run it

1. Save a backup copy of the `.blend` project.
2. Open the script in Blender's Scripting workspace and run it.
3. Read the `PDHQ_STAGE21_GEOMETRY_CLEANUP_REPORT` text block.
4. Inspect every flagged item visually before making edits. Save a separate cleaned version after each major cleanup pass.

The report flags likely temporary guides, near-zero or unusually large mesh dimensions, non-manifold edges, shared mesh data, missing materials, and potential axis-aligned bounding-box overlaps. Layered architectural surfaces often overlap intentionally, so overlap results are review prompts rather than errors.

## Important limits

This script does not repair geometry, delete guide objects, create collision meshes, cut stair/elevator slab openings, or export assets. A successful Python syntax check is not a Blender scene test. Inspect the actual `.blend`, use Sollumz and CodeWalker for asset preparation/inspection, and test the result in FiveM before considering the MLO complete.
