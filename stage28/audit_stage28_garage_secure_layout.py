"""Stage 28 — garage and secure ground-floor layout screening.

Run inside Blender after the Stage 2–4 geometry and Stage 13–14 guides exist.
Creates review envelopes and an advisory AABB report. It does not repair geometry,
calculate a true vehicle swept path, or certify access/security.
"""
import json
import bpy
from mathutils import Vector

COLLECTION = "PDHQ_STAGE28_GARAGE_SECURE_REVIEW"
REPORT_NAME = "PDHQ_STAGE28_GARAGE_SECURE_REPORT"
PREFIX = "PDHQ_STAGE28_"

scene = bpy.context.scene
col = bpy.data.collections.get(COLLECTION)
if col is None:
    col = bpy.data.collections.new(COLLECTION)
    scene.collection.children.link(col)
else:
    for obj in list(col.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

def get_material(name, color):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF") if mat.node_tree else None
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.8
    return mat

MAT_VEHICLE = get_material("MAT_Stage28_VehicleReview", (0.95, 0.22, 0.08))
MAT_PEDESTRIAN = get_material("MAT_Stage28_PedestrianReview", (0.08, 0.55, 0.50))
MAT_TRANSFER = get_material("MAT_Stage28_SecureTransferReview", (0.95, 0.62, 0.10))

def make_box(name, loc, dims, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = PREFIX + name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.display_type = "WIRE"
    obj.show_in_front = True
    obj.data.materials.append(mat)
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)
    obj["review_only"] = True
    return obj

# Provisional envelopes in the current schematic coordinate system. Confirm the
# actual garage door and secure booking-transfer route before treating as final.
routes = [
    {"name": "GARAGE_DRIVE_AISLE", "loc": (0.0, 15.2, 1.1), "dims": (22.0, 3.4, 2.2), "kind": "vehicle"},
    {"name": "GARAGE_ENTRY_APPROACH", "loc": (17.0, -5.0, 1.1), "dims": (7.0, 18.0, 2.2), "kind": "vehicle"},
    {"name": "PEDESTRIAN_PROTECTED_PATH", "loc": (12.1, 12.0, 1.0), "dims": (1.2, 10.0, 2.0), "kind": "pedestrian"},
    {"name": "SECURE_BOOKING_TRANSFER", "loc": (-12.0, 0.0, 1.0), "dims": (2.0, 8.0, 2.0), "kind": "transfer"},
]
mats = {"vehicle": MAT_VEHICLE, "pedestrian": MAT_PEDESTRIAN, "transfer": MAT_TRANSFER}
for route in routes:
    make_box(route["name"], route["loc"], route["dims"], mats[route["kind"]])

def world_bounds(obj):
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return (
        tuple(min(p[i] for p in corners) for i in range(3)),
        tuple(max(p[i] for p in corners) for i in range(3)),
    )

def overlaps(a, b):
    amin, amax = a
    bmin, bmax = b
    return all(amin[i] < bmax[i] and amax[i] > bmin[i] for i in range(3))

# Exclude the guide collection, floor plates, vehicle proxy volumes and common
# guide/label objects. Remaining overlaps are candidates for human inspection.
excluded_tokens = (
    "SLAB", "FLOOR", "ROOF", "CLEARANCE", "GUIDE", "ZONE_", "STAIR_",
    "DOOR_ACCESS", "WAYFINDING", "BRANDING", "EMBLEM", "STAGE28_",
    "GARAGE13_", "EXTERIOR_ACCESS", "SITE_SECURITY",
)
candidates = []
for obj in scene.objects:
    if obj.type != "MESH" or obj.name.startswith(PREFIX):
        continue
    if any(token in obj.name.upper() for token in excluded_tokens):
        continue
    if obj.dimensions.length == 0:
        continue
    candidates.append(obj)

findings = []
for route in routes:
    route_obj = bpy.data.objects.get(PREFIX + route["name"])
    route_bounds = world_bounds(route_obj)
    hits = []
    for obj in candidates:
        if overlaps(route_bounds, world_bounds(obj)):
            hits.append(obj.name)
    findings.append({
        "route": route["name"],
        "route_type": route["kind"],
        "status": "REVIEW_POSSIBLE_OBSTRUCTION" if hits else "NO_AABB_INTERSECTION_FOUND",
        "intersecting_objects": hits,
        "intersection_method": "world-axis-aligned bounding-box screening",
    })

report = {
    "stage": 28,
    "title": "Garage and secure ground-floor layout screening",
    "status": "REQUIRES_MANUAL_REVIEW",
    "routes": findings,
    "vehicle_clearance_assumptions_m": {
        "nominal_vehicle_width": 2.6,
        "nominal_vehicle_length": 5.8,
        "note": "Screening envelope only; vehicle type, turning radius, door opening and swept path remain unverified."
    },
    "limitations": [
        "All route locations are provisional and based on the schematic centre-origin plan.",
        "AABB overlap may produce false positives and can miss angled/functional conflicts.",
        "No true vehicle swept-path, door swing, line-of-sight, fire-code, accessibility, or security certification is performed.",
        "The guide collection is review-only and must be hidden or excluded from final exports.",
        "This audit does not move walls/furniture or prove that the MLO works in FiveM."
    ]
}
block = bpy.data.texts.get(REPORT_NAME) or bpy.data.texts.new(REPORT_NAME)
block.clear()
block.write(json.dumps(report, indent=2))
print("[Stage 28] Garage/secure layout report written to " + REPORT_NAME)
for item in findings:
    print("[Stage 28] %s: %s (%d candidate overlaps)" % (
        item["route"], item["status"], len(item["intersecting_objects"])))
