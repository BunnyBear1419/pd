# Stage 2 — Optimized Police HQ Blockout

This folder contains the first procedural 3D blockout for the custom FiveM police station.

## Generate the Blender scene

1. Install Blender (3.x or 4.x recommended).
2. Open Blender and switch to **Scripting**.
3. Open `generate_stage2_blockout.py`.
4. Click **Run Script**.
5. Save the resulting scene as `pd_hq_stage2_blockout.blend`.

The script creates a roughly 54 m × 38 m, three-storey building with a roof deck, helipad markings, HVAC placeholders, entrance canopy, site apron, room-zone guide empties, and simplified collision proxy objects.

## Collections

- `PDHQ_STRUCTURE` — slabs, perimeter walls, roof deck, parapets.
- `PDHQ_INTERIOR_ZONES` — conceptual partitions and circulation placeholders.
- `PDHQ_ROOF_EQUIPMENT` — helipad and HVAC blockout.
- `PDHQ_EXTERIOR_ASSETS` — site apron, façade glazing, canopy.
- `PDHQ_COLLISION_PROXIES` — coarse proxy volumes for later replacement.
- `PDHQ_GUIDES` — zone markers, camera and lighting.

## Important limits

This is a **blockout**, not a finished or install-ready FiveM MLO. The room partitions are deliberately schematic. The collision proxies are not production collision meshes. The building still requires reviewed floor plans, real door openings, stairs and landings, accessible circulation, room-specific geometry, UVs/materials, lighting, portals/occlusion planning where appropriate, and export/testing with the Sollumz and CodeWalker toolchain.

Do not put this scene directly on a live server as an MLO. Use a dedicated test server after the asset pipeline and resource manifest are complete.
