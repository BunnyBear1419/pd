# Stage 4 — Furniture, equipment and security blockout

## Run order
1. Open Blender and run `stage2/generate_stage2_blockout.py`.
2. In the same scene, run `stage3/generate_stage3_interior.py`.
3. In the same scene, run `stage4/generate_stage4_furnishing.py`.

Stage 4 adds schematic, metre-scale proxy geometry for reception and booking desks, holding benches, secure cabinets, garage clearance envelopes, dispatch consoles, evidence/armory storage, SWAT briefing furniture, detective desks, interview tables, and conference furniture.

## Important limitations
- This is layout-review geometry, not finished furniture assets.
- Yellow garage volumes are **clearance guides**, not vehicles or final collision.
- No final door leaves, working hinges, cell bars, materials/UVs, LODs, game collision, occlusion, portals, archetypes, or Sollumz export are generated.
- Stage 2 currently includes generic room zoning and Stage 3 replaces that collection with a more detailed schematic. Check room circulation and possible overlaps in Blender before treating dimensions as approved.
- A real FiveM MLO still requires Blender plus compatible Sollumz/GTA asset preparation and in-game testing.

## Review checklist
- Check that each furniture group is in the intended room and on the correct floor.
- Verify corridor widths, accessible routes, door clearances and stair landings.
- Confirm garage bay envelope dimensions against the largest intended vehicle.
- Ensure evidence and armory storage are in access-controlled rooms.
- Replace all proxy geometry with optimized assets; build collision and LODs intentionally.
