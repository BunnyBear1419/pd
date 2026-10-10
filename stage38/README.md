# Stage 38 — Visual floor-plan previews

Run from the repository root:

```bash
python stage38/generate_stage38_floorplan_preview.py --output-dir build/stage38-floorplans
```

This runs the Stage 37 rectangle-fit screen, then emits an HTML review index, three floor SVGs, a roof/helipad SVG and a JSON summary. It uses only the Python standard library.

**Important:** these are schematic rectangle-packing visualizations, not construction drawings and not a finished Blender model. They do not solve adjacency, doors, walls, egress, accessibility, structure, utilities, aircraft requirements or game asset validity. A failed fit screen still produces previews to help expose the problem.

Review the SVGs in a browser before using any coordinates to alter Blender geometry.
