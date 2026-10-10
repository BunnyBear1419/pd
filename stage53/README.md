# Stage 53 — Gameplay and multiplayer QA

## Purpose
Run a structured test matrix for floors, rooms, routes, doors, vehicles, roof access and multiplayer streaming.

## Workflow
1. Back up the last accepted Blender scene and exported resource.
2. Use the approved outputs of Stages 36–38 as review references, not as authoritative construction plans.
3. Complete the work in the real Blender/Sollumz/CodeWalker/FiveM toolchain.
4. Run applicable audits, inspect findings manually, and retain evidence.

## Acceptance checklist
- [ ] Test spawn/reconnect/resource restart
- [ ] walk and drive routes
- [ ] inspect every room with multiple clients
- [ ] record and retest defects
- [ ] Record tool versions, evidence, defects, reviewer and date.
- [ ] Do not treat CI/package success as proof of external toolchain or in-game validity.

## Status boundary
This stage defines the work package and acceptance gate. It is not complete until the real work and evidence exist. Do not claim production readiness without successful export, CodeWalker inspection and FiveM testing.


## QA matrix helper

Create a structured, initially uncompleted multiplayer QA record:

```bash
python stage53/manage_stage53_multiplayer_qa.py --init --output build/fivem_multiplayer_test.json
```

After performing the real tests, fill in each case's result (`pass`, `fail`, `blocked`, `not_applicable`, or `not_run`), add evidence references and notes, then validate:

```bash
python stage53/manage_stage53_multiplayer_qa.py --validate build/fivem_multiplayer_test.json
```

The matrix covers fresh join, interior/exterior visibility, reconnect, respawn, resource restart, routes across all floors, doors, collision, vehicle garage, rooftop/helipad, textures, two-client and multi-client streaming, and a long-session check. A `pass` without evidence is flagged for review.

Run the tool's synthetic self-test with:

```bash
python stage53/manage_stage53_multiplayer_qa.py --self-test
```

The helper does not execute or automate GTA/FiveM. Never mark a test as passed unless it was actually performed against the target build; production readiness remains false pending human sign-off.
