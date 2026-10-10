# Stage 39 — Room adjacency and circulation reconciliation

## Purpose
Compare intended Stage 36 room adjacencies with Stage 37 schematic room placements and produce a review report. The audit does not automatically move rooms.

## Run
```bash
python stage39/audit_stage39_adjacency.py --output build/stage39_adjacency_report.json
```

The report categorizes pairs as shared-edge candidates, near-but-not-adjacent, not adjacent in the packing, unplaced, cross-floor review, or invalid references. Geometric closeness is not proof of a door, usable route, security separation or code compliance.

## Workflow
1. Review the generated Stage 38 SVG previews and Stage 39 JSON report.
2. Decide which adjacency mismatches require room-program or placement changes.
3. Update coordinates only after human review; preserve a backup.
4. Verify actual wall openings, door swings, corridor connections, vertical circulation and secure route separation in Blender.

## Status boundary
This is a deterministic advisory audit, not an architectural or life-safety certification. Repository presence and CI success do not mean the Blender/Sollumz/CodeWalker/FiveM work is complete.
