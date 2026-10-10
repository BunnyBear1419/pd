"""Stage 29 — room dimensions, door clearances, and furniture screening.

Run inside Blender after the scene has been generated. This is a non-destructive,
heuristic audit: it reports object dimensions and possible overlaps; it does not
infer code-compliant room boundaries or certify accessibility.
"""
import json
import bpy
from mathutils import Vector

REPORT_NAME = "PDHQ_STAGE29_ROOM_CLEARANCE_REPORT"
MIN_DOOR_CLEAR_WIDTH_M = 0.90
MIN_CORRIDOR_SCREENING_WIDTH_M = 1.20
MIN_ROOM_SIDE_SCREENING_M = 2.40
EXCLUDED_NAME_TOKENS = (
    "GUIDE", "CLEARANCE", "ZONE_", "WAYFINDING", "BRANDING", "EMBLEM",
    "STAGE27_", "STAGE28_", "STAGE29_", "ARCHITECTURAL_DETAILS",
    "GARAGE13_", "EXTERIOR_ACCESS", "SITE_SECURITY",
)

def bounds(obj):
    pts = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return (
        tuple(min(p[i] for p in pts) for i in range(3)),
        tuple(max(p[i] for p in pts) for i in range(3)),
    )

def overlaps(a, b, epsilon=0.015):
    amin, amax = a
    bmin, bmax = b
    return all(amin[i] < bmax[i] - epsilon and amax[i] > bmin[i] + epsilon for i in range(3))

def world_dims(obj):
    lo, hi = bounds(obj)
    return tuple(round(hi[i] - lo[i], 3) for i in range(3))

def ignored(obj):
    name = obj.name.upper()
    return any(token in name for token in EXCLUDED_NAME_TOKENS)

objects = [o for o in bpy.context.scene.objects if o.type == "MESH" and not ignored(o)]
door_objects = [o for o in objects if any(t in o.name.upper() for t in ("DOOR", "FRAME"))]
furniture = [o for o in objects if any(t in o.name.upper() for t in (
    "DESK", "COUNTER", "BENCH", "CABINET", "LOCKER", "TABLE", "CONSOLE",
    "CHAIR", "SHELF", "BED", "WORKBENCH", "STORAGE", "INTERVIEW", "EVIDENCE",
))]

door_findings = []
for obj in door_objects:
    dims = world_dims(obj)
    # For simple door leaves, the smallest horizontal dimension is treated as
    # width only when orientation is ambiguous; every flag remains advisory.
    horizontal = sorted((dims[0], dims[1]))
    estimated_clear_width = horizontal[0] if horizontal[0] < 1.5 else horizontal[1]
    flags = []
    if "DOOR" in obj.name.upper() and "FRAME" not in obj.name.upper() and estimated_clear_width < MIN_DOOR_CLEAR_WIDTH_M:
        flags.append("POSSIBLY_NARROW_DOOR_LEAF_OR_PROXY")
    door_findings.append({
        "object": obj.name,
        "world_dimensions_m": dims,
        "estimated_horizontal_width_m": round(estimated_clear_width, 3),
        "flags": flags,
        "note": "Proxy dimensions do not equal certified clear opening; verify opening between jambs in Blender."
    })

fixture_overlaps = []
for i, a in enumerate(furniture):
    for b in furniture[i + 1:]:
        if overlaps(bounds(a), bounds(b)):
            fixture_overlaps.append({
                "object_a": a.name,
                "object_b": b.name,
                "status": "REVIEW_POSSIBLE_FIXTURE_OVERLAP",
            })

small_meshes = []
for obj in objects:
    dims = world_dims(obj)
    horizontal = sorted((dims[0], dims[1]))
    # Only label likely furniture or partition objects; generic meshes may be
    # signage, trim, or architectural accents and are not assumed to be rooms.
    name = obj.name.upper()
    if any(t in name for t in ("ROOM", "CORRIDOR", "HALL", "PARTITION", "WALL")):
        if horizontal[0] < MIN_ROOM_SIDE_SCREENING_M and max(dims) > 1.8:
            small_meshes.append({
                "object": obj.name,
                "world_dimensions_m": dims,
                "status": "REVIEW_DIMENSION_OR_CLASSIFICATION",
            })

report = {
    "stage": 29,
    "title": "Room dimensions, door clearances, and furniture screening",
    "status": "REQUIRES_MANUAL_REVIEW",
    "scene_object_count": len(objects),
    "door_and_frame_proxy_count": len(door_objects),
    "furniture_proxy_count": len(furniture),
    "screening_thresholds_m": {
        "door_proxy_width": MIN_DOOR_CLEAR_WIDTH_M,
        "corridor_width_reference": MIN_CORRIDOR_SCREENING_WIDTH_M,
        "room_side_reference": MIN_ROOM_SIDE_SCREENING_M,
        "note": "Reference values are screening prompts, not jurisdiction-specific code requirements."
    },
    "door_findings": door_findings,
    "possible_furniture_overlaps": fixture_overlaps,
    "possible_small_room_or_partition_dimensions": small_meshes,
    "limitations": [
        "The scene uses schematic objects and names; room polygons and usable floor areas are not reliably inferred.",
        "Door leaves and frame proxies do not establish actual clear opening or door swing.",
        "Bounding-box overlap is approximate and can report false positives or miss functional conflicts.",
        "Accessibility, turning circles, egress, fire-code compliance, and secure separation require manual review against applicable requirements.",
        "No geometry is moved or repaired, and no production readiness or FiveM compatibility is certified."
    ]
}
block = bpy.data.texts.get(REPORT_NAME) or bpy.data.texts.new(REPORT_NAME)
block.clear()
block.write(json.dumps(report, indent=2))
print("[Stage 29] Room-clearance report written to " + REPORT_NAME)
print("[Stage 29] Door/frame proxies: %d; furniture proxies: %d; possible fixture overlaps: %d" % (
    len(door_objects), len(furniture), len(fixture_overlaps)))
