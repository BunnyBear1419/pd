# Stage 10 — Exterior Architectural Detail Pass

Adds a modest, low-complexity set of editable exterior details in a dedicated collection.

## Files
- `generate_stage10_architectural_details.py` — Blender generator.
- `ARCHITECTURAL_DETAIL_CHECKLIST.md` — inspection and optimization checklist.

## Run
1. Open the Blender scene after generating Stage 2.
2. Run this script in the same scene.
3. Inspect the `PDHQ_ARCHITECTURAL_DETAILS` collection.
4. Re-run safely after edits; the script clears only its own collection.

## What it adds
- Vertical façade fins
- Front glazing mullions, heads, and sills
- Thin floor bands and accent strips
- Entrance canopy fascia and underside panel
- Front base plinth and corner caps

## Important
This is a coordinate-based blockout detail pass. Inspect for overlaps with the Stage 7 branding, Stage 8 signs, Stage 9 emblem, glazing, and canopy. The script does not create final collision, UVs, LODs, portals, occlusion, or Sollumz metadata. Run the scene audit and validate the actual export and in-game resource before release.
