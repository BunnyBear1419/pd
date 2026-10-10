# Stage 30 — Exterior site, emergency access and helipad review

Stage 30 adds a non-destructive Blender audit for the exterior/site plan, access guides, and rooftop helipad surroundings.

## Run

After generating the scene with Stage 25, run in Blender's Python Console or Scripting workspace:

```python
exec(compile(open("stage30/audit_stage30_exterior_helipad_clearance.py", encoding="utf-8").read(), "stage30/audit_stage30_exterior_helipad_clearance.py", "exec"))
```

The report is written to the Blender Text datablock `PDHQ_STAGE30_EXTERIOR_HELIPAD_REPORT` and printed to the console.

## What it checks

- Expected helipad, roof deck, public/accessible approach, emergency lane, gate, garage and service approach objects.
- World-space bounds for important objects.
- Potential plan-view overlap between the helipad platform and HVAC units/bases.
- Presence and object counts of the exterior access and site-security guide collections.

## Important limitations

This is a preliminary inventory and axis-aligned bounding-box screen, not an engineering or regulatory certification. The helipad is only a schematic platform: aviation obstacle surfaces, approach/departure paths, rotor clearance, lighting, structural loading and operational requirements are not modeled. Emergency access, vehicle turning, gates, accessibility, drainage and site boundaries are still provisional. Inspect the scene from top, side and perspective views and resolve conflicts before asset production. No geometry is repaired or exported by this audit.
