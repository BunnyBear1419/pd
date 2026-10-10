# Stage 47 — LOD and geometry budget

## Purpose
Create an evidence-based geometry budget and identify LOD candidates rather than relying on object count alone.

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
- [ ] Review high-poly objects
- [ ] create appropriate LOD strategy where supported
- [ ] remove hidden/internal faces when safe
- [ ] verify silhouettes at distance
- [ ] compare measured frame time and memory

## Status boundary
This stage is a production work package and acceptance gate. Repository presence or CI success does not mean the Blender/Sollumz/CodeWalker/FiveM work has been performed. Do not mark complete until the required external evidence exists.
