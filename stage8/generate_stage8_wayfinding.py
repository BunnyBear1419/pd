"""Stage 8 — editable wayfinding and department signage for the PDHQ blockout.

Run after Stages 2–7 in Blender. All signage is schematic Blender text and
simple backing meshes. Adjust BRAND and SIGN_LAYOUT before running. Placement
coordinates are intentionally editable because the final room geometry must be
inspected in Blender before export. This is not a final Sollumz-ready asset pack.
"""
import bpy

PREFIX = "PDHQ_"
COLLECTION_NAME = "PDHQ_WAYFINDING_SIGNS"

# Reuse the agency identity used by Stage 7. Keep these values synchronized.
BRAND = {
    "short_name": "LSPD",
    "agency_name": "LOS SANTOS POLICE DEPARTMENT",
    "primary_color": (0.055, 0.12, 0.20, 1.0),
    "accent_color": (0.82, 0.66, 0.25, 1.0),
    "text_color": (0.96, 0.97, 0.98, 1.0),
}

# Positions are editable placeholders in the Stage 2 coordinate system.
# Plaques face toward the room/corridor from their mounting wall.
# rotation is Euler radians. The default faces toward -Y.
SIGN_LAYOUT = {
    "room_plaques": [
        {"label": "RECEPTION", "location": (-9.0, -17.5, 2.25), "rotation": (1.5707963, 0.0, 0.0)},
        {"label": "BOOKING", "location": (-3.0, -17.5, 2.25), "rotation": (1.5707963, 0.0, 0.0)},
        {"label": "DISPATCH", "location": (7.0, -17.5, 2.25), "rotation": (1.5707963, 0.0, 0.0)},
        {"label": "EVIDENCE", "location": (13.0, -17.5, 2.25), "rotation": (1.5707963, 0.0, 0.0)},
        {"label": "INTERVIEW ROOMS", "location": (-9.0, -5.0, 2.25), "rotation": (1.5707963, 0.0, 0.0)},
        {"label": "DETECTIVES", "location": (3.0, -5.0, 2.25), "rotation": (1.5707963, 0.0, 0.0)},
        {"label": "ARMORY", "location": (13.0, -5.0, 2.25), "rotation": (1.5707963, 0.0, 0.0)},
        {"label": "LOCKER ROOMS", "location": (-9.0, 8.0, 5.85), "rotation": (1.5707963, 0.0, 0.0)},
        {"label": "SWAT BRIEFING", "location": (3.0, 8.0, 5.85), "rotation": (1.5707963, 0.0, 0.0)},
        {"label": "ROOF ACCESS", "location": (13.0, 8.0, 8.95), "rotation": (1.5707963, 0.0, 0.0)},
    ],
    "garage_signs": [
        {"label": "SECURE VEHICLE BAY", "location": (18.0, -12.0, 3.0), "rotation": (1.5707963, 0.0, 0.0)},
        {"label": "AUTHORIZED VEHICLES ONLY", "location": (18.0, -4.0, 3.0), "rotation": (1.5707963, 0.0, 0.0)},
    ],
    "floor_directories": [
        {"label": "FLOOR 1  |  PUBLIC SERVICES", "location": (0.0, -16.8, 2.6), "rotation": (1.5707963, 0.0, 0.0)},
        {"label": "FLOOR 2  |  OPERATIONS", "location": (0.0, 0.0, 5.6), "rotation": (1.5707963, 0.0, 0.0)},
        {"label": "FLOOR 3  |  SPECIAL OPERATIONS", "location": (0.0, 0.0, 8.6), "rotation": (1.5707963, 0.0, 0.0)},
    ],
}

scene = bpy.context.scene
collection = bpy.data.collections.get(COLLECTION_NAME)
if collection is None:
    collection = bpy.data.collections.new(COLLECTION_NAME)
    scene.collection.children.link(collection)

# Safe reruns: only clear this script's own dedicated collection.
for obj in list(collection.objects):
    bpy.data.objects.remove(obj, do_unlink=True)

def material(name, color, metallic=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = 0.55
    return mat

MAT_BASE = material("MAT_Wayfinding_Base", BRAND["primary_color"], 0.15)
MAT_ACCENT = material("MAT_Wayfinding_Accent", BRAND["accent_color"], 0.25)
MAT_TEXT = material("MAT_Wayfinding_Text", BRAND["text_color"])

def register(obj):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)
    return obj

def add_box(name, location, dimensions, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = PREFIX + "WAYFINDING_" + name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    return register(obj)

def add_text(name, body, location, size, rotation, mat):
    curve = bpy.data.curves.new(PREFIX + "WAYFINDING_TEXT_" + name, "FONT")
    curve.body = body
    curve.size = size
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.extrude = 0.003
    obj = bpy.data.objects.new(PREFIX + "WAYFINDING_TEXT_" + name, curve)
    collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = rotation
    obj.data.materials.append(mat)
    return obj

def add_sign(group, index, item, width, height, text_size):
    x, y, z = item["location"]
    rx, ry, rz = item["rotation"]
    # Assumes wall-mounted plaque's broad face is in the X/Z plane.
    name = "%s_%02d" % (group.upper(), index + 1)
    add_box(name + "_BACKPLATE", (x, y, z), (width, 0.10, height), MAT_BASE)
    add_box(name + "_ACCENT", (x, y - 0.06, z - height * 0.38),
            (width * 0.88, 0.025, 0.035), MAT_ACCENT)
    add_text(name, item["label"], (x, y - 0.065, z + height * 0.10),
             text_size, (rx, ry, rz), MAT_TEXT)

for i, item in enumerate(SIGN_LAYOUT["room_plaques"]):
    add_sign("ROOM", i, item, 3.2, 0.48, 0.22)
for i, item in enumerate(SIGN_LAYOUT["garage_signs"]):
    add_sign("GARAGE", i, item, 4.4, 0.62, 0.25)
for i, item in enumerate(SIGN_LAYOUT["floor_directories"]):
    add_sign("DIRECTORY", i, item, 5.6, 0.72, 0.25)

print("Stage 8 wayfinding signage generated for: " + BRAND["agency_name"])
print("Inspect and adjust SIGN_LAYOUT placements in Blender before export.")
