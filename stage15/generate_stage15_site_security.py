"""Stage 15: perimeter security, site landscape, lighting and drainage guides.

Visual planning guides only. Run inside Blender after earlier stages are loaded.
Reruns replace only PDHQ_SITE_SECURITY_LANDSCAPE_GUIDES.
"""
import bpy

CONFIG = {
    # Approximate site guide bounds, deliberately adjustable.
    "site_min_x": -36.0,
    "site_max_x": 36.0,
    "site_front_y": -48.0,
    "site_rear_y": 27.0,
    "fence_height": 2.2,
    "fence_post_spacing": 3.0,
    "fence_post_size": 0.16,
    "fence_rail_depth": 0.10,
    "front_gate_center_x": 0.0,
    "front_gate_width": 16.0,
    "service_gate_center_x": -20.0,
    "service_gate_width": 5.0,
    "light_spacing": 14.0,
    "landscape_bed_depth": 2.0,
    "drainage_guide_count": 5,
    "show_perimeter_fence": True,
    "show_lighting_guides": True,
    "show_landscape_beds": True,
    "show_drainage_guides": True,
}

COLLECTION_NAME = "PDHQ_SITE_SECURITY_LANDSCAPE_GUIDES"


def collection_get(name):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    else:
        for obj in list(col.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
    return col


def move_to(obj, col):
    for previous in list(obj.users_collection):
        previous.objects.unlink(obj)
    col.objects.link(obj)


def get_material(name, color):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    return mat


def make_box(name, loc, dims, mat, col):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    move_to(obj, col)
    return obj


def make_cylinder(name, loc, radius, depth, mat, col, vertices=12):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=depth, location=loc
    )
    obj = bpy.context.object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    move_to(obj, col)
    return obj


def make_label(name, body, loc, size, mat, col):
    curve = bpy.data.curves.new(name + "_Text", type="FONT")
    curve.body = body
    curve.size = size
    curve.align_x = "LEFT"
    curve.align_y = "CENTER"
    obj = bpy.data.objects.new(name, curve)
    obj.location = loc
    if mat:
        curve.materials.append(mat)
    col.objects.link(obj)
    return obj


def fence_line(prefix, x1, y1, x2, y2, gate_center, gate_width, horizontal,
               post_mat, rail_mat, col):
    cfg = CONFIG
    length = abs(x2 - x1) if horizontal else abs(y2 - y1)
    count = max(1, int(length / cfg["fence_post_spacing"]))
    for i in range(count + 1):
        t = i / count
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t
        along = x if horizontal else y
        if gate_center is not None and abs(along - gate_center) <= gate_width / 2:
            continue
        make_box(f"{prefix}_Post_{i+1:02d}", (x, y, cfg["fence_height"] / 2),
                 (cfg["fence_post_size"], cfg["fence_post_size"], cfg["fence_height"]),
                 post_mat, col)
    # Rails are split around a gate opening on horizontal sides; side rails are continuous.
    segments = [(x1, y1, x2, y2)]
    if horizontal and gate_center is not None and gate_width > 0:
        left_end = gate_center - gate_width / 2
        right_start = gate_center + gate_width / 2
        segments = []
        if x1 < left_end:
            segments.append((x1, y1, left_end, y2))
        if right_start < x2:
            segments.append((right_start, y1, x2, y2))
    for j, (ax, ay, bx, by) in enumerate(segments):
        length_seg = abs(bx - ax) if horizontal else abs(by - ay)
        center = ((ax + bx) / 2, (ay + by) / 2, cfg["fence_height"] * 0.66)
        dims = (length_seg, cfg["fence_rail_depth"], 0.10) if horizontal else (
            cfg["fence_rail_depth"], length_seg, 0.10)
        make_box(f"{prefix}_Upper_Rail_{j+1}", center, dims, rail_mat, col)
        center_low = (center[0], center[1], cfg["fence_height"] * 0.34)
        make_box(f"{prefix}_Lower_Rail_{j+1}", center_low, dims, rail_mat, col)


