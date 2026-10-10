# Stage 17 — Room and Circulation Checklist

## Public and staff circulation
- [ ] Public entrance connects to reception without crossing secure areas.
- [ ] Booking, holding, and staff-only paths are logically separated.
- [ ] Dispatch, evidence, and armory access routes are clear and controlled.
- [ ] Detective offices, interview rooms, briefing, and locker facilities are reachable without blocked doors.
- [ ] Corridor widths are checked at the narrowest points, including furniture and door swings.
- [ ] Accessible route and emergency egress are manually reviewed.

## Fixtures and room boundaries
- [ ] Run `audit_stage17_room_circulation.py` after Stages 2–4.
- [ ] Inspect each reported fixture-overlap candidate in Blender.
- [ ] Confirm counters, desks, cabinets, lockers, tables, and vehicle-clearance guides are in the intended rooms.
- [ ] Check furniture does not cross partition walls or block door openings.
- [ ] Confirm garage vehicle envelopes and turning aisle do not intersect desks, partitions, or pedestrian routes.
- [ ] Check door leaf/frame dimensions against Stage 3 openings.

## Before progressing
- [ ] Save a versioned Blender file before geometry corrections.
- [ ] Re-run Stage 6, Stage 16, and Stage 17 reports after edits.
- [ ] Verify actual geometry, not just object names or bounding boxes.
- [ ] Do not claim accessibility, collision correctness, optimization, or MLO readiness until tested in the target game.
