# Stage 34 — Architecture & Geometry Acceptance Checklist

- [ ] Run the audit in the same Blender version used for the scene build.
- [ ] Confirm the report exists in Blender Text datablocks and the saved scene is versioned.
- [ ] Review zero/nearly-zero world-dimension objects; classify intentional guides versus defective geometry.
- [ ] Review unusually large bounds for unit mistakes, stray vertices, or accidental giant objects.
- [ ] Review every structural AABB overlap candidate in the 3D viewport; document intentional joins.
- [ ] Confirm stair and elevator voids align through all occupied floors and do not intersect usable landings.
- [ ] Manually verify door openings, door swings, accessible routes, and corridor clear widths.
- [ ] Verify garage entry, aisle, vehicle turning/clearance, and pedestrian routes.
- [ ] Verify rooftop access, helipad deck boundaries, and unobstructed safety/approach areas.
- [ ] Confirm public, staff, booking, evidence, armory, and detainee routes remain appropriately separated.
- [ ] Re-run Stages 27–30 after any geometry changes; treat their checks as heuristics.
- [ ] Do not interpret CI success or this report as proof of a finished FiveM MLO.
- [ ] After detailed modeling, author/validate collision, portals/occlusion, LODs and archetypes in the appropriate toolchain; inspect in CodeWalker and test in FiveM.
