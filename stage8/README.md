# Stage 8 — Wayfinding and Department Signage

Adds a separate, rerunnable signage collection for room plaques, garage signs, and floor-directory panels.

## Files
- `generate_stage8_wayfinding.py` — Blender Python generator.
- `WAYFINDING_SIGNAGE_PLAN.md` — label and placement guide.

## Use
1. Open the working Blender scene containing Stages 2–7.
2. Open `generate_stage8_wayfinding.py` in Blender's Text Editor.
3. Edit `BRAND` to match the Stage 7 agency identity.
4. Adjust the `SIGN_LAYOUT` coordinates and rotations to match the actual walls/doors in your scene.
5. Run the script and inspect the `PDHQ_WAYFINDING_SIGNS` collection.
6. Re-run after edits; it only replaces objects inside that dedicated collection.

## Important limitations
- The supplied coordinates are blockout placeholders, not surveyed placements. Some signs may overlap doors, walls, furniture, or each other until adjusted in Blender.
- Text and simple backing meshes are editable proxies, not final UV-mapped decals, emblems, emissive signage, or optimized GTA assets.
- This is visual rebranding only. It does not change FiveM job permissions, uniforms, scripts, map blips, or role names.
- Before release, inspect font sizing, visibility, collision, materials, draw distance, and performance in Blender/Sollumz and in-game.
