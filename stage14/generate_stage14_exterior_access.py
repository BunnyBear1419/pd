"""Stage 14: generate adjustable exterior access and circulation guides in Blender.

Run inside Blender's Scripting workspace after the Stage 2 blockout is loaded.
All generated objects are visual planning guides, not production collision or map assets.
Reruns replace only the PDHQ_EXTERIOR_ACCESS_GUIDES collection.
"""
import bpy
from mathutils import Vector

CONFIG = {
    "front_y": -19.0,
    "front_entrance_center_x": 0.0,
    "entrance_width": 15.0,
    "dropoff_center_x": 0.0,
    "dropoff_y": -31.0,
    "dropoff_width": 18.0,
    "public_path_width": 2.0,
    "public_path_end_y": -42.0,
    # Provisional until the actual garage opening is confirmed in the scene.
    "garage_entry_center_x": 17.0,
    "garage_entry_y": 2.0,
    "garage_opening_width": 7.0,
    "garage_approach_end_y": -12.0,
    "service_center_x": -20.0,
    "service_y": -6.0,
    "service_width": 5.0,
    "guide_height": 0.08,
    "bollard_spacing": 2.0,
    "bollard_radius": 0.16,
    "bollard_height": 1.0,
    "show_turning_envelope": True,
}

COLLECTION_NAME = "PDHQ_EXTERIOR_ACCESS_GUIDES"


def get_collection(name):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    else:
        for obj in list(collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
    return collection


def move_to_collection(obj, collection):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)


def material(name, color):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    return mat


def box(name, location, dimensions, mat, collection, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    if bevel > 0:
        mod = obj.modifiers.new("Guide edge softening", "BEVEL")
        mod.width = bevel
        mod.segments = 1
    move_to_collection(obj, collection)
    return obj


def cylinder(name, location, radius, depth, mat, collection, vertices=12):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=depth, location=location
    )
    obj = bpy.context.object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    move_to_collection(obj, collection)
    return obj


def label(name, body, location, size, mat, collection):
    curve = bpy.data.curves.new(name + "_Text", type="FONT")
    curve.body = body
    curve.size = size
    curve.extrude = 0.0
    curve.align_x = "LEFT"
    curve.align_y = "CENTER"
    obj = bpy.data.objects.new(name, curve)
    obj.location = location
    if mat:
        curve.materials.append(mat)
    collection.objects.link(obj)
    return obj


def marker(name, x, y, width, depth, mat, collection, z=0.05):
    return box(name, (x, y, z), (width, depth, CONFIG["guide_height"]), mat, collection)


def make_bollard_row(prefix, x1, x2, y, spacing, mat, collection):
    x = x1
    index = 1
    while x <= x2 + 0.001:
        cylinder(
            f"{prefix}_{index:02d}",
            (x, y, CONFIG["bollard_height"] / 2),
            CONFIG["bollard_radius"],
            CONFIG["bollard_height"],
            mat,
            collection,
        )
        x += spacing
        index += 1


