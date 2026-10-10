# Blender build and acceptance checklist

## Build run

- [ ] Clone the repository and install a compatible Blender release.
- [ ] Run `blender -b --python stage25/build_stage25_scene.py -- --output build/pdhq_stage25_blockout.blend --log build/pdhq_stage25_build_report.json` from the repository root.
- [ ] Confirm the command exits successfully and the JSON report says `BUILD_COMPLETED_REQUIRES_MANUAL_REVIEW`.
- [ ] Open the saved `.blend` in Blender's UI and inspect the scene in perspective and top/orthographic views.
- [ ] Read the audit report text blocks for scene/layout, structural circulation, room circulation, export preflight, LOD/performance, geometry cleanup, and visibility/streaming.

## Geometry review before export

- [ ] Fix floor slabs that block stairs, elevator, ducts, or service openings.
- [ ] Validate stairs, landings, headroom, door widths, and corridor continuity.
- [ ] Verify all departments and furniture are actually inside intended rooms.
- [ ] Verify garage doors, turning envelope, vehicle clearance, pedestrian path, and emergency/service access.
- [ ] Resolve intersecting signs, emblems, facade elements, interior finishes, furniture, and glass.
- [ ] Identify guide/proxy/collision candidates; hide or exclude temporary guides from production export.
- [ ] Review normals, topology, scale, materials, UVs, object origins, and collision geometry.

## Export and runtime acceptance

- [ ] Prepare GTA asset types and MLO metadata using compatible Sollumz tools.
- [ ] Build room/portal/occlusion and collision setup using the actual supported export workflow.
- [ ] Export and inspect assets in CodeWalker; fix warnings and missing dependencies.
- [ ] Assemble a resource with the correct `fxmanifest.lua`, `stream/` assets, and any required YTYP registration.
- [ ] Run `python stage23/validate_stage23_resource.py <resource-folder>` against the real resource.
- [ ] Test on a development FiveM server: fresh join, spawn/respawn, reconnect, resource restart, multiple clients, textures, collision, visibility, default-building overlap, and representative viewing distances.
- [ ] Record test conditions and observed performance; keep a known-good release for rollback.

## Definition of done

The orchestration script completing successfully is a **successful blockout build only**. Production readiness requires passing manual geometry review, actual Sollumz export, CodeWalker inspection, and FiveM runtime acceptance. No CI result alone can certify those steps.
