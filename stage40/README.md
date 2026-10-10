# Stage 40 — Wall, opening and door coordination

Stage 40 now includes an executable, review-only schedule generator.

```bash
python stage40/generate_stage40_wall_door_schedule.py --output build/stage40_wall_door_schedule.json
```

The script runs the Stage 37 fit screen, then compares the scheduled adjacency pairs against rectangle edges. It emits candidate door openings, perimeter-wall candidates, and explicit review items for unplaced rooms, non-touching adjacency pairs, and cross-floor links.

**Important:** these are schematic candidates, not actual wall geometry, construction drawings, accessibility/code certification, or proof that a door exists. Check the actual Blender scene, wall thickness, swing clearances, secure/public boundaries, and routes manually.

## Stage 40–55 execution boundary

Stages 41–48 define exterior, interior, equipment, lighting, materials, collision, geometry-budget and streaming requirements. Stages 49–55 require the real Blender/Sollumz/CodeWalker/FiveM toolchain and in-game evidence. CI can prepare and audit specifications, but cannot honestly certify those external steps from text files alone.
