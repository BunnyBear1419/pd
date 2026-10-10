# Stage 29 — Room dimensions, door clearances, and furniture placement

This stage adds a non-destructive Blender audit for door/frame proxy dimensions, likely furniture-to-furniture overlaps, and selected suspiciously small room/partition dimensions. The report is stored in Blender's Text Editor as `PDHQ_STAGE29_ROOM_CLEARANCE_REPORT`.

## Run

Run the Stage 25 build orchestrator from the repository root:

```powershell
blender -b --python stage25/build_stage25_scene.py -- --output build/pdhq_stage29_blockout.blend --log build/pdhq_stage29_build_report.json
```

The orchestrator includes Stage 29 after the Stage 28 garage/secure review. Python CI checks syntax and package structure only; it does not run Blender.

## What to inspect manually

- Check each room's usable inside dimensions, not just the overall wall or mesh bounding box.
- Verify door clear openings between jambs, door swing, handles, thresholds, and approach space.
- Inspect desks, consoles, benches, lockers, cabinets, and interview furniture for collisions and usable circulation.
- Check corridor pinch points, accessible routes, turning areas, stair/elevator landings, and exits.
- Review booking, holding, evidence, armory, dispatch, and other secure areas for separation and controlled access.
- Hide or exclude all temporary guide/proxy objects from production exports.

The thresholds in the script are prompts for review only, not a declaration of legal compliance. Actual requirements depend on the jurisdiction and final building use. Stage 29 neither repairs geometry nor proves the MLO works in FiveM.
