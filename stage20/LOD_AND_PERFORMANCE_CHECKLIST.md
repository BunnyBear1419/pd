# LOD and performance checklist

## Scene triage

- [ ] Run `audit_stage20_lod_performance.py` on a saved copy of the scene.
- [ ] Inspect the highest-polygon objects first; confirm whether dense geometry is visible or hidden/internal.
- [ ] Review large architectural assets for a simplified distant silhouette.
- [ ] Review small props with unnecessary bevels, dense curves, or hidden faces.
- [ ] Review objects with four or more material slots for redundant material assignments and possible atlas opportunities.
- [ ] Inspect unused materials before deleting them; they may be intentionally staged for later work.
- [ ] Review unapplied object scale and modifiers before final export; do not blindly apply or remove either.
- [ ] Keep temporary guides, clearance volumes, labels, and proxy geometry out of final exports after manually confirming what is temporary.

## Manual LOD design

- [ ] Identify which assets are repeated and likely to dominate scene cost.
- [ ] Preserve the exterior silhouette and important police-HQ landmarks in lower-detail variants.
- [ ] Remove tiny bevels, interior faces, and hidden details from distant variants where safe.
- [ ] Check transitions for visible popping, gaps, z-fighting, and material changes.
- [ ] Verify each LOD's origin, dimensions, naming, material setup, and intended distance using the current Sollumz workflow.
- [ ] Do not use a single global distance or polygon target without profiling the actual asset and scene.

## FiveM validation

- [ ] Export only reviewed production assets; inspect the exported files in CodeWalker.
- [ ] Verify collision separately from render geometry and test player movement, vehicle access, stairs, doors, roof, and helipad.
- [ ] Check portals, occlusion, interior visibility, and streaming setup where applicable.
- [ ] Test on a clean FiveM client at near, medium, and far distances, including entry/exit and reconnect.
- [ ] Compare frame time, memory/streaming behavior, and visual quality before and after each optimization.
- [ ] Repeat tests with other streamed resources enabled to look for conflicts.

## Interpretation guardrails

The script reports Blender polygon counts, dimensions, modifiers, material slots, and names. These are review clues, not draw-call counts or in-game benchmarks. It neither creates LODs nor proves performance. Record real measurements from the target FiveM environment before declaring an optimization successful.
