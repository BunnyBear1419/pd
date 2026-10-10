# Stage 33 — Safe, Repeatable Build Workflow

This stage adds guardrails to the Blender build orchestrator. It does not change the model geometry or claim to fix existing layout problems.

## What changed

- The build now refuses to replace an existing output `.blend` unless `--overwrite` is explicitly provided.
- With `--overwrite`, it first makes a timestamped sibling backup of the existing output.
- The build rejects using the same path for the Blender output and JSON log.
- The generator plan starts with Stage 2, whose scene setup deletes scene objects and reconstructs the blockout; do not run it against a scene you intend to preserve without saving a separate copy.
- The report records whether overwrite was explicitly allowed.

## Recommended use

First build to a new versioned path:

```bash
blender -b --python stage25/build_stage25_scene.py -- --output build/pdhq_v001.blend --log build/pdhq_v001_report.json
```

To deliberately replace an existing output, the backup guard must be explicitly enabled:

```bash
blender -b --python stage25/build_stage25_scene.py -- --output build/pdhq_v001.blend --log build/pdhq_v001_report.json --overwrite
```

Keep important project files under version control or in separate backups. The backup is a copy of the existing output file, not a snapshot of every asset in the project.

## Limitations

- This is still a schematic Blender blockout/proxy generator.
- CI only compiles scripts and packages source; it does not execute Blender.
- A build report marked completed means the scripts ran, not that the scene is architecturally correct or ready for FiveM.
