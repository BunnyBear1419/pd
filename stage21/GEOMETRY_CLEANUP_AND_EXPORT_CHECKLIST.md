# Geometry cleanup and export checklist

## Save and audit

- [ ] Save a versioned backup of the `.blend` file before cleanup.
- [ ] Run `audit_stage21_geometry_cleanup.py` and retain the JSON report.
- [ ] Review guide/proxy candidates manually; confirm intended use before hiding or excluding any object.
- [ ] Review near-zero dimensions, extreme dimensions, shared mesh data, missing materials, and non-manifold edge candidates.
- [ ] Treat AABB overlaps as prompts for visual inspection, not automatic failures.

## Architecture and circulation

- [ ] Confirm each floor slab has intentional openings for the stairwell and elevator shaft; verify no slab blocks a shaft or stair landing.
- [ ] Check stairs, landings, guardrails, door openings, door leaves, and access points for continuity and player clearance.
- [ ] Inspect all facade details, mullions, signage, emblems, canopy pieces, and interior finish layers for z-fighting and accidental intersections.
- [ ] Confirm booking/cells, dispatch, evidence, armory, detective rooms, interview rooms, lockers/showers, SWAT briefing, garage, roof, and helipad remain reachable.
- [ ] Check garage entry/exit, turning envelope, vehicle clearance, pedestrian path, emergency lane, service approach, and perimeter gates.
- [ ] Review roof edge protection, helipad approach, HVAC obstructions, and rooftop access.

## Geometry and materials

- [ ] Recalculate normals where appropriate and inspect backfaces; do not blindly fill open surfaces that are intentionally single-sided.
- [ ] Remove hidden/internal faces only after checking they do not form needed collision or visible interior surfaces.
- [ ] Reduce excessive bevels and unnecessary geometry while preserving the architectural silhouette.
- [ ] Standardize material assignments and UVs; check texture scale, naming, and resolution.
- [ ] Keep render meshes and collision meshes separate where required by the current Sollumz workflow.
- [ ] Verify object origins, transforms, naming, collections, and export inclusion/exclusion decisions.

## Export gate

- [ ] Export reviewed assets using the compatible Sollumz workflow; inspect archetypes and bounds in CodeWalker.
- [ ] Verify collision, portals, occlusion, LODs, and streaming configuration as separate tasks.
- [ ] Test entry/exit, stairs, doors, cells, garage vehicles, roof access, and helipad in FiveM.
- [ ] Test a clean client and the target server's full resource set; watch for missing textures, invisible geometry, default GTA building overlap, and streaming conflicts.
- [ ] Keep a known-good build and compare changes one batch at a time.

## Interpretation

The audit is advisory. It does not automatically fix geometry or guarantee a valid GTA V/FiveM MLO. Do not call the asset production-ready until the exported build has passed visual, collision, streaming, and in-game checks.
