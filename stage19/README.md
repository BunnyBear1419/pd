# Stage 19 — Collision and export preflight

## Purpose
Create an advisory inventory before converting the blockout to GTA assets. The audit identifies likely temporary guides/proxies, likely collision candidates, mesh/material basics, non-unit object scales, and modifiers that deserve review.

## Run
1. Save a backup copy of the working .blend file.
2. Open Blender's Scripting workspace and run `audit_stage19_export_preflight.py`.
3. Read `PDHQ_STAGE19_EXPORT_PREFLIGHT_REPORT` and `PDHQ_STAGE19_EXPORT_MANIFEST` in the Text Editor.
4. Review every item tagged `REVIEW_EXCLUDE_TEMPORARY_GUIDE`; do not blindly delete or exclude it.
5. Mark intended collision meshes deliberately and verify them with Sollumz/CodeWalker.

## What it checks
- Scene/object and mesh counts plus total polygon count.
- Objects whose names or collections suggest guides, clearance volumes, proxies, planning aids, or circulation helpers.
- Potential collision candidates based on names/collection names or a custom `PDHQ_collision_candidate` property.
- Meshes with no material slots, non-unit object scale, or modifiers.
- World-space bounds and a suggested per-object export disposition.

## Important limitations
This script does not create collision geometry, set GTA collision flags, repair topology, apply transforms, remove modifiers, hide/delete guides, export assets, or validate portals/occlusion/LODs. The manifest is a review aid, not an automatic export list. Final collision and drawable setup must be completed with Blender + Sollumz and checked in CodeWalker and FiveM.
