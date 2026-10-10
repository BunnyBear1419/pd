# Stage 39 — Room adjacency and circulation reconciliation

## Purpose
Compare the schematic placements with intended room adjacencies and reserve a continuous public/staff/secure circulation strategy. Do not automatically move rooms without human review.

## Inputs
- Approved Stage 36 room program and adjacency schedule.
- Stage 37 fit-screen JSON and Stage 38 SVG previews.
- The current Blender scene, reviewed and saved as a versioned copy.

## Work sequence
1. Review the current scene and record a baseline before editing.
2. Make a small, reversible change set; preserve backups.
3. Run relevant earlier audits and inspect the result visually.
4. Record unresolved issues instead of silently accepting a heuristic pass.
5. Do not export placeholders as production GTA assets.

## Acceptance criteria
- [ ] Review every Stage 36 adjacency pair in the proposed plan
- [ ] identify adjacency mismatches
- [ ] confirm circulation is continuous
- [ ] keep public, detainee, staff and vehicle paths separated
- [ ] document all exceptions

## Status boundary
This stage is a production work package and acceptance gate. Repository presence or CI success does not mean the Blender/Sollumz/CodeWalker/FiveM work has been performed. Do not mark complete until the required external evidence exists.
