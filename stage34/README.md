# Stage 34 — Architecture & Geometry Review

Stage 34 adds a **non-destructive Blender-side review** to help identify architectural geometry that deserves human inspection before detailed modeling and GTA export.

## Run

From the repository root with Blender installed:

```powershell
blender -b build/pdhq_stage31_blockout.blend --python stage34/audit_stage34_architecture_geometry.py
```

The report is stored as the Blender Text datablock `PDHQ_STAGE34_ARCHITECTURE_GEOMETRY_REPORT`. Open the scene in Blender and inspect that datablock in the Text Editor. To make the report available outside Blender, save the .blend after running the audit, or adapt a local runner to write the text datablock to a JSON file.

The Stage 25 orchestrator also runs this audit as its final review step when audits are enabled.

## What it reviews

- Scene and mesh counts plus polygon totals by collection.
- World-space dimensions that are zero/nearly zero or unusually large.
- Naming hints for walls, slabs, stairs, elevators, helipad, and garage objects.
- Large axis-aligned bounding-box (AABB) overlap candidates among likely structural objects.

## Important limitations

This is a screening tool, not an architectural, structural, accessibility, fire-code, collision, or MLO certification. AABB overlap does not equal exact mesh intersection: wall/slab contacts can be intentional and can be reported. Name matches do not establish that a room or facility is properly built. The script never edits or deletes scene content.

Review every candidate in Blender. Check actual dimensions, stair/elevator openings across floors, door swing/clearance, garage vehicle circulation, secure/public separation, roof access, and helipad approach/obstructions. Continue with Sollumz authoring, CodeWalker inspection, resource validation, and multi-client FiveM tests before considering the MLO complete.
