"""Stage 5 non-destructive scene audit for the PDHQ Blender blockout.

Run after Stages 2-4 in the same Blender scene. This script does not modify
or export geometry; it writes a readable report to the Blender Text Editor and
prints the same report to the system console.
"""
import bpy
from collections import Counter

PREFIX = "PDHQ_"
lines = []
def out(message=""):
    lines.append(str(message))

scene = bpy.context.scene
objects = list(scene.objects)
meshes = [o for o in objects if o.type == "MESH"]
triangles = 0
for obj in meshes:
    try:
        mesh = obj.to_mesh()
        triangles += sum(max(0, len(poly.vertices)-2) for poly in mesh.polygons)
        obj.to_mesh_clear()
    except Exception as exc:
        out("WARNING: triangle estimate failed for %s: %s" % (obj.name, exc))

out("PDHQ STAGE 5 SCENE AUDIT")
out("=" * 72)
out("Scene: %s" % scene.name)
out("Objects: %d | Meshes: %d | Estimated triangles: %d" % (len(objects), len(meshes), triangles))
out("")
out("COLLECTION COUNTS")
for col in sorted(bpy.data.collections, key=lambda c: c.name):
    count = len(list(col.all_objects))
    if count:
        out("  %-34s %4d objects" % (col.name, count))

out("")
out("REVIEW FLAGS (warnings are not automatic failures)")
unapplied_scale = []
large_meshes = []
high_tri_meshes = []
missing_materials = []
unprefixed = []
for obj in meshes:
    scale = obj.scale
    if any(abs(v-1.0) > 0.001 for v in scale):
        unapplied_scale.append("%s scale=(%.3f, %.3f, %.3f)" % (obj.name, scale.x, scale.y, scale.z))
    dims = obj.dimensions
    if max(dims) > 20.0:
        large_meshes.append("%s dimensions=(%.1f, %.1f, %.1f)" % (obj.name, dims.x, dims.y, dims.z))
    try:
        tri_count = sum(max(0, len(poly.vertices)-2) for poly in obj.data.polygons)
        if tri_count > 50000:
            high_tri_meshes.append("%s triangles=%d" % (obj.name, tri_count))
    except Exception:
        pass
    if len(obj.data.materials) == 0:
        missing_materials.append(obj.name)
    if not obj.name.startswith(PREFIX):
        unprefixed.append(obj.name)

def report_group(title, values):
    out("%s: %d" % (title, len(values)))
    for value in values[:80]:
        out("  - " + value)
    if len(values) > 80:
        out("  ... and %d more" % (len(values)-80))

report_group("Objects with unapplied object scale", unapplied_scale)
report_group("Meshes with a dimension above 20 m (check intentional building shells)", large_meshes)
report_group("Meshes above 50,000 triangles", high_tri_meshes)
report_group("Meshes without materials", missing_materials)
report_group("Meshes without the PDHQ_ name prefix", unprefixed)

out("")
out("EXPORT READINESS REMINDERS")
out("- This audit does not validate GTA archetypes, portals, room flags, occlusion, or game collision.")
out("- This audit does not detect all mesh intersections, duplicate surfaces, bad normals, or invisible-in-game assets.")
out("- Hide or remove camera/light objects, zone empties, guide labels, and garage clearance volumes from export selection.")
out("- Replace proxy materials and geometry; build intentional low-cost collision and LOD assets.")
out("- Test exported assets in a local FiveM server at realistic streaming distance.")
out("- Never treat this report alone as proof that the MLO is optimized or game-ready.")

report = "\n".join(lines)
text_block = bpy.data.texts.get("PDHQ_STAGE5_AUDIT_REPORT") or bpy.data.texts.new("PDHQ_STAGE5_AUDIT_REPORT")
text_block.clear()
text_block.write(report)
print(report)
