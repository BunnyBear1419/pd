# Stage 31 — Optimization review and export manifest

Stage 31 adds a non-destructive optimization inventory and suggested export manifest for the active Blender scene.

## Run

After the Stage 25 build has completed, run this file in Blender's Scripting workspace:

    exec(compile(open("stage31/audit_stage31_optimization_export_manifest.py", encoding="utf-8").read(), "stage31/audit_stage31_optimization_export_manifest.py", "exec"))

Read the PDHQ_STAGE31_OPTIMIZATION_EXPORT_REPORT text block for the JSON report and PDHQ_STAGE31_EXPORT_MANIFEST_CSV for a spreadsheet-friendly inventory. To save the CSV outside Blender, open that text block and use Blender's text-editor save option.

## Scope

- Per-object type, collection, bounds, dimensions, polygon/vertex counts, materials, modifiers and scale.
- Collection-level mesh/polygon summaries.
- Suggested review dispositions for guide/proxy objects, collision candidates, render meshes and non-mesh dependencies.
- High-polygon, non-unit-scale, modifier and missing-material review lists.

## Important limitations

This is an inventory and decision aid, not an automatic optimizer. It does not decimate meshes, merge objects, delete internal faces, hide guides, apply modifiers, generate LODs/collision, or export GTA assets. Suggested dispositions must be verified against the actual scene. Real optimization is only established after export inspection and measured FiveM tests.
