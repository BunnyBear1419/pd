# Stage 17 — Room Layout and Circulation Review

Stage 17 adds a non-destructive report that checks expected floor and furnishing anchors, counts major furniture categories, and flags possible overlaps between major fixtures using world-axis-aligned bounding boxes.

## Run
1. Open the Blender scene after running Stages 2, 3, and 4.
2. Run `stage17/audit_stage17_room_circulation.py` from the Scripting workspace.
3. Read the console output or the `PDHQ_STAGE17_ROOM_CIRCULATION_REPORT` text block.
4. Inspect each reported candidate in Blender before making any edits.

## Limits
The script never edits geometry. Bounding-box overlaps are candidates, not proof of mesh intersections; objects that intentionally touch can trigger findings. Conversely, the absence of findings does not prove a room is accessible or that the MLO is ready. Door widths, swing clearances, egress, security separation, accessible paths, room membership, and actual walking/vehicle collision all require visual/manual validation and eventual in-game testing.

Save a versioned `.blend` file before changing the scene. The generator uses object names and collection presence as lightweight checks; if naming conventions change, update the script accordingly.
