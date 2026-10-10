# Stage 16 — Structural and Circulation Audit

Stage 16 adds a non-destructive Blender audit for floor levels, slab dimensions, expected structural objects, stair placeholders, and vertical-penetration review items.

## Run it
1. Open the working Blender file containing Stage 2 and Stage 3 output.
2. Run stage16/audit_stage16_structure.py from Blender's Scripting workspace.
3. Read the console output or open the generated PDHQ_STAGE16_STRUCTURAL_AUDIT text block in Blender's Text Editor.
4. Resolve findings in the scene, save a new version, and rerun the audit.

## Important limits
The audit does not move, delete, boolean-cut, or repair objects. Findings are heuristic and name-based. It cannot reliably determine whether arbitrary meshes intersect, whether a door is passable, or whether stairs meet building-code requirements. A review flag is a prompt for inspection, not proof of a defect.

The Stage 2 blockout uses broad slab plates and stair/elevator placeholders. Check actual slab openings and clearances manually in section view before finalizing the structure. Save a versioned Blender file before substantial geometry changes.

## Review scope
- Floor slab presence, dimensions, and approximate elevations.
- Roof deck presence.
- Stair-core placeholders and stair-step/landing counts.
- Door/frame naming presence.
- Reminders to review stairwell/elevator penetrations and slab cuts.

Passing this audit does not mean the MLO is complete or optimized. Manual Blender inspection, production collision/materials, Sollumz setup, CodeWalker review, export, and FiveM testing are still required.
