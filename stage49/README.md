# Stages 49–55 — External export, QA and release gate

Run from the repository root:

```bash
python stage49/audit_stage49_55_release_gate.py --output build/stage49_55_release_gate.json
```

The audit checks for the actual Blender scene, export manifest, FiveM manifest and stream directory, CodeWalker review, measured performance profile, multiplayer QA record, and release notes. Missing evidence is reported as a blocker; the script never fabricates validation or marks the MLO production-ready.

Stages 49–55 still require real Blender/Sollumz/CodeWalker/FiveM execution and human inspection. A successful GitHub workflow only verifies the repository tools/specification, not the in-game MLO.
