# Stage 37 — Coordinate-Based Floor Fit Screening

Stage 37 takes the Stage 36 room schedule and proposes preliminary XY rectangles for the three occupied floors. It packs the larger rooms first, permits 90-degree rotation, maintains a 0.5 m nominal perimeter margin, and reserves a 2.4 m central circulation spine.

## Run it

```bash
python stage37/audit_stage37_floor_fit.py
python stage37/audit_stage37_floor_fit.py --output build/stage37_proposed_floor_plan.json
```

A nonzero exit code means one or more rooms could not be packed or an overlap was found. The output is deterministic JSON and includes coordinates, orientation, unplaced rooms, overlap checks, and limitations.

## Interpretation

- Coordinates are in metres relative to the building footprint center.
- The public/front side remains at negative Y.
- The central spine is reserved between X = -1.2 m and X = +1.2 m.
- Room rectangles are net-area targets only. They do not generate walls or doors and do not guarantee that listed adjacency pairs physically touch.
- The rooftop helipad envelope is checked against the nominal footprint, not certified for aviation use.

This is a coarse fit test, not a finished architectural plan. The next modeling pass must reconcile room coordinates with wall thickness, stairs/elevator, doors and swings, accessible routes, structural grid, furniture, secure circulation, and the existing Blender scene.
