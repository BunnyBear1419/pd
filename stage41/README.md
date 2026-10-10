# Stages 41–48 — Generated design and optimization specification

Run from the repository root:

```bash
python stage41/generate_stage41_48_design_specs.py --output build/stage41_48_design_spec.json
```

The generator produces room-specific interior kit, lighting intent, collision profile, material guidance, LOD/geometry checks, and streaming review requirements for all rooms in the Stage 36 program. It consumes Stage 37 placements if `build/stage37_floor_fit.json` exists; otherwise it clearly marks placements unavailable.

This is a design specification only. It does not create façade or interior geometry, texture files, collision meshes, LODs, Sollumz archetypes, or a working FiveM MLO. Keep `production_ready` false until external production and validation are complete.
