# Stage 18 — Reusable materials and surface planning

## Goal
Create a compact, shared Blender material library for the police HQ blockout so surfaces can be reviewed consistently before production texturing and Sollumz export.

## Run
1. Open the working .blend file containing Stages 2–17.
2. Open Blender's Scripting workspace and load generate_stage18_materials.py.
3. Run the script.
4. Inspect materials in Material Preview and the Material Properties panel.
5. Review PDHQ_STAGE18_MATERIAL_REPORT in Blender's Text Editor.

## Safe defaults
- AUTO_ASSIGN = False: creates/reuses materials without changing object assignments.
- Set AUTO_ASSIGN = True only after backing up the .blend and reviewing the keyword rules. It assigns a single first material to eligible meshes in collections whose names start with PDHQ_; this is a convenience pass, not a final art pass.
- Rerunning reuses named materials and updates their shader/color settings.

## Materials included
Light/dark concrete, tinted glass, aluminum, black metal, interior wall paint, stone floor, secure-area floor, agency primary/accent, signage backing, yellow planning guides, landscape, and roof membrane.

## Optimization notes
- Reuse shared materials; do not create a unique material for every object.
- Keep material slots limited and remove unused materials after review.
- Avoid relying on transparency for every window in the game build; choose an appropriate GTA shader and Sollumz settings during production conversion.
- Use trim sheets/atlases and tiled materials for final textures where appropriate.
- This script does not generate UVs, texture maps, GTA shaders, collision, LODs, portals, occlusion, or Sollumz drawable metadata.

## Validation status
Python syntax can be checked in CI. Blender material rendering and Sollumz/FiveM behavior still require testing in the actual tools.