def main():
    cfg = CONFIG
    col = collection_get(COLLECTION_NAME)
    fence_mat = get_material("PDHQ_Guide_Fence_Grey", (0.30, 0.34, 0.38))
    rail_mat = get_material("PDHQ_Guide_Fence_Rails", (0.48, 0.52, 0.56))
    security_mat = get_material("PDHQ_Guide_Security_Amber", (1.0, 0.48, 0.06))
    lighting_mat = get_material("PDHQ_Guide_Lighting_Purple", (0.62, 0.30, 0.95))
    landscape_mat = get_material("PDHQ_Guide_Landscape_Green", (0.18, 0.55, 0.25))
    drainage_mat = get_material("PDHQ_Guide_Drainage_Cyan", (0.05, 0.72, 0.82))
    text_mat = get_material("PDHQ_Guide_Site_Label_White", (1.0, 1.0, 1.0))

    xmin, xmax = cfg["site_min_x"], cfg["site_max_x"]
    yfront, yrear = cfg["site_front_y"], cfg["site_rear_y"]
    front_gate = cfg["front_gate_center_x"]
    front_width = cfg["front_gate_width"]
    service_gate = cfg["service_gate_center_x"]
    service_width = cfg["service_gate_width"]

    if cfg["show_perimeter_fence"]:
        fence_line("Front_Perimeter", xmin, yfront, xmax, yfront,
                   front_gate, front_width, True, fence_mat, rail_mat, col)
        fence_line("Rear_Perimeter", xmin, yrear, xmax, yrear,
                   None, 0, True, fence_mat, rail_mat, col)
        fence_line("West_Perimeter", xmin, yfront, xmin, yrear,
                   None, 0, False, fence_mat, rail_mat, col)
        fence_line("East_Perimeter", xmax, yfront, xmax, yrear,
                   None, 0, False, fence_mat, rail_mat, col)
        # Provisional gate leaves are shown as ground-level guides only.
        make_box("PROVISIONAL_Main_Security_Gate_Zone",
                 (front_gate, yfront, 0.06), (front_width, 1.0, 0.12),
                 security_mat, col)
        make_label("Label_Main_Gate", "MAIN VEHICLE ENTRY - VERIFY SITE ACCESS",
                   (front_gate - front_width / 2, yfront - 2.0, 0.16), 0.45,
                   text_mat, col)
        make_box("PROVISIONAL_Service_Security_Gate_Zone",
                 (service_gate, yfront, 0.06), (service_width, 1.0, 0.12),
                 security_mat, col)
        make_label("Label_Service_Gate", "SERVICE GATE - PROVISIONAL",
                   (service_gate - service_width / 2, yfront - 3.0, 0.16),
                   0.40, text_mat, col)

    if cfg["show_lighting_guides"]:
        index = 1
        x = xmin + cfg["light_spacing"] / 2
        while x < xmax:
            for y in (yfront + 5.0, yrear - 5.0):
                make_cylinder(f"Site_Light_Pole_{index:02d}",
                              (x, y, 2.0), 0.10, 4.0, lighting_mat, col)
                make_box(f"Site_Light_Base_{index:02d}",
                         (x, y, 0.15), (0.55, 0.55, 0.3), lighting_mat, col)
                index += 1
            x += cfg["light_spacing"]
        make_label("Label_Lighting_Guides", "EXTERIOR LIGHTING LOCATIONS - AIM / GLARE REVIEW",
                   (xmin + 1.0, yrear - 2.0, 0.16), 0.42, text_mat, col)

    if cfg["show_landscape_beds"]:
        bed_depth = cfg["landscape_bed_depth"]
        # Keep planting guides along the perimeter edges, away from assumed building core.
        for side, x in (("West", xmin + 1.5), ("East", xmax - 1.5)):
            make_box(f"Landscape_Bed_{side}", (x, (yfront + yrear) / 2, 0.04),
                     (2.0, max(1.0, yrear - yfront - 10.0), 0.08),
                     landscape_mat, col)
        make_box("Landscape_Bed_Rear", (0, yrear - bed_depth / 2, 0.04),
                 (max(1.0, xmax - xmin - 8.0), bed_depth, 0.08),
                 landscape_mat, col)
        make_label("Label_Landscape", "LANDSCAPE ZONES - KEEP SIGHTLINES / ACCESS CLEAR",
                   (xmin + 2.0, yrear - 5.0, 0.16), 0.42, text_mat, col)

    if cfg["show_drainage_guides"]:
        count = max(1, int(cfg["drainage_guide_count"]))
        for i in range(count):
            x = xmin + 6.0 + i * ((xmax - xmin - 12.0) / max(1, count - 1))
            make_box(f"Drainage_Channel_Guide_{i+1:02d}",
                     (x, (yfront + yrear) / 2, 0.03),
                     (0.16, max(1.0, yrear - yfront - 4.0), 0.06),
                     drainage_mat, col)
        make_label("Label_Drainage", "DRAINAGE / GRADING REVIEW - NOT ENGINEERED",
                   (xmin + 1.0, yfront + 5.0, 0.18), 0.40, text_mat, col)

    print(f"Stage 15 complete: {len(col.objects)} site planning guide objects.")
    print("Verify site bounds, gate openings, building clearance, lighting and drainage in Blender.")


if __name__ == "__main__":
    main()
