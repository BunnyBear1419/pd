# Stage 56 — Integrated Blender review scene

## Purpose
Assemble the Stage 42 shell blockout, Stage 43 furniture/equipment blockout, Stage 44 review lighting, and Stage 45 reusable material profiles into one Blender scene for visual inspection.

## Prerequisites
Run the upstream manifest generators from the repository root first:
- `python stage42/generate_stage42_shell_geometry.py`
- `python stage43/generate_stage43_furniture_blockout.py`
- `python stage44/generate_stage44_lighting_manifest.py`
- `python stage45/generate_stage45_material_manifest.py`

Use the exact inputs/outputs configured by those scripts. If a generator requires additional source manifests, follow that stage's README and resolve its inputs first.

## Build in Blender
From the repository root, with Blender installed and on PATH:

```bash
blender --background --python stage56/build_stage56_review_scene.py -- --output build/pdhq_stage56_review.blend
```

The builder requires these generated files:
- `build/stage42_shell_geometry.json`
- `build/stage43_furniture_blockout.json`
- `build/stage44_lighting_manifest.json`
- `build/stage45_material_manifest.json`

It creates separate review collections for shell, furniture, lights, and camera. It refuses to replace existing review collections or an existing output unless you explicitly choose a fresh collection prefix or pass `--overwrite-output`. Save a copy before experimenting.

## Important limitations
- This creates a **schematic review blockout**, not detailed architecture or a final MLO.
- The layout, wall openings, room furniture and lights require visual review and adjustment.
- It does not create final doors, windows, stairs/elevators, portals, occlusion, collisions, YTYP/archetype definitions, GTA shaders, UVs, or streamed assets.
- Do not include review helpers or placeholder objects in a release resource.
- `production_ready` remains false; the scene must be refined in Blender/Sollumz, exported, checked in CodeWalker, and tested in FiveM with multiple clients.

## CI
CI checks the script's Python syntax and required file presence only. Blender execution is an external validation step because Blender and Sollumz are not guaranteed to exist on the CI runner.
