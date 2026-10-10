"""Stage 11 — interior architectural finish accents.

Run after Stages 2–4 in the same Blender scene. Adds lightweight, non-structural
interior finish details in its own collection. This is a visual blockout pass:
inspect placements in Blender before any Sollumz/GTA export.
"""
import bpy

PREFIX = "PDHQ_INTDETAIL_"
COLLECTION_NAME = "PDHQ_INTERIOR_ARCHITECTURAL_DETAILS"
FLOOR_H = 4.2
FLOORS = 3

COLORS = {
    "graphite": (0.075, 0.09, 0.105, 1.0),
    "panel": (0.20, 0.25, 0.27, 1.0),
    "light": (0.64, 0.68, 0.68, 1.0),
    "accent": (0.72, 0.53, 0.20, 1.0),
    "teal": (0.06, 0.19, 0.21, 1.0),
}
scene = bpy.context.scene
collection = bpy.data.collections.get(COLLECTION_NAME)
if collection is None:
    collection = bpy.data.collections.new(COLLECTION_NAME)
    scene.collection.children.link(collection)
for obj in list(collection.objects):
    bpy.data.objects.remove(obj, do_unlink=True)

def material(name, color, metallic=0.0, roughness=0.55):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return mat

MAT_GRAPHITE = material("MAT_IntDetail_Graphite", COLORS["graphite"], 0.25)
MAT_PANEL = material("MAT_IntDetail_Panel", COLORS["panel"], 0.12)
MAT_LIGHT = material("MAT_IntDetail_LightTrim", COLORS["light"], 0.25)
MAT_ACCENT = material("MAT_IntDetail_Accent", COLORS["accent"], 0.35)
MAT_TEAL = material("MAT_IntDetail_Dispatch", COLORS["teal"], 0.12)

def add_box(name, loc, dims, mat, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = PREFIX + name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    if bevel:
        mod = obj.modifiers.new("Finish_Edge_Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)
    return obj

def add_text(name, body, loc, size, mat):
    curve = bpy.data.curves.new(name + "_CURVE", "FONT")
    curve.body = body
    curve.size = size
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.extrude = 0.001
    obj = bpy.data.objects.new(PREFIX + name, curve)
    collection.objects.link(obj)
    obj.location = loc
    # Default faces toward -Y; lobby's front-facing wall is viewed from +Y.
    obj.rotation_euler = (-1.57079632679 if name.startswith("LOBBY_") else 1.57079632679, 0.0, 0.0)
    obj.data.materials.append(mat)
    return obj

# Corridor skirting and thin protective rails, placed just inside corridor faces.
for floor in range(FLOORS):
    z = floor * FLOOR_H
    for side, y in (("N", 2.70), ("S", -2.70)):
        add_box("F%d_CORRIDOR_%s_SKIRT" % (floor + 1, side),
                (0, y, z + 0.12), (51.0, 0.07, 0.20), MAT_GRAPHITE)
        add_box("F%d_CORRIDOR_%s_ACCENT" % (floor + 1, side),
                (0, y + (0.05 if side == "N" else -0.05), z + 0.25),
                (51.0, 0.025, 0.035), MAT_ACCENT)

# Lobby reception feature wall, located against the front-left solid wall segment.
add_box("LOBBY_FEATURE_BACKER", (-15.0, -18.72, 2.15), (10.5, 0.10, 2.75), MAT_GRAPHITE)
for i in range(15):
    x = -19.8 + i * 0.685
    add_box("LOBBY_FEATURE_SLAT_%02d" % (i + 1),
            (x, -18.645, 2.15), (0.035, 0.055, 2.48),
            MAT_ACCENT if i in (0, 14) else MAT_PANEL)
add_box("LOBBY_FEATURE_HEADER", (-15.0, -18.60, 3.38), (8.7, 0.045, 0.045), MAT_LIGHT)
add_text("LOBBY_WELCOME_LABEL", "WELCOME",
         (-15.0, -18.57, 2.95), 0.30, MAT_LIGHT)

# Dispatch backdrop: subdued panel behind the console line on the rear wall.
add_box("DISPATCH_BACKDROP", (1.0, 18.68, FLOOR_H + 2.0),
        (23.0, 0.12, 2.8), MAT_TEAL)
for i in range(12):
    x = -9.0 + i * 1.8
    add_box("DISPATCH_BACKDROP_RIB_%02d" % (i + 1),
            (x, 18.59, FLOOR_H + 2.0), (0.045, 0.055, 2.55), MAT_PANEL)
add_text("DISPATCH_WALL_LABEL", "DISPATCH",
         (1.0, 18.55, FLOOR_H + 3.0), 0.34, MAT_LIGHT)

# Evidence and armory wall strips visually distinguish controlled-access rooms.
for i, x in enumerate((-20.0, -16.0, -12.0)):
    add_box("EVIDENCE_WALL_MARKER_%02d" % (i + 1),
            (x, 18.55, FLOOR_H + 3.15), (1.6, 0.08, 0.18), MAT_ACCENT)
for i, x in enumerate((-20.0, -17.5, -15.0, -12.5)):
    add_box("ARMORY_WALL_MARKER_%02d" % (i + 1),
            (-15.90, 5.5 + i * 1.0, FLOOR_H + 3.0), (0.06, 0.85, 0.12), MAT_ACCENT)

# Detective floor: understated workstation-zone wall panels at the back wall.
for i, x in enumerate((-10.0, -4.0, 2.0, 8.0, 14.0, 20.0)):
    add_box("DETECTIVE_WALL_PANEL_%02d" % (i + 1),
            (x, 18.62, 2 * FLOOR_H + 2.05), (4.8, 0.10, 2.4), MAT_PANEL)
    add_box("DETECTIVE_PANEL_TOPLINE_%02d" % (i + 1),
            (x, 18.55, 2 * FLOOR_H + 3.27), (4.5, 0.035, 0.045), MAT_LIGHT)

# Small wall-protection strips in the two stair-core zones; schematic only.
for floor in range(FLOORS):
    z = floor * FLOOR_H
    for sx in (-22.0, 22.0):
        add_box("F%d_STAIR_CORE_GUARD_%s" % (floor + 1, str(sx).replace("-", "M")),
                (sx, -3.7, z + 1.05), (3.8, 0.08, 0.12), MAT_GRAPHITE)

print("Stage 11 interior finish accents generated in " + COLLECTION_NAME)
print("Inspect all wall clearances, door openings, text orientation, furniture overlap, and room alignment.")
