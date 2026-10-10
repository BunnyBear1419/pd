# Stage 46 — UV mapping and texture-atlas preparation

Stage 46 creates a UV/atlas planning manifest and a read-only Blender audit for an actual scene.

## Files
- `generate_stage46_uv_plan.py`: creates atlas grouping and per-asset-class UV guidance from the Stage 45 material manifest.
- `audit_stage46_uvs_blender.py`: run inside Blender to report missing active UV layers, UV coordinates outside 0–1, zero-area polygons, and high material-slot counts. It does not change meshes.

## Run the plan
```bash
python stage45/generate_stage45_material_manifest.py --output build/stage45_material_manifest.json
python stage46/generate_stage46_uv_plan.py --materials build/stage45_material_manifest.json --output build/stage46_uv_atlas_plan.json
```

## Audit a real Blender scene
```bash
blender --background path/to/your_scene.blend --python stage46/audit_stage46_uvs_blender.py -- --output build/stage46_uv_audit.json
```

The audit is intentionally read-only. UVs outside 0–1 may be intentional for tiling, and overlapping UV islands may be correct for mirrored/reused assets. Review flagged objects before editing. This stage does not create texture images, unwrap meshes, or export GTA assets. Use a versioned scene copy and validate in Sollumz/CodeWalker/FiveM before treating anything as production-ready.
