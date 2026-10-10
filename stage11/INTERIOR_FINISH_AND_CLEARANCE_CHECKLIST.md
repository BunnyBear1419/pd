# Stage 11 Interior Finish and Clearance Checklist

## Blender review
- [ ] Generate Stages 2–4 before running Stage 11.
- [ ] Confirm the lobby feature wall sits on the intended solid wall segment and does not obscure entrance glazing.
- [ ] Check the welcome and dispatch labels face the room and remain legible.
- [ ] Inspect corridor skirting against the corridor partitions and every door opening.
- [ ] Verify evidence and armory markers match the intended room locations.
- [ ] Check detective panels against the rear wall, ceiling, and furnishings.
- [ ] Confirm stair-core protection strips do not intrude into stair circulation.
- [ ] Hide the detail collection to compare the base scene with the added finish pass.

## Optimization and export
- [ ] Keep the collection separate until the layout is approved.
- [ ] Review object count, material slots, normals, and modifier costs.
- [ ] Merge repeated static details only if it helps the chosen export pipeline.
- [ ] Decide which items need collision; do not give every decorative strip collision by default.
- [ ] Review LOD/draw-distance, portal, and occlusion strategy in the actual Sollumz/CodeWalker workflow.

## Release gate
Python syntax and packaging checks do not prove Blender execution or in-game correctness. Test the exported resource in FiveM with multiple viewing distances and typical player movement before release.
