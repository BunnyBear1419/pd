# Stage 20 — LOD and performance planning

Stage 20 adds a **non-destructive Blender audit** to help prioritize manual Level of Detail (LOD) work and optimization reviews.

## Files

- `audit_stage20_lod_performance.py` — run in Blender's Scripting workspace with the police HQ scene active.
- `LOD_AND_PERFORMANCE_CHECKLIST.md` — manual review and in-game validation steps.

## Run it

1. Open the current `.blend` blockout in Blender.
2. Save a backup copy before continuing scene work.
3. Open the script in the Scripting workspace and click **Run Script**.
4. In the Text Editor, inspect `PDHQ_STAGE20_LOD_PERFORMANCE_REPORT` and `PDHQ_STAGE20_LOD_MANIFEST`.
5. Review high-polygon objects, material-slot counts, modifiers, object scale, and unused materials. Confirm each candidate visually before changing it.

The report sorts mesh objects by polygon count and assigns heuristic review categories based on polygon count and bounding dimensions. These thresholds are triage hints only; they are not certified GTA V budgets.

## Important limits

This script does not generate LODs, decimate meshes, merge materials, apply modifiers, alter scene objects, export YDR/YDD/YTYP assets, or benchmark FiveM. A Blender report cannot confirm streaming memory, draw calls, collision quality, portals, occlusion, or frame rate. Final results require Sollumz/CodeWalker review and in-game tests at near, medium, and far viewing distances.
