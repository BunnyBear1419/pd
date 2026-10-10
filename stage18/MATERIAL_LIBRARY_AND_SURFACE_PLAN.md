# Stage 18 — Material library and surface plan

## Surface schedule

| Surface/use | Shared blockout material | Production direction |
|---|---|---|
| Exterior main walls | Concrete Light | Tiled concrete/plaster or trim-sheet panels |
| Recesses/base/plinth | Concrete Dark | Dark concrete or coated masonry |
| Windows/curtain wall | Glass Tint | GTA-compatible glass shader; validate transparency |
| Frames, rails, handles | Aluminum / Black Metal | Shared metal trim texture |
| Interior partitions | Interior Wall | Reusable painted-wall material |
| Public floors | Floor Stone | Tiled floor texture; keep roughness readable |
| Secure floors | Floor Secure | Durable sealed concrete/rubber |
| Agency feature surfaces | Agency Primary / Accent | Replace colors via agency branding configuration |
| Signs/emblems | Signage Back | Final vector/raster atlas or mesh lettering |
| Temporary clearance guides | Guide Yellow | Remove or hide before final export |
| Roof | Roof Membrane | Roof texture plus separate helipad markings |
| Site planting | Landscape | Replace proxy color with optimized ground/foliage assets |

## Material discipline
- Prefer a small shared library over per-object duplicates.
- Keep temporary guide materials unmistakable and exclude guide geometry from final export.
- Do not use transparency as a shortcut for every glass surface; final GTA shader and draw order must be checked in-game.
- Assign production materials by surface role, not just object name. Name-based assignment is only an optional starting pass.
- Use trim sheets, atlases, and tiling textures to reduce texture count and draw-call pressure.
- Validate material slot counts and shader compatibility after Sollumz conversion.

## Important limitations
This stage creates Blender Principled materials as authoring placeholders. It does not create final PBR texture images, UV layouts, GTA shader graphs, collision meshes, LODs, portals, occlusion, or a ready-to-stream MLO. Visual fidelity and performance remain unverified until export and in-game testing.
