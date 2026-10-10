# Stage 36 — Room Program and Adjacency Schedule

Stage 36 turns the facilities brief into a machine-checkable room schedule before detailed modeling. It defines room IDs, target clear dimensions, minimum screening widths for doors, security zones, and adjacency intent.

## Floor concept

- **Ground floor:** public entry and reporting; booking/processing/holding; interviews; evidence intake/vault; armory and patrol support; secure transfer; fleet garage.
- **Level 2:** dispatch, incident operations, command, detectives, confidential interview, briefing/conference, IT/radio, staff support.
- **Level 3:** SWAT briefing and gear, locker rooms/showers, fitness/rest support, tactical command, controlled roof access.
- **Roof:** helipad planning envelope and marked safety buffer.

## Run the schedule audit

From repository root:

```bash
python stage36/audit_stage36_room_program.py
```

The audit uses only the Python standard library. It checks unique IDs, positive dimensions, screening door widths, valid floor labels, adjacency references, required facility coverage, and whether the sum of scheduled net room areas looks implausibly large relative to the 54 × 38 m reference footprint.

## Important limitations

This is a **design brief**, not a remodeled Blender scene. Room dimensions are preliminary net-clear targets; they do not prove the current schematic fits. The auditor does not check actual room polygons, wall thickness, door swing conflicts, accessibility, fire/life safety, secure circulation, structural loads, aircraft/helipad regulations, or local building code. Reconcile this schedule against the model before detailed assets and GTA export. Helipad geometry and operational requirements must be reviewed by qualified specialists.
