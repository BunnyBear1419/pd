# Stage 10 Architectural Detail Checklist

## Visual alignment
- [ ] Run Stage 2 first, then Stage 10 in the same Blender scene.
- [ ] Confirm fins do not cover door openings, windows, or signage.
- [ ] Confirm each mullion sits on the glass plane and not in front of the interior.
- [ ] Inspect canopy fascia, underside, columns, and entrance clearance.
- [ ] Compare floor bands with slab heights and adjacent façade elements.
- [ ] Check the Stage 7 name sign, Stage 8 wayfinding, and Stage 9 crest for overlap.

## Optimization
- [ ] Keep the detail collection separate until approved.
- [ ] Apply or remove bevel modifiers according to the final export pipeline.
- [ ] Merge repeated static pieces where that benefits the chosen asset pipeline.
- [ ] Check normals, material slots, collision needs, draw distance, and LOD policy.
- [ ] Run Stage 5 scene audit and Stage 6 layout validation after all generators.

## Release gate
Python syntax and ZIP packaging do not prove Blender execution, Sollumz export, or FiveM stability. Test the exported resource in-game and inspect streaming/performance before calling the MLO production-ready.
