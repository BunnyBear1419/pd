# Stage 3 — Room Layout and Door Schedule

Stage 3 takes the Stage 2 shell from a massing blockout toward a navigable interior. Dimensions below are planning targets in metres, not code-approved architectural drawings. Validate clearances, access control, emergency egress, and gameplay scale in Blender and in FiveM.

## Coordinate conventions

- Building footprint: 54 m east-west × 38 m north-south.
- Public/front entrance: negative Y.
- Main corridor concept: central east-west spine.
- Floor-to-floor height: 4.2 m.
- Blender scene units: metres.
- Keep doors, frames, glazing, decorative meshes, and collision as separate objects.

## Ground floor — public intake, secure operations, garage

| Zone | Target planning area | Notes |
|---|---:|---|
| Public lobby / reception | 10 × 8 m | Front entry, reception desk, waiting area |
| Public report / service counter | 7 × 6 m | Adjacent to lobby; public-facing |
| Booking / intake | 9 × 8 m | Controlled staff access, interview intake point |
| Processing / fingerprinting | 7 × 6 m | Near booking; equipment props later |
| Temporary holding | 8 × 6 m | Secure access and staff sightlines |
| Cell block | 12 × 10 m | Multiple cell bays; doors must be functional in game |
| Vehicle garage | 20 × 12 m | Confirm vehicle turning, entry width, and clear height |
| Staff lockers / support | 8 × 6 m | Staff-only circulation |
| Stair / lift cores | Approx. 5 × 8 m each | Continuous vertical circulation; validate landing alignment |

## Level 2 — communications and tactical support

| Zone | Target planning area | Notes |
|---|---:|---|
| Dispatch / communications | 14 × 10 m | Console rows, wall display, quiet equipment zone |
| SWAT briefing | 12 × 8 m | Briefing table, display wall, clear route to equipment |
| SWAT equipment | 8 × 7 m | Secure racks and loadout props |
| Evidence intake | 8 × 7 m | Controlled receiving point |
| Evidence storage | 10 × 8 m | Secure shelving; avoid unnecessary small props in collision |
| Armory | 8 × 7 m | Secure door and storage racks |
| Staff break / support | 8 × 6 m | Secondary staff area |

## Level 3 — investigations and administration

| Zone | Target planning area | Notes |
|---|---:|---|
| Detective bullpen | 14 × 10 m | Desks and shared investigation boards |
| Detective offices | 3–5 rooms, about 4 × 4 m each | Keep windows and doors modular |
| Interview rooms | 2 rooms, about 4 × 5 m each | Include observation/control side where useful |
| Case review / conference | 9 × 7 m | Table, wall display, chair circulation |
| Administration | 8 × 7 m | Controlled access |
| Records / secure files | 7 × 6 m | Storage shelving and limited access |

## Roof

- Helipad deck and visible H/perimeter markings.
- HVAC service area kept out of the intended landing area.
- Roof access vestibule and stair headhouse to be added in the next geometry pass.
- Preserve a clear approach/landing envelope; final dimensions must be checked against the intended helicopter assets.

## Door and opening schedule

| Type | Planning clear opening | Use |
|---|---:|---|
| Public entrance | 2.4–3.0 m | Main lobby |
| Standard interior | 0.9–1.0 m | Offices and support rooms |
| Interview / staff | 0.9–1.0 m | Secure staff zones |
| Secure cell | 0.9–1.1 m | Cell block; door model and collision must be tested |
| Garage vehicle entry | 4.0–5.0 m wide | Vehicle clearance; verify target vehicle fleet |
| Double equipment door | 1.6–2.0 m | SWAT / evidence movement |
| Roof access | 1.0–1.2 m | Stair headhouse and roof |

## Acceptance checks before calling the interior playable

- [ ] Every occupied room has a navigable route from a stair/lift or entrance.
- [ ] Door openings are actual gaps in wall geometry, not painted-on door textures.
- [ ] Doors have appropriate collision and opening behavior if interactive.
- [ ] Stairs connect at matching elevations with landings and safe head clearance.
- [ ] Cells, armory, evidence, and roof have clear staff-only access boundaries.
- [ ] Garage accommodates intended vehicle width, height, and turning envelope.
- [ ] Player camera and character collision are tested in narrow areas.
- [ ] No decorative mesh is used as the primary collision surface.
- [ ] Verify emergency egress and accessibility concepts before finalising layout.
