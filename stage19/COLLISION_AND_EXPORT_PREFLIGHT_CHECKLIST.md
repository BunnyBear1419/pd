# Stage 19 — Collision and export preflight checklist

## Before running
- [ ] Save a separate backup of the .blend file.
- [ ] Run the audit on the combined scene after Stages 2–18.
- [ ] Keep the original scene intact while reviewing report output.

## Geometry and collision
- [ ] Identify final visual meshes separately from temporary guide/proxy geometry.
- [ ] Design simple collision meshes for walkable floors, walls, doors, stairs, railings, and fixed large props.
- [ ] Avoid detailed/high-polygon collision where simple convex or box-like collision is sufficient.
- [ ] Check stair collision and walkable slopes in-game.
- [ ] Confirm garage vehicle access and vehicle clearance with real test vehicles.
- [ ] Verify all collision objects and flags in Sollumz/CodeWalker; this audit cannot validate them.

## Export hygiene
- [ ] Review every `REVIEW_EXCLUDE_TEMPORARY_GUIDE` entry manually.
- [ ] Hide or exclude yellow clearance volumes, zone labels, route dashes, access markers, and planning envelopes from production export.
- [ ] Review non-unit object scales and apply transforms only after checking geometry/modifier effects.
- [ ] Resolve missing material assignments and review modifier application.
- [ ] Keep shared material usage consistent and avoid unnecessary material slots.
- [ ] Create and verify LODs, portals, and occlusion where appropriate.
- [ ] Validate resource naming, drawable hierarchy, collision, and streaming setup in CodeWalker.
- [ ] Test spawn-in, interiors, visibility, collision, stair traversal, doors, garage entry, and performance in FiveM.

## Gate
Do not label the MLO production-ready until the exported resource has passed CodeWalker review and multiplayer FiveM testing.
