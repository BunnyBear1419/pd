# Stage 47 — Geometry budget and LOD review

Stage 47 creates a review plan from the Stage 42 shell and Stage 43 furniture blockout, plus a read-only Blender scene audit.

## Files
- `generate_stage47_geometry_lod_plan.py`: records schematic geometry counts, LOD guidance and the evidence needed before release.
- `audit_stage47_blender_geometry.py`: run inside Blender to report evaluated triangle estimates, material-slot counts, missing UV layers, unusual object scale and high-poly review candidates.

## Run planning report
```bash
python stage42/generate_stage42_shell_geometry.py --output build/stage42_shell_geometry.json
python stage43/generate_stage43_furniture_blockout.py --spec build/stage41_48_design_spec.json --fit-report build/stage37_floor_fit.json --output build/stage43_furniture_blockout.json
python stage47/generate_stage47_geometry_lod_plan.py --shell build/stage42_shell_geometry.json --furniture build/stage43_furniture_blockout.json --output build/stage47_geometry_lod_plan.json
```

## Audit a real scene (read-only)
```bash
blender --background path/to/your_scene.blend --python stage47/audit_stage47_blender_geometry.py -- --output build/stage47_blender_geometry_audit.json
```

The Blender audit does not decimate meshes, delete hidden faces, create LODs or edit collision. Treat triangle/material thresholds as review prompts, not universal limits. Keep collision simpler than render geometry where feasible, and validate walkable surfaces, doorways, vehicle clearance, CodeWalker export, FiveM frame time and memory. Stage 47 remains not production-ready until the actual scene and in-game evidence have been reviewed.
