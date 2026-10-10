# Stage 9 — Rebrandable Agency Emblem Kit

Creates an editable exterior shield crest and a smaller lobby badge from simple mesh geometry and Blender text.

## Files
- generate_stage9_emblems.py — Blender Python generator.
- EMBLEM_AND_BRANDING_GUIDE.md — configuration, placement, and export notes.

## Configure
Edit the BRAND dictionary in the generator:
- agency_name — full agency label
- short_name — initials displayed in the crest
- subtitle — optional motto
- primary_color, accent_color, text_color — RGBA material colors
- show_subtitle — whether the motto appears

Edit EMBLEM_LAYOUT to move the exterior and lobby anchors or change their scale. Keep the Stage 7 and Stage 8 BRAND values synchronized manually.

## Run
1. Open the working Blender scene with Stages 2–8 generated.
2. Open this script in Blender's Text Editor and edit BRAND and EMBLEM_LAYOUT.
3. Run the script and inspect the PDHQ_AGENCY_EMBLEMS collection.
4. Re-run safely after changes; only that collection is replaced.

## Limitations
These are generic, procedural placeholder crests, not official logos or final production assets. Long agency names may need smaller text or a wider plaque. The supplied anchors are approximate and may intersect the façade or interior wall. Inspect in Blender; then perform the Sollumz/GTA export, collision, material, LOD, streaming, and in-game validation separately. This stage changes visuals only, not FiveM jobs, permissions, uniforms, scripts, or map labels.
