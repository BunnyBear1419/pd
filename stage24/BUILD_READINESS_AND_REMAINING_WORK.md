# Build readiness and remaining work

## Repository-level checks

- [ ] Confirm all stage directories and expected source files are present, including the Stage 29 room-clearance audit.
- [ ] Confirm the packaging workflow includes every current stage and its required source files.
- [ ] Run the Stage 24 audit from the repository root and review its JSON report.
- [ ] Keep the successful GitHub Actions package as a source/documentation bundle, not as a claim of a finished MLO.

## Blender scene gate

- [ ] Open the project in a compatible Blender version and save a versioned `.blend` file.
- [ ] Run generators in documented order on a backup and inspect the resulting scene after each major pass.
- [ ] Resolve architectural issues: full-footprint slabs, stair/elevator openings, stair continuity, room access, doors, room dimensions, furniture clearances, and roof/helipad circulation.
- [ ] Inspect the provisional garage entry, vehicle turning/clearance, secure transfer, room dimensions and door/furniture clearance, pedestrian separation, emergency lane, and service approach.
- [ ] Confirm branding, signs, glazing, facade details, interior details, and furniture do not intersect or z-fight.
- [ ] Decide which guide, placeholder, clearance, and audit objects are excluded from production export.
- [ ] Review topology, normals, materials, UVs, object origins, transforms, collision candidates, and LOD priorities.

## GTA asset/export gate

- [ ] Use a compatible Sollumz version to prepare actual GTA asset types, archetypes, collision, and relevant MLO metadata.
- [ ] Author and inspect room/portal/occlusion setup using the supported tool workflow; do not treat Blender collections as MLO visibility data.
- [ ] Export the actual assets and inspect the result in CodeWalker.
- [ ] Build a real resource folder with correct `fxmanifest.lua`, `stream/` contents, exact paths, and required YTYP registration.
- [ ] Run Stage 23's resource validator on the exported resource folder and resolve issues/warnings.

## FiveM acceptance gate

- [ ] Install the resource on a development server and inspect startup/client logs.
- [ ] Confirm intended map placement and no unexpected default GTA building overlap.
- [ ] Test collision, player movement, stairs, doors, booking/cells, garage vehicle entry/exit, roof access, and helipad access.
- [ ] Test textures, visibility, portals/occlusion, LOD transitions, and streaming from near/medium/far distances.
- [ ] Test fresh join, spawn/respawn, reconnect, resource restart, and multiple clients with the full server resource set.
- [ ] Compare performance before/after optimization on the target server; record the actual test conditions and results.
- [ ] Keep a known-good export and version each tested release.

## Honest status

The repository currently contains staged generators, audit scripts, checklists, and packaging automation. CI syntax/package success is useful but is not Blender scene validation. Until a real `.blend` scene is generated and inspected, assets are exported through Sollumz and reviewed in CodeWalker, and the resource is tested in FiveM, the MLO must be treated as **in development, not production-ready**.