def main():
    cfg = CONFIG
    collection = get_collection(COLLECTION_NAME)
    public = material("PDHQ_Guide_Public_Cyan", (0.08, 0.72, 0.95))
    vehicle = material("PDHQ_Guide_Vehicle_Amber", (1.0, 0.55, 0.08))
    emergency = material("PDHQ_Guide_Emergency_Red", (0.9, 0.12, 0.12))
    pedestrian = material("PDHQ_Guide_Pedestrian_Green", (0.15, 0.8, 0.36))
    barrier = material("PDHQ_Guide_Barrier_White", (0.86, 0.88, 0.9))
    text_mat = material("PDHQ_Guide_Label_White", (1.0, 1.0, 1.0))

    # Main public approach, aligned to the Stage 2 central entrance gap.
    px = cfg["front_entrance_center_x"]
    path_mid_y = (cfg["front_y"] + cfg["public_path_end_y"]) / 2
    marker("Public_Pedestrian_Approach", px, path_mid_y,
           cfg["public_path_width"], abs(cfg["public_path_end_y"] - cfg["front_y"]),
           public, collection)
    marker("Accessible_Entrance_Landing", px, cfg["front_y"] - 0.8,
           cfg["entrance_width"], 2.0, pedestrian, collection)
    label("Label_Public_Entrance", "PUBLIC / ACCESSIBLE ENTRANCE",
          (-cfg["entrance_width"] / 2, cfg["front_y"] - 3.0, 0.16), 0.65,
          text_mat, collection)
    for i, y in enumerate((cfg["front_y"] - 4.5, cfg["front_y"] - 8.0,
                           cfg["front_y"] - 11.5)):
        marker(f"Pedestrian_Crossing_Band_{i+1}", px, y,
               cfg["dropoff_width"], 0.22, pedestrian, collection)

    # Drop-off guides.
    marker("Dropoff_Zone_Center", cfg["dropoff_center_x"], cfg["dropoff_y"],
           cfg["dropoff_width"], 5.0, vehicle, collection)
    marker("Dropoff_Edge_Left", cfg["dropoff_center_x"] - cfg["dropoff_width"]/2,
           cfg["dropoff_y"], 0.16, 5.0, barrier, collection)
    marker("Dropoff_Edge_Right", cfg["dropoff_center_x"] + cfg["dropoff_width"]/2,
           cfg["dropoff_y"], 0.16, 5.0, barrier, collection)
    label("Label_Dropoff", "DROP-OFF / KEEP CLEAR",
          (cfg["dropoff_center_x"] - cfg["dropoff_width"]/2, cfg["dropoff_y"] - 3.2, 0.16),
          0.55, text_mat, collection)

    # Bollards leave the central entrance clear.
    half_entry = cfg["entrance_width"] / 2
    bollard_y = cfg["front_y"] - 1.3
    make_bollard_row("Bollards_Left_Frontage", -cfg["dropoff_width"]/2,
                     -half_entry - 1.0, bollard_y, cfg["bollard_spacing"],
                     vehicle, collection)
    make_bollard_row("Bollards_Right_Frontage", half_entry + 1.0,
                     cfg["dropoff_width"]/2, bollard_y, cfg["bollard_spacing"],
                     vehicle, collection)

    # Garage access is intentionally adjustable; verify its opening first.
    gx, gy, gw = cfg["garage_entry_center_x"], cfg["garage_entry_y"], cfg["garage_opening_width"]
    marker("PROVISIONAL_Garage_Entry_Threshold", gx, gy, gw, 1.0, vehicle, collection)
    marker("PROVISIONAL_Garage_Approach", gx,
           (gy + cfg["garage_approach_end_y"]) / 2, gw + 4.0,
           abs(gy - cfg["garage_approach_end_y"]), vehicle, collection)
    marker("PROVISIONAL_Garage_Exit_Staging", gx + gw + 4.0, gy - 7.0,
           5.0, 7.0, emergency, collection)
    label("Label_Provisional_Garage_Access", "VERIFY GARAGE OPENING",
          (gx - gw/2, gy - 2.0, 0.18), 0.45, text_mat, collection)

    # Service / delivery approach is also provisional.
    sx, sy, sw = cfg["service_center_x"], cfg["service_y"], cfg["service_width"]
    marker("PROVISIONAL_Service_Access_Threshold", sx, sy, sw, 1.0, emergency, collection)
    service_end_y = cfg["public_path_end_y"] + 5.0
    marker("PROVISIONAL_Service_Approach", sx,
           (sy + service_end_y) / 2, sw + 3.0,
           abs(sy - service_end_y), emergency, collection)
    label("Label_Service_Access", "SERVICE / DELIVERIES",
          (sx - sw/2, sy - 2.0, 0.16), 0.45, text_mat, collection)

    marker("Emergency_Clear_Access_Lane", -14.0, -29.0, 5.0, 24.0,
           emergency, collection)
    label("Label_Emergency_Access", "EMERGENCY ACCESS - KEEP CLEAR",
          (-16.5, -41.5, 0.16), 0.42, text_mat, collection)
    if cfg["show_turning_envelope"]:
        marker("Vehicle_Turning_Review_Envelope", 15.0, -24.0, 18.0, 12.0,
               vehicle, collection)
        label("Label_Turning_Review", "TURNING / OBSTRUCTION REVIEW",
              (6.0, -31.0, 0.16), 0.42, text_mat, collection)

    print(f"Stage 14 complete: {len(collection.objects)} exterior access guide objects.")
    print("Inspect provisional garage/service positions and frontage clearances in Blender.")


if __name__ == "__main__":
    main()
