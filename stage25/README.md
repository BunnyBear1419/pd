# Stage 25 — Blender build orchestration

This stage adds a repeatable entry point for generating the schematic PDHQ scene and running the existing non-destructive audit scripts in order. It saves a `.blend` file and a JSON run report when executed successfully.

## Requirements

- Install Blender on the Windows workstation or build machine.
- Clone/download this repository so the `stage2` through `stage25` folders are together.
- Run the command from the repository root. Use the `blender` executable available on your system PATH, or replace `blender` with its full path.

## Windows PowerShell example

```powershell
blender -b --python stage25/build_stage25_scene.py -- --output build/pdhq_stage31_blockout.blend --log build/pdhq_stage31_build_report.json
```

If the target `.blend` already exists, the runner now refuses to overwrite it unless you explicitly opt in. To replace it while preserving a timestamped backup first:

```powershell
blender -b --python stage25/build_stage25_scene.py -- --output build/pdhq_stage31_blockout.blend --log build/pdhq_stage31_build_report.json --overwrite
```

Prefer a new versioned output filename for the first run. Stage 2 resets the scene objects and rebuilds the blockout, so only run the generator against a copy of any scene you want to preserve.

To generate without running the audit scripts:

```powershell
blender -b --python stage25/build_stage25_scene.py -- --output build/pdhq_stage25_blockout.blend --skip-audits
```

The default run generates Stage 2, applies the Stage 26 slab-opening/vertical-circulation reconciliation, then generates Stages 3–4, branding/signage/detail and site-guide passes (7–15), then scene/layout/structural/room audits (5, 6, 16, 17, 27, 28, 29, 30), Stage 18 materials, and final export/performance/geometry/visibility audits (19–22), followed by the Stage 31 optimization/export manifest review. Stage 23 remains a validator for a real exported FiveM resource folder, not a Blender generation step. Stage 24 checks repository readiness and is run as a standard Python script outside Blender.

## Output and failure behavior

- `.blend`: saved only after all requested steps finish.
- JSON report: records each completed script and the overall status.
- On failure: the report includes the error/traceback and the script attempts to save a `.partial.blend` for diagnosis.

## Important limitations

The generated scene is a schematic blockout with placeholder geometry and guide objects. This runner does not call Sollumz, export GTA assets, generate actual MLO archetypes/portals/occlusion/collision/LODs, or test the result in FiveM. Review the scene and all audit reports in Blender, then proceed through the Stage 23 export/resource checklist. Do not upload the generated `.blend` or call the MLO production-ready until the external tool and in-game gates pass.
