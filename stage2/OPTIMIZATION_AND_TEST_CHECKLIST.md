# Optimization and Testing Checklist

## Blender scene hygiene
- [ ] Keep the named collections separate through blockout and detailing.
- [ ] Apply object transforms before final export.
- [ ] Use instancing or linked duplicates for repeated fixtures where practical.
- [ ] Avoid unnecessary bevel modifiers and high-segment geometry on background props.
- [ ] Use consistent metre-based scale and validate the origin/placement coordinates.
- [ ] Replace zone guide empties and collision placeholders before production export.

## Geometry and materials
- [ ] Add actual door/window openings; do not rely on glass panels to imply openings.
- [ ] Keep large flat surfaces simple and avoid hidden duplicate faces.
- [ ] Create low-complexity collision meshes independent of decorative meshes.
- [ ] Reuse trim sheets/material atlases where appropriate.
- [ ] Use sensible texture dimensions and mipmaps; avoid huge unique textures.
- [ ] Inspect normals, smoothing, UVs, and material assignments.

## MLO and FiveM pipeline
- [ ] Validate assets with the chosen Sollumz and CodeWalker versions.
- [ ] Confirm archetype/interior setup and required portals/rooms for the chosen workflow.
- [ ] Confirm collision, walkable surfaces, stair traversal, doors, and roof access.
- [ ] Confirm all interior assets are streamed and referenced by the resource correctly.
- [ ] Test at the intended map location and check for conflicts with existing map assets.
- [ ] Test from fresh join, relog, different player positions, and after resource restart.
- [ ] Check occlusion/pop-in and verify the exterior shell does not hide the interior.
- [ ] Check garage access, helipad landing area, and emergency egress paths.

## Performance targets to validate (not yet measured)
- [ ] Minimize draw calls through sensible material reuse and mesh organization.
- [ ] Keep collision simple and avoid detailed collision on small decorative objects.
- [ ] Test texture memory and streaming on a representative server/client setup.
- [ ] Inspect frame-time and memory before/after entering the interior.
- [ ] Check network/server logs for resource or asset errors.
- [ ] Record before/after screenshots and a reproducible test route.

## Release gate
Do not label the MLO production-ready until it has been exported through the target asset pipeline and validated in-game. The generated Stage 2 scene is only a starting blockout.
