"""Stage 12 — door leaves and access-point visualization proxies.

Run after Stages 2–4 in the same Blender scene. Uses the current Stage 3
schematic door-gap coordinates; all door geometry is illustrative and nonfunctional.
"""
import bpy

COLLECTION_NAME = "PDHQ_DOOR_ACCESS_BLOCKOUT"
FLOOR_H = 4.2
DOOR_H = 2.05
DOOR_W = 0.84
PREFIX = "PDHQ_DOOR12_"
scene = bpy.context.scene

col = bpy.data.collections.get(COLLECTION_NAME)
if col is None:
    col = bpy.data.collections.new(COLLECTION_NAME)
    scene.collection.children.link(col)
for obj in list(col.objects):
    bpy.data.objects.remove(obj, do_unlink=True)

def mat(name, color, metallic=0.0, roughness=0.55):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return m

MAT_PUBLIC = mat("MAT_Door12_Public", (0.32, 0.38, 0.40), 0.18)
MAT_STAFF = mat("MAT_Door12_Staff", (0.16, 0.23, 0.26), 0.22)
MAT_SECURE = mat("MAT_Door12_Secure", (0.10, 0.13, 0.15), 0.38)
MAT_GLASS = mat("MAT_Door12_GlassProxy", (0.06, 0.20, 0.23), 0.12)
MAT_HARDWARE = mat("MAT_Door12_Hardware", (0.72, 0.55, 0.24), 0.65)
MAT_THRESHOLD = mat("MAT_Door12_Threshold", (0.85, 0.58, 0.12), 0.25)

def box(name, loc, dims, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = PREFIX + name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    if bevel:
        mod = obj.modifiers.new("DoorProxy_Edge", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)
    return obj

def door_x(name, x, y, z, kind):
    material = MAT_PUBLIC if kind == "PUBLIC" else MAT_STAFF if kind == "STAFF" else MAT_SECURE
    box(name+"_LEAF", (x, y, z + DOOR_H/2), (DOOR_W, 0.065, DOOR_H), material, 0.012)
    # Narrow vision-light proxy on staff/security doors.
    if kind != "PUBLIC":
        box(name+"_VISION", (x, y - 0.037, z + 1.48), (0.24, 0.012, 0.34), MAT_GLASS, 0.004)
    box(name+"_HANDLE", (x + DOOR_W*0.32, y - 0.055, z + 1.02), (0.035, 0.035, 0.16), MAT_HARDWARE, 0.008)
    box(name+"_THRESHOLD", (x, y, z + 0.025), (1.02, 0.22, 0.05), MAT_THRESHOLD)

def door_y(name, x, y, z, kind):
    material = MAT_PUBLIC if kind == "PUBLIC" else MAT_STAFF if kind == "STAFF" else MAT_SECURE
    box(name+"_LEAF", (x, y, z + DOOR_H/2), (0.065, DOOR_W, DOOR_H), material, 0.012)
    if kind != "PUBLIC":
        box(name+"_VISION", (x - 0.037, y, z + 1.48), (0.012, 0.24, 0.34), MAT_GLASS, 0.004)
    box(name+"_HANDLE", (x - 0.055, y + DOOR_W*0.32, z + 1.02), (0.035, 0.035, 0.16), MAT_HARDWARE, 0.008)
    box(name+"_THRESHOLD", (x, y, z + 0.025), (0.22, 1.02, 0.05), MAT_THRESHOLD)

# Door panels are centered in the existing Stage 3 corridor-wall gaps.
# The opening centres and dimensions remain provisional until inspected in Blender.
for floor in range(3):
    z = floor * FLOOR_H
    for wall, y in (("N", 2.8), ("S", -2.8)):
        for i, x in enumerate((-20, -10, 0, 10, 20)):
            if floor == 0 and wall == "S" and x == -20:
                kind = "PUBLIC"
            elif floor == 0 and wall == "N" and x in (10, 20):
                kind = "SECURE"
            elif floor == 1 and wall == "N" and x in (-20, -10):
                kind = "SECURE"
            else:
                kind = "STAFF"
            door_x("F%d_CORRIDOR_%s_%02d_%s" % (floor+1, wall, i+1, kind),
                   x, y, z, kind)

    # Doors in the four side partition lines; these align with Stage 3 openings.
    for i, x in enumerate((-16, -5, 6, 17)):
        for j, y in enumerate((-12, -7)):
            kind = "SECURE" if floor == 0 and x >= 6 else "STAFF"
            door_y("F%d_FRONT_DIV_%02d_%02d_%s" % (floor+1, i+1, j+1, kind),
                   x, y, z, kind)
        for j, y in enumerate((7, 12)):
            kind = "SECURE" if (floor == 1 and x <= -12) or (floor == 0 and x >= 6) else "STAFF"
            door_y("F%d_REAR_DIV_%02d_%02d_%s" % (floor+1, i+1, j+1, kind),
                   x, y, z, kind)

# Access-reader props at a few illustrative restricted entrances. These are
# visual only; no keycard, job, or door-lock functionality is implemented.
for name, loc in [
    ("F1_HOLDING_READER", (6.08, 8.0, 1.35)),
    ("F1_SECURE_STORAGE_READER", (17.08, 10.0, 1.35)),
    ("F2_EVIDENCE_READER", (-15.92, 10.0, FLOOR_H + 1.35)),
    ("F2_ARMORY_READER", (-15.92, 7.0, FLOOR_H + 1.35)),
    ("F3_ROOF_ACCESS_READER", (22.0, -2.2, 2*FLOOR_H + 1.35)),
]:
    box(name+"_READER_BODY", loc, (0.09, 0.055, 0.20), MAT_SECURE, 0.008)
    box(name+"_READER_LED", (loc[0], loc[1]-0.031, loc[2]+0.045),
        (0.025, 0.012, 0.025), MAT_HARDWARE, 0.004)

print("Stage 12 door/access proxies generated in " + COLLECTION_NAME)
print("Visual blockout only: inspect door alignment, swing/clearance, access-reader placement, and all openings in Blender.")
