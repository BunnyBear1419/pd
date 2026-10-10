# Visibility, streaming, and MLO checklist

## Scene inventory

- [ ] Save a backup `.blend` and run `audit_stage22_visibility_streaming.py`.
- [ ] Review likely temporary guides and proxies individually; decide which must be excluded from final exports.
- [ ] Confirm object/collection names, origins, transforms, bounds, and material/texture assignments are consistent.
- [ ] Identify the intended MLO boundary and map placement before preparing GTA-specific visibility data.

## Visibility design

- [ ] Review every entrance, door, window, corridor junction, stairwell, elevator shaft, garage opening, and roof access.
- [ ] Decide which rooms and surfaces should be visible from each transition and which geometry should occlude them.
- [ ] Confirm there are no accidental gaps that expose the void or unrelated parts of the map.
- [ ] Confirm the exterior facade, lobby glazing, internal walls, and floor slabs do not unintentionally hide required spaces.
- [ ] Do not create portals or occlusion from the report alone; author them with the current supported Sollumz workflow and inspect in CodeWalker.

## GTA/FiveM integration

- [ ] Confirm intended map coordinates and ensure the custom site does not conflict with the base-game building or another streamed map.
- [ ] Verify correct MLO/archetype setup, bounds, room/portal data, occlusion strategy, collision, and LOD assignments as separate checks.
- [ ] Verify texture dictionaries, material/shader setup, paths, asset names, and resource manifest/stream folder.
- [ ] Test default-building overlap deliberately: establish whether a map replacement, hide/remove setup, or different placement is required for the selected location.
- [ ] Test fresh join, spawn/respawn, interior entry and exit, reconnect, and changing camera angles.
- [ ] Test with the full server resource set enabled and ask a second client to verify visibility independently.
- [ ] Check for missing textures, invisible walls, black materials, flickering/z-fighting, disappearing interiors, and unexpected base-game geometry.

## Acceptance criteria

- [ ] Every required room is visible from intended approach paths and occluded where intended.
- [ ] Interior visibility is stable across join, respawn, and reconnect.
- [ ] No unexpected default building overlaps the custom HQ.
- [ ] No missing textures/materials and no critical collision or streaming warnings remain.
- [ ] Keep a known-good build and compare changes one at a time.

The Blender audit is a planning aid only. Acceptance requires exported asset inspection and real FiveM tests.
