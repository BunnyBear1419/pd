# Stage 7 — Rebrandable Agency Signage

This stage separates the building's identity from its architecture. Run the script in the same Blender scene after Stage 2, ideally after Stages 3 and 4.

## Change the agency

Open `generate_stage7_branding.py` and edit the `BRAND` dictionary near the top:

- `agency_name`: full name used on the exterior sign
- `short_name`: abbreviation used on the exterior and lobby plaque
- `subtitle`: lobby plaque subtitle
- `primary_color`, `accent_color`, `text_color`: RGBA material colors
- `show_subtitle`: whether to create the lobby plaque

Examples:
- Police: `LOS SANTOS POLICE DEPARTMENT` / `LSPD`
- Federal: `FEDERAL INVESTIGATION BUREAU` / `FIB`
- Sheriff: `LOS SANTOS COUNTY SHERIFF` / `LSCSO`
- Security: `PRIVATE SECURITY` / `SECURITY`

The script creates editable Blender text and simple backing meshes in the `PDHQ_BRANDING_SIGNS` collection. Rerunning it clears and rebuilds only objects in that collection; it does not clear the building or other scene collections.

## Important limitations

This is a convenient blockout branding system, not a full customization interface and not final game-ready signage. Long agency names may need a smaller font or wider sign. Review sign placement in Blender, replace text with approved vector/logo artwork where desired, UV-map and texture final meshes, and validate the exported asset in-game. Branding changes do not automatically change room names, uniforms, job scripts, map labels, or server logic.
