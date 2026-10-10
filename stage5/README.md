# Stage 5 — Optimization and scene audit

Run the script after Stages 2, 3 and 4 in the same Blender scene. It performs a **non-destructive** audit and writes the report to a Blender Text datablock named `PDHQ_STAGE5_AUDIT_REPORT`, as well as printing it to the console.

The report summarizes object/mesh counts and estimated triangle totals, collection sizes, non-unit object scale, large meshes, high-triangle meshes, meshes without materials, and mesh names that do not use the `PDHQ_` prefix.

## What this can and cannot prove
- It is a useful first-pass scene hygiene check; it does not change geometry.
- A large dimension is a review flag, not automatically a problem: building shells and site geometry can legitimately be large.
- Triangle totals are rough scene metrics, not a reliable FiveM performance prediction.
- It cannot validate Sollumz metadata, archetypes, portals, room flags, occlusion, collision quality, material texture budgets, streaming behavior, or all intersections.
- It does not export a YMAP/YTYP/YDR/YBN or a finished MLO.

## Recommended review order
1. Run Stages 2 → 3 → 4 → 5 in one Blender scene.
2. Read the report and resolve unexpected warnings.
3. Review overlapping Stage 2/3 partitions and all door openings visually.
4. Confirm garage clearance, stairs, accessible circulation, and rooftop safety.
5. Replace blockout assets with optimized production geometry and materials.
6. Prepare Sollumz assets and validate in-game with a separate export/test pass.
