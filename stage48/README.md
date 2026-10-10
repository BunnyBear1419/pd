# Stage 48 — Integrated pre-export review

Stage 48 ties the Stage 42–47 planning outputs together and creates a machine-readable pre-export report.

## Generate the report
```bash
python stage48/audit_stage48_pre_export.py --root . --output build/stage48_pre_export_report.json
```

The report checks that each expected JSON manifest exists, has the expected stage marker, remains explicitly not production-ready, and contains its expected collection/count field. Missing or malformed inputs are listed as blockers.

## What this does not do
It does not combine geometry inside Blender, create GTA MLO archetypes or portals, convert materials to GTA shaders, generate collision, or export a resource. Those tasks require the real Blender/Sollumz/CodeWalker workflow and then in-game FiveM validation.

## Human acceptance checklist
- [ ] Inspect the saved Blender scene, collections and transforms.
- [ ] Review actual mesh UVs, materials, collision and LODs.
- [ ] Verify doorways, stairs, garage turning/entry clearance, roof and helipad access.
- [ ] Export and inspect actual assets in CodeWalker.
- [ ] Test visibility/streaming on join, spawn, respawn, reconnect, resource restart and multiple clients.
- [ ] Record performance measurements, defects, tool versions, reviewer and rollback instructions.

**Status boundary:** report generation and CI success validate the planning package only. Stage 48 remains not production-ready until external evidence is reviewed.
