# Stage 27 — Room layout and circulation conflict review

Stage 27 adds a non-destructive Blender screening pass after the room partitions and furniture proxies have been generated. It creates review-only wireframe envelopes for the public entry/reception approach, booking approach, garage drive aisle, dispatch, secure storage, and interview rooms.

It then checks approximate world-space bounding-box intersections between these route envelopes and nearby named floor objects, and between major furniture proxies and partition meshes. Findings are written to the Blender Text datablock `PDHQ_STAGE27_ROOM_CIRCULATION_REPORT`.

## Run

The Stage 25 orchestrator includes this pass after Stage 4:

```powershell
blender -b --python stage25/build_stage25_scene.py -- --output build/pdhq_stage27_blockout.blend --log build/pdhq_stage27_build_report.json
```

## Interpret results carefully

- `REVIEW_POSSIBLE_OBSTRUCTION` means inspect the reported objects in Blender; it is not proof that the route is physically blocked.
- `NO_AABB_INTERSECTION_FOUND` is not proof of a safe, accessible, or usable route.
- The route dimensions and coordinates are provisional. Adjust them to the final room plan, door positions, stair landings, and actual garage entrance.
- The wireframe collection `PDHQ_STAGE27_CIRCULATION_REVIEW` is a review aid only and must be hidden/excluded from final exports.
- This pass does not move furniture or walls automatically, certify accessibility, calculate vehicle swept paths, or create production FiveM assets.
