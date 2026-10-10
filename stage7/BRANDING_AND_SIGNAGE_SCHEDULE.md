# Branding and Signage Schedule

| Sign | Proposed location | Editable content |
|---|---|---|
| Main exterior sign | Front facade above entrance canopy | Full agency name and acronym |
| Public lobby plaque | Near public entrance | Acronym and headquarters subtitle |
| Future garage sign | Vehicle garage entry | Agency name / unit designation |
| Future secure-area plaques | Booking, cells, armory, evidence, dispatch | Room title and access classification |
| Future wayfinding set | Corridors, stairs, elevator lobby | Floor, department, directional arrows |

## Rules for a rebrand-friendly asset

1. Keep all sign objects in a dedicated `PDHQ_BRANDING_SIGNS` collection.
2. Keep all names, acronyms, and colors in one configuration block.
3. Never bake the agency name into structural wall geometry.
4. Use replaceable decal/logo meshes for insignia; do not make logos part of the wall mesh.
5. Check font availability and text legibility before export. For production, convert approved text to mesh and create UVs/materials as required by the GTA asset pipeline.
6. Rebranding the physical model does not reconfigure framework jobs, door access, uniforms, map blips, or server permissions; those remain separate server-side work.
