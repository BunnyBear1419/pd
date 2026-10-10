# Stage 45 — Reusable materials and texture budget

This stage defines a small shared PBR starting library for the modern police HQ and validates optional external texture references.

## Files
- `generate_stage45_material_manifest.py`: emits `build/stage45_material_manifest.json` with 14 shared surface profiles.
- `audit_stage45_material_assets.py`: checks populated `texture_set` paths relative to the project root, prevents path traversal, checks extension and size, and reports intentional texture reuse.
- `build_stage45_materials_blender.py`: optional Blender-side review importer. Run with Blender's Python, not ordinary system Python.

## Optimization choices
- Reuse a small material vocabulary rather than assigning a unique material to every prop.
- Share texture groups and prefer atlases for repeated small details.
- Keep texture sizes conservative; only increase after visual inspection and profiling.
- Keep glass, metal, wet-room tile and safety markings distinct where their surface response matters.

## Run
```bash
python stage45/generate_stage45_material_manifest.py --output build/stage45_material_manifest.json
python stage45/audit_stage45_material_assets.py build/stage45_material_manifest.json --project-root .
```

No textures are bundled by this stage; an empty texture_set means no external file is expected yet. Blender importer creates review materials only. GTA shader mapping, UVs, texture baking, Sollumz conversion, CodeWalker validation and in-game performance tests remain required. This stage is not production-ready.
