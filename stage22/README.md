# Stage 22 — Interior visibility and streaming preparation

Stage 22 provides a non-destructive inventory to help organize the next MLO visibility and streaming review.

## Files

- `audit_stage22_visibility_streaming.py` — run in Blender with the current HQ scene active.
- `VISIBILITY_STREAMING_AND_MLO_CHECKLIST.md` — manual visibility, map integration, and FiveM test plan.

## Run it

1. Save a versioned backup of the `.blend` file.
2. Open the script in Blender's Scripting workspace and run it.
3. Review the `PDHQ_STAGE22_VISIBILITY_STREAMING_REPORT` text block.
4. Use its candidate lists to guide manual review; names and collections are only hints.

## Critical limitation

This script does not create GTA MLO archetypes, portals, occlusion, collision, LODs, texture dictionaries, or resource configuration. Those require the compatible Sollumz/CodeWalker workflow and in-game validation. Do not infer that a space is correctly streamed simply because it appears in the Blender scene.
