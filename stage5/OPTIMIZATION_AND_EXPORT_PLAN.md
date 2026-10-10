# Stage 5 — Optimization and export-readiness plan

## Target approach
Treat optimization as a budget and validation process, not a single polygon-count trick. Keep high-detail visual meshes separate from collision; use simple collision volumes; avoid unnecessary material slots; reuse shared materials; use sensible LODs where applicable; and keep props, guides, and non-export objects in dedicated collections.

## Audit pass
The included Blender script records:
- total scene objects, mesh objects, and estimated triangles;
- object counts by collection;
- non-unit object scale;
- unusually large meshes and meshes above a review threshold;
- mesh objects without materials or without the project naming prefix.

Warnings are prompts for human review, not automatic defects.

## Manual pre-export checklist
- [ ] Remove duplicate/overlapping wall geometry after Stage 2/3 reconciliation.
- [ ] Verify all doors and corridors connect; confirm stair rise, run, landings and headroom.
- [ ] Confirm garage clearance with the largest intended vehicle and pedestrian paths.
- [ ] Separate render geometry, collision geometry, guides, cameras, lights and staging objects.
- [ ] Build low-complexity collision with walkable floors and no accidental invisible blockers.
- [ ] Set consistent origins, applied transforms, names and collection ownership.
- [ ] Review normals, UVs, texture sizes, material count, LOD strategy and interior visibility.
- [ ] Prepare the actual Sollumz archetype/interior metadata, portals, room flags and occlusion as required.
- [ ] Export with a compatible Sollumz/GTA workflow and inspect exporter warnings.
- [ ] Test in a local FiveM server for collision, occlusion, texture streaming, visibility and performance.

## Not yet verified
The blockout scripts have not been validated by opening Blender or loading an export in FiveM. Passing Python syntax checks does not prove geometry correctness or in-game readiness.
