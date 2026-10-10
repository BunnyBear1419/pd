# Stage 6 — Layout validation pass

Run Stages 2, 3 and 4 in the same Blender scene, then run `stage6/validate_stage6_layout.py`. The script does not modify the scene. It writes a report to the Text Editor datablock `PDHQ_STAGE6_LAYOUT_REPORT` and prints it to the console.

It checks expected collections and anchor names, counts selected furnishing groups, and performs a deliberately coarse axis-aligned bounding-box intersection check between garage clearance guide volumes and selected counters/desks/consoles.

## Limitations
- This is a heuristic review aid, not a geometric proof or automatic certification.
- It does not check every mesh pair, wall intersections, navigation, door swings, accessibility, collision, or GTA/FiveM metadata.
- Bounding boxes can report false positives and miss real conflicts.
- Visual inspection and in-game testing remain required.
