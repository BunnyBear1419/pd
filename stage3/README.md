# Stage 3 — Interior Layout Pass

1. Open Blender.
2. Run `stage2/generate_stage2_blockout.py` to create the shell.
3. Without clearing the scene, run `stage3/generate_stage3_interior.py`.
4. Inspect the `PDHQ_INTERIOR_ZONES` collection and the named zone guides.
5. Save a new file such as `pd_hq_stage3_interior_pass.blend` so the Stage 2 blockout remains available.

Stage 3 replaces the schematic interior collection with partition geometry that includes door gaps and frame/lintel placeholders, and adds stepped stair blockouts. It does not yet create production doors, finished cell modules, final collision, portals, textures, or a FiveM resource ready for release.

See `ROOM_LAYOUT_AND_DOOR_SCHEDULE.md` for the planning dimensions and acceptance checklist.
