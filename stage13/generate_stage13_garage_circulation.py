"""Stage 13 — garage circulation and vehicle-clearance review guides.

Run after Stages 2–4 in the same Blender scene. Adds lightweight floor markings
and review volumes in a separate collection; it does not move or delete prior assets.
"""
import bpy

COLLECTION_NAME = "PDHQ_GARAGE_CIRCULATION_GUIDES"
PREFIX = "PDHQ_GARAGE13_"
scene = bpy.context.scene
col = bpy.data.collections.get(COLLECTION_NAME)
if col is None:
    col = bpy.data.collections.new(COLLECTION_NAME)
    scene.collection.children.link(col)
for obj in list(col.objects):
    bpy.data.objects.remove(obj, do_unlink=True)

def material(name, color, roughness=0.75):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
    return mat

MAT_LINE = material("MAT_Garage13_SafetyLine", (0.90, 0.62, 0.10))
MAT_WALK = material("MAT_Garage13_PedestrianPath", (0.12, 0.42, 0.43))
MAT_REVIEW = material("MAT_Garage13_ReviewVolume", (0.95, 0.22, 0.08))
MAT_NEUTRAL = material("MAT_Garage13_ReviewNeutral", (0.28, 0.32, 0.34))

def box(name, loc, dims, mat, bevel=0.0, wire=False):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = PREFIX + name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    if wire:
        obj.display_type = "WIRE"
        obj.show_in_front = True
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)
    return obj

# Three nominal vehicle bays aligned to Stage 4 clearance proxies. Floor paint
# sits low and should be reviewed against the actual garage slab in Blender.
bay_centres = (-9.0, 0.0, 9.0)
for idx, x in enumerate(bay_centres, start=1):
    box("BAY_%02d_LEFT_LINE" % idx, (x - 1.55, 7.45, 0.315), (0.08, 6.1, 0.025), MAT_LINE)
    box("BAY_%02d_RIGHT_LINE" % idx, (x + 1.55, 7.45, 0.315), (0.08, 6.1, 0.025), MAT_LINE)
    box("BAY_%02d_REAR_STOP" % idx, (x, 4.42, 0.315), (3.1, 0.08, 0.025), MAT_LINE)
    # A small flat marker near the front of each bay; not a literal arrow mesh.
    box("BAY_%02d_FRONT_MARKER" % idx, (x, 10.15, 0.315), (0.42, 0.08, 0.025), MAT_LINE)

# Central drive aisle guide: wireframe bounds make it easy to inspect vehicle turns.
box("DRIVE_AISLE_REVIEW_VOLUME", (0.0, 15.2, 1.1), (22.0, 3.4, 2.2),
    MAT_REVIEW, wire=True)
# Pedestrian path is a separate, flat strip along the eastern edge of the guide area.
box("PEDESTRIAN_PATH_STRIP", (12.1, 12.0, 0.32), (1.0, 10.0, 0.035), MAT_WALK)
for i in range(5):
    box("PEDESTRIAN_DASH_%02d" % (i+1), (12.1, 8.2 + i*1.8, 0.345),
        (0.12, 0.65, 0.02), MAT_LINE)

# Garage-to-booking transfer route is an abstract floor marking, not an actual
# access-controlled corridor. Confirm the room boundaries before keeping it.
for i, y in enumerate((-1.4, -0.2, 1.0), start=1):
    box("TRANSFER_ROUTE_DASH_%02d" % i, (-12.0, y, 0.315), (0.12, 0.42, 0.025), MAT_WALK)

# Review volume around the existing Stage 4 vehicle guide footprints.
for idx, x in enumerate(bay_centres, start=1):
    obj = box("VEHICLE_CLEARANCE_REVIEW_%02d" % idx, (x, 10.5, 0.95),
              (2.6, 5.8, 1.7), MAT_NEUTRAL, wire=True)
    obj["purpose"] = "Review only; compare with Stage 4 vehicle clearance proxy"
    obj["vehicle_width_m"] = 2.6
    obj["vehicle_length_m"] = 5.8

print("Stage 13 garage circulation guides created in " + COLLECTION_NAME)
print("Review bay markings, turning space, pedestrian path, and door/corridor clearance in Blender.")
