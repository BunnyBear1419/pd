# Stages 49–55 — External export, QA and release gate

Run from the repository root:

```bash
python stage49/audit_stage49_55_release_gate.py --output build/stage49_55_release_gate.json
```

The audit checks for the actual Blender scene, export manifest, FiveM manifest and stream directory, CodeWalker review, measured performance profile, multiplayer QA record, and release notes. Missing evidence is reported as a blocker; the script never fabricates validation or marks the MLO production-ready.

Stages 49–55 still require real Blender/Sollumz/CodeWalker/FiveM execution and human inspection. A successful GitHub workflow only verifies the repository tools/specification, not the in-game MLO.

## Export inventory integrity check

Before reviewing a real export, create `build/export_manifest.json` with `schema_version: 1` and a non-empty `assets` array. Each asset record must include a project-root-relative path under `resource/stream/`, exact `size_bytes`, and SHA-256 digest. The validator rejects traversal paths, missing files, duplicate entries, invalid hashes, size mismatches, and hash mismatches.

Run it against actual exported files:

```bash
python stage49/validate_export_manifest.py --root . --manifest build/export_manifest.json
```

Run the validator's fixture tests without a real export:

```bash
python stage49/validate_export_manifest.py --self-test
```

The fixture test only checks the validator's logic; it is not evidence that the police station has been exported or tested.
