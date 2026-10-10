"""Stage 10 — non-destructive exterior architectural detail pass.

Run after Stage 2 in the same Blender scene. Adds editable façade fins, glazing
mullions, floor bands, and entrance canopy trim to a dedicated collection.
Coordinates are based on the Stage 2 blockout and must be inspected in Blender.
"""
import bpy

PREFIX = "PDHQ_DETAIL_"
COLLECTION_NAME = "PDHQ_ARCHITECTURAL_DETAILS"
W = 54.0
D = 38.0
FLOOR_H = 4.2
FLOORS = 3

COLORS = {
    "dark": (0.075, 0.095, 0.11, 1.0),
    "metal": (0.30, 0.34, 0.36, 1.0),
    "accent": (0.72, 0.55, 0.22, 1.0),
    "glass": (0.045, 0.12, 0.15, 1.0),
}
scene = bpy.context.scene
collection = bpy.data.collections.get(COLLECTION_NAME)
if collection is None:
    collection = bpy.data.collections.new(COLLECTION_NAME)
    scene.collection.children.link(collection)
for obj in list(collection.objects):
    bpy.data.objects.remove(obj, do_unlink=True)

def material(name, color, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return mat

MAT_DARK = material("MAT_ArchDetail_Dark", COLORS["dark"], 0.25)
MAT_METAL = material("MAT_ArchDetail_Metal", COLORS["metal"], 0.55)
MAT_ACCENT = material("MAT_ArchDetail_Accent", COLORS["accent"], 0.45)
MAT_GLASS = material("MAT_ArchDetail_Glass", COLORS["glass"], 0.2, 0.24)

def add_box(name, location, dimensions, mat, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = PREFIX + name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    if bevel:
        mod = obj.modifiers.new("Small_Edge_Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)
    return obj

# Vertical fins provide a clean modern rhythm without changing the core shell.
for i, x in enumerate((-25.4, -20.0, -14.0, -8.0, 8.0, 14.0, 20.0, 25.4)):
    add_box("FRONT_FIN_%02d" % (i + 1),
            (x, -19.18, 6.3), (0.18, 0.20, 12.3), MAT_METAL, 0.025)

# Slim mullions over each front glazing panel, on all three levels.
window_centers = (-23, -17, -11, 13, 19)
for floor in range(FLOORS):
    z0 = floor * FLOOR_H
    for i, x in enumerate(window_centers):
        for side, dx in (("L", -1.38), ("R", 1.38)):
            add_box("WINDOW_%d_%02d_MULLION_%s" % (floor + 1, i + 1, side),
                    (x + dx, -19.105, z0 + 2.25), (0.075, 0.08, 1.55), MAT_DARK)
        add_box("WINDOW_%d_%02d_SILL" % (floor + 1, i + 1),
                (x, -19.12, z0 + 1.47), (3.05, 0.12, 0.10), MAT_METAL)
        add_box("WINDOW_%d_%02d_HEAD" % (floor + 1, i + 1),
                (x, -19.12, z0 + 3.03), (3.05, 0.12, 0.10), MAT_METAL)

# Floor bands articulate the façade; intentionally kept thin and low-poly.
for floor in (1, 2):
    z = floor * FLOOR_H - 0.12
    add_box("FRONT_FLOOR_BAND_%d" % floor,
            (0, -19.18, z), (53.5, 0.18, 0.16), MAT_DARK)
    add_box("FRONT_BAND_ACCENT_%d" % floor,
            (0, -19.285, z - 0.08), (53.0, 0.035, 0.035), MAT_ACCENT)

# Entrance canopy fascia and a narrow accent strip at the leading edge.
add_box("CANOPY_FRONT_FASCIA", (0, -25.02, 4.0), (23.2, 0.22, 0.72), MAT_DARK, 0.035)
add_box("CANOPY_ACCENT_STRIP", (0, -25.145, 3.72), (22.8, 0.035, 0.055), MAT_ACCENT)
add_box("CANOPY_UNDERSIDE_PANEL", (0, -22.0, 3.755), (22.6, 5.5, 0.06), MAT_METAL)

# Simple base plinth and corner caps keep the building visually grounded.
add_box("FRONT_BASE_PLINTH", (0, -19.17, 0.20), (53.7, 0.18, 0.32), MAT_DARK)
for i, x in enumerate((-26.4, 26.4)):
    add_box("FRONT_CORNER_CAP_%d" % (i + 1), (x, -19.18, 6.2),
            (0.45, 0.28, 12.0), MAT_DARK, 0.025)

print("Stage 10 architectural details generated in " + COLLECTION_NAME)
print("Inspect alignment, wall clearance, window intersections, and emblem/sign overlap before export.")
