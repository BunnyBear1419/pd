# Stage 28 — Garage and secure ground-floor layout

Stage 28 adds review envelopes for the garage drive aisle, provisional vehicle entry approach, protected pedestrian route, and garage-to-booking secure transfer route. It screens the envelopes against selected scene meshes and writes findings to the Blender Text datablock `PDHQ_STAGE28_GARAGE_SECURE_REPORT`.

## Run

Run after the scene generators, preferably through the Stage 25 orchestrator:

```powershell
blender -b --python stage25/build_stage25_scene.py -- --output build/pdhq_stage28_blockout.blend --log build/pdhq_stage28_build_report.json
```

The orchestrator now runs this review after Stage 27. You can also run the script directly from Blender's Scripting workspace once Stages 2–4 and the garage guides are present.

## Review checklist

- Confirm the actual garage opening and approach; the current east-side entry is provisional.
- Inspect vehicle bay widths, aisle clearance, turning path, and garage-to-street transition using the intended emergency vehicles.
- Keep pedestrian circulation physically separated from reversing/turning vehicles where practical.
- Confirm the booking transfer path is secure, controlled, and does not cross public reception circulation.
- Inspect doors, partitions, holding-cell fixtures, workbench and storage for real clearances.
- Hide or exclude `PDHQ_STAGE28_GARAGE_SECURE_REVIEW` before production export.

The report uses world-axis-aligned bounding boxes. It is a screening aid, not a swept-path simulation, automatic repair, accessibility/fire-code certification, or proof of FiveM functionality. Blender, Sollumz, CodeWalker, and in-game validation remain required.
