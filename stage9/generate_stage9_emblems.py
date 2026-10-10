"""Stage 9 — configurable agency crest and lobby badge.

Run in Blender after the Stage 2 blockout. The emblem uses editable mesh geometry
and Blender text, not third-party logos or final UV-mapped game textures.
Coordinates and dimensions are provisional; inspect before export.
"""
import math
import bpy

COLLECTION_NAME = "PDHQ_AGENCY_EMBLEMS"
BRAND = {
    "agency_name": "LOS SANTOS POLICE DEPARTMENT",
    "short_name": "LSPD",
    "subtitle": "PROTECT • SERVE • UNITE",
    "primary_color": (0.055, 0.12, 0.20, 1.0),
    "accent_color": (0.82, 0.66, 0.25, 1.0),
    "text_color": (0.96, 0.97, 0.98, 1.0),
    "show_subtitle": True,
}
# Front faces point toward -Y. Move these anchors to match the final architecture.
EMBLEM_LAYOUT = {
    "exterior": {"center": (0.0, -19.25, 5.0), "scale": 1.0},
    "lobby": {"center": (0.0, -17.15, 2.15), "scale": 0.48},
}

scene = bpy.context.scene
collection = bpy.data.collections.get(COLLECTION_NAME)
if collection is None:
    collection = bpy.data.collections.new(COLLECTION_NAME)
    scene.collection.children.link(collection)
for obj in list(collection.objects):
    bpy.data.objects.remove(obj, do_unlink=True)

def register(obj):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)
    return obj

def make_material(name, color, metallic=0.0, roughness=0.48):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return mat

MAT_PRIMARY = make_material("MAT_AgencyEmblem_Primary", BRAND["primary_color"], 0.28)
MAT_ACCENT = make_material("MAT_AgencyEmblem_Accent", BRAND["accent_color"], 0.62)
MAT_TEXT = make_material("MAT_AgencyEmblem_Text", BRAND["text_color"], 0.12)

def add_mesh(name, vertices, faces, material):
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(vertices, [], faces)
    mesh.materials.append(material)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    return obj

def add_shield(name, center, width, height, depth, material):
    x, y, z = center
    # Convex shield outline, laid out in the X/Z plane.
    outline = [
        (-0.50, 0.34), (-0.39, 0.50), (0.39, 0.50), (0.50, 0.34),
        (0.44, -0.10), (0.25, -0.37), (0.0, -0.50),
        (-0.25, -0.37), (-0.44, -0.10),
    ]
    front_y = y - depth / 2
    back_y = y + depth / 2
    verts = [(x + px * width, front_y, z + pz * height) for px, pz in outline]
    verts += [(x + px * width, back_y, z + pz * height) for px, pz in outline]
    n = len(outline)
    faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, j + n, i + n))
    return add_mesh(name, verts, faces, material)

def add_torus(name, center, major_radius, minor_radius, material):
    bpy.ops.mesh.primitive_torus_add(
        major_segments=48, minor_segments=8,
        location=center, major_radius=major_radius, minor_radius=minor_radius,
        rotation=(math.pi / 2, 0.0, 0.0),
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    return register(obj)

def add_text(name, body, location, size, material, align="CENTER"):
    curve = bpy.data.curves.new(name + "_CURVE", "FONT")
    curve.body = body
    curve.size = size
    curve.align_x = align
    curve.align_y = "CENTER"
    curve.extrude = 0.0015
    obj = bpy.data.objects.new(name, curve)
    collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (math.pi / 2, 0.0, 0.0)
    obj.data.materials.append(material)
    return obj

def add_emblem(kind, layout):
    cx, cy, cz = layout["center"]
    s = layout["scale"]
    prefix = "PDHQ_EMBLEM_" + kind.upper()
    add_shield(prefix + "_SHIELD", (cx, cy, cz), 1.5 * s, 1.75 * s, 0.12 * s, MAT_PRIMARY)
    add_shield(prefix + "_INNER", (cx, cy - 0.071 * s, cz + 0.015 * s),
               1.29 * s, 1.52 * s, 0.035 * s, MAT_ACCENT)
    add_shield(prefix + "_FIELD", (cx, cy - 0.094 * s, cz + 0.015 * s),
               1.20 * s, 1.43 * s, 0.025 * s, MAT_PRIMARY)
    add_torus(prefix + "_RING", (cx, cy - 0.12 * s, cz + 0.12 * s),
              0.36 * s, 0.025 * s, MAT_ACCENT)
    add_text(prefix + "_INITIALS", BRAND["short_name"],
             (cx, cy - 0.15 * s, cz + 0.13 * s), 0.24 * s, MAT_TEXT)
    add_text(prefix + "_AGENCY", BRAND["agency_name"],
             (cx, cy - 0.15 * s, cz - 0.32 * s), 0.075 * s, MAT_TEXT)
    if BRAND["show_subtitle"] and BRAND["subtitle"]:
        add_text(prefix + "_SUBTITLE", BRAND["subtitle"],
                 (cx, cy - 0.15 * s, cz - 0.46 * s), 0.052 * s, MAT_ACCENT)

add_emblem("EXTERIOR", EMBLEM_LAYOUT["exterior"])
add_emblem("LOBBY", EMBLEM_LAYOUT["lobby"])
print("Stage 9 agency emblems generated for: " + BRAND["agency_name"])
print("Inspect scale, orientation, wall clearance, text readability, and materials before export.")
