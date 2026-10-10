# Stage 31 — Optimization and export manifest checklist

## Preserve the source
- [ ] Save a versioned copy of the generated Blender project before making changes.
- [ ] Run the Stage 31 inventory and retain both report text blocks.
- [ ] Review the complete object manifest; approve export disposition for every object.
- [ ] Confirm important rooms, stairs, elevator openings, doors, roof access, garage and helipad remain represented.

## Reduce avoidable cost
- [ ] Inspect high-polygon objects for hidden/internal faces and unnecessary bevel subdivisions.
- [ ] Share compatible materials where this does not compromise the intended appearance.
- [ ] Review modifier stacks and non-unit transforms before applying or removing anything.
- [ ] Check repeated props for reusable mesh data/instancing where supported by the target export pipeline.
- [ ] Separate visible render geometry, collision geometry and temporary review guides according to the current Sollumz workflow.
- [ ] Create LODs only where useful and verify silhouette, pop-in and material behavior at distance.
- [ ] Avoid blind decimation, automatic joining, or name-only guide deletion.

## Export preparation
- [ ] Decide each object's inclusion/exclusion manually and document the reason.
- [ ] Confirm object origins, naming, materials, UVs, normals, scale, collision roles and bounds.
- [ ] Export a small representative test batch through compatible Sollumz tools.
- [ ] Inspect the test batch in CodeWalker and resolve export warnings before scaling up.
- [ ] Build and validate the complete resource with Stage 23 against the actual exported folder.
- [ ] Test fresh join, respawn, reconnect, resource restart, multiple clients, textures, collisions, streaming and viewing distances in FiveM.
- [ ] Record real resource size and in-game performance; Blender polygon counts alone are not proof of optimization.

**Acceptance rule:** Stage 31 is complete when the manifest has been manually reviewed and the actual exported/tested asset demonstrates acceptable visuals and measured runtime behavior. Script completion alone is not an optimization pass.
