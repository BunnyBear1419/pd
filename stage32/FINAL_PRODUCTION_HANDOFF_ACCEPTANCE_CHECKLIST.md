# Final Production Handoff Acceptance Checklist

## Repository and automation
- [ ] Stage 32 report has been generated from the actual checkout.
- [ ] No missing stage/source files are unexplained.
- [ ] Latest GitHub Actions package run completed successfully; review its log and downloadable artifact.
- [ ] Preserve a known-good commit and backup before modifying scene geometry.

## Blender scene — required external work
- [ ] Run `blender -b --python stage25/build_stage25_scene.py -- --output build/pdhq_stage31_blockout.blend --log build/pdhq_stage31_build_report.json` in a compatible Blender installation.
- [ ] Open the saved scene in Blender and inspect every floor, stair/elevator opening, room access, door swing, furniture clearance, garage aisle/turning, service routes, exterior access, roof equipment, and helipad.
- [ ] Review Stage 24–31 findings and the Stage 31 manifest; manually approve guide/proxy disposition.
- [ ] Fix topology, normals, transforms, materials, UVs, intersections, and optimization issues. Keep backups.

## GTA asset pipeline
- [ ] Use a compatible Sollumz workflow to create the actual GTA assets and MLO archetype data.
- [ ] Author and validate collision, portals/room setup, occlusion, and LODs as applicable.
- [ ] Export and inspect in CodeWalker; resolve all errors.
- [ ] Create the actual resource folder, `fxmanifest.lua`, and `stream/` assets; do not ship the template as if it were a finished manifest.
- [ ] Run Stage 23 resource validation on the exported folder.

## FiveM release gate
- [ ] Test map placement and default-building overlap.
- [ ] Test collision, movement, stairs, doors, booking/cells, vehicle entry/exit, roof access, and helipad access.
- [ ] Test visibility/textures/streaming/LOD from multiple distances, fresh join, spawn/respawn, reconnect, and resource restart.
- [ ] Test with multiple clients and the intended server resource stack.
- [ ] Record before/after performance measurements and retain a tested release backup.

## Release decision
Do not label or distribute this as production-ready until all external gates above pass. GitHub CI only checks repository files, Python syntax, and ZIP packaging; it does not run Blender or FiveM.
