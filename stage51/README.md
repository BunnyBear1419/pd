# Stage 51 — FiveM resource assembly

## Purpose
Assemble the actual resource with fxmanifest.lua, stream assets, metadata and installation notes; do not ship templates as finished assets.

## Workflow
1. Back up the last accepted Blender scene and exported resource.
2. Use the approved outputs of Stages 36–38 as review references, not as authoritative construction plans.
3. Complete the work in the real Blender/Sollumz/CodeWalker/FiveM toolchain.
4. Run applicable audits, inspect findings manually, and retain evidence.

## Acceptance checklist
- [ ] Manifest paths match real files
- [ ] dependencies are declared
- [ ] no placeholder template remains
- [ ] resource starts cleanly
- [ ] install/rollback steps work
- [ ] Record tool versions, evidence, defects, reviewer and date.
- [ ] Do not treat CI/package success as proof of external toolchain or in-game validity.

## Status boundary
This stage defines the work package and acceptance gate. It is not complete until the real work and evidence exist. Do not claim production readiness without successful export, CodeWalker inspection and FiveM testing.

## Resource deployment preflight

Run the audit against the **actual exported resource folder** (not the repository root):

```bash
python stage51/audit_stage51_resource_deployment.py path/to/pdhq_resource --server-cfg path/to/server.cfg --json-out build/stage51_deployment_report.json
```

It checks for `fxmanifest.lua`, a populated `stream/` directory, recognized asset extensions, basic manifest declarations, referenced stream paths, YTYP registration hints, possible template placeholders, and—if supplied—the resource's `ensure`/`start` line in `server.cfg`.

Run its synthetic fixture test with:

```bash
python stage51/audit_stage51_resource_deployment.py --self-test
```

The fixture test is only a test of the checker. Do not run the deployment audit against a placeholder folder and interpret it as evidence that the MLO is ready. It cannot parse all Lua syntax, validate GTA binary assets, or replace a staging-server test.
