# Stage 54 — Release packaging and documentation

## Purpose
Prepare a versioned release bundle only after exported resource and test matrix pass.

## Workflow
1. Back up the last accepted Blender scene and exported resource.
2. Use the approved outputs of Stages 36–38 as review references, not as authoritative construction plans.
3. Complete the work in the real Blender/Sollumz/CodeWalker/FiveM toolchain.
4. Run applicable audits, inspect findings manually, and retain evidence.

## Acceptance checklist
- [ ] Include install/rollback steps, known limitations, tool versions, asset manifest and changelog
- [ ] exclude review artifacts from runtime resource
- [ ] Record tool versions, evidence, defects, reviewer and date.
- [ ] Do not treat CI/package success as proof of external toolchain or in-game validity.

## Status boundary
This stage defines the work package and acceptance gate. It is not complete until the real work and evidence exist. Do not claim production readiness without successful export, CodeWalker inspection and FiveM testing.


## Release-candidate gate

Run from the project root after the actual external evidence has been collected:

```bash
python stage54/audit_stage54_release_candidate.py --root . --output build/stage54_release_candidate_report.json
```

The gate checks for a real Blender scene, export manifest, FiveM resource manifest and stream assets, CodeWalker review, measured performance profile, multiplayer QA record, and release notes with explicit backup/rollback guidance. Missing evidence blocks the candidate. Presence of files is not proof that the evidence is valid; the report always keeps `production_ready: false`.

Synthetic validator check:

```bash
python stage54/audit_stage54_release_candidate.py --self-test
```

Before a real deployment, back up the current resource and configuration, test under a staging resource name, and retain a known-good rollback copy. Do not deploy a schematic or placeholder blockout as a finished MLO.
