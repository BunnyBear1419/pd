# Stage 14 — Exterior Entrances and Vehicle Approach

## Purpose
Create a separate, rerunnable Blender guide layer for the public entrance, accessible pedestrian route, covered drop-off, protective bollards, emergency/service access, and provisional garage circulation.

## Run
1. Open the police HQ Blender project in Blender.
2. Open the **Scripting** workspace and load stage14/generate_stage14_exterior_access.py.
3. Run the script.
4. Inspect the PDHQ_EXTERIOR_ACCESS_GUIDES collection in the viewport and Outliner.

The script deletes and rebuilds only its own collection. It does not modify prior stage collections.

## Important configuration
Edit the CONFIG dictionary at the top of the script before running:
- front_y, front_entrance_center_x, entrance_width: Stage 2 public façade/entrance reference.
- dropoff values and public_path values: frontage approach dimensions.
- garage_entry_center_x, garage_entry_y, garage_opening_width: **provisional** garage opening reference. Confirm the actual opening in Blender before treating these as aligned.
- service_center_x, service_y, service_width: provisional service route.
- show_turning_envelope: toggle the broad review envelope.

## What this stage is — and is not
All objects are visual layout guides and labels. They are not final road meshes, working doors, vehicle AI paths, production collisions, navmesh, or game-ready Sollumz assets. The turning envelope is not a vehicle swept-path simulation. Check route widths and turning behavior using the actual intended emergency vehicles.

## Review checklist
- Confirm public entrance guides line up with the Stage 2 façade and canopy.
- Verify accessible approach and drop-off do not conflict with doors, steps, or the building footprint.
- Confirm actual garage/service openings before repositioning their provisional guides.
- Check emergency lane, bollards, and turning envelope for overlap with walls, props, curb edges, and each other.
- Confirm sufficient clearance for the largest intended vehicle and pedestrian movement.
- Hide or delete this guide collection before production export if these guide meshes are not wanted in-game.
- Run the project packaging workflow; Blender scene execution and FiveM validation still need to be performed separately.
