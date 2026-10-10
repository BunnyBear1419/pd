# Stage 30 — Exterior site and helipad acceptance checklist

## Site and public entrance
- [ ] Confirm actual site boundary, north/orientation, street connection and terrain level.
- [ ] Verify the front gate, accessible landing, pedestrian route, crossing, drop-off and bollards align with the modeled entrance.
- [ ] Check step-free route, turning space, door approach and unobstructed public access against the applicable local requirements.
- [ ] Confirm fence and gate leaves do not block the public approach, vehicle path or emergency route.

## Garage, service and emergency access
- [ ] Replace provisional garage/service coordinates with the actual openings and drive geometry.
- [ ] Test representative police SUVs, vans and emergency vehicles with a true swept-path review, not only boxes.
- [ ] Confirm entrance/exit operation, turning, headroom, ramp grade, pedestrian separation and secure prisoner-transfer route.
- [ ] Keep emergency access clear of bollards, landscape, light poles, gates, parked vehicles and site furniture.
- [ ] Review gate widths, queue space, sightlines, access control and responder access with the server/site design requirements.

## Rooftop helipad and equipment
- [ ] Confirm the intended helicopter dimensions and the appropriate landing-area design basis with qualified aviation/site professionals.
- [ ] Inspect the pad against parapets, stair/elevator overruns, antennas, HVAC, lighting and every other rooftop obstacle.
- [ ] Review approach/departure surfaces, rotor/obstacle clearance, edge protection, fire response, lighting, drainage and structural loading.
- [ ] Confirm rooftop access is safe and does not route public traffic through secure operational areas.

## Blender/export gate
- [ ] Run `stage30/audit_stage30_exterior_helipad_clearance.py` and inspect `PDHQ_STAGE30_EXTERIOR_HELIPAD_REPORT`.
- [ ] Inspect all guide geometry in orthographic and perspective views; the automated AABB screen is advisory only.
- [ ] Mark temporary site/access guides for exclusion or deliberate conversion before production export.
- [ ] Re-run the build and all reviews after any site-coordinate or roof-layout change.

**Acceptance rule:** Stage 30 is not passed solely because the script runs. Actual site dimensions, emergency vehicle paths and helipad requirements require manual review by appropriately qualified people. This checklist is not regulatory or aviation approval.
