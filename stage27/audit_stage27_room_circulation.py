"""Stage 27: room-layout and circulation conflict audit.

Run after Stages 2, 26, 3, and 4 in the same Blender scene. This pass is
non-destructive: it reports AABB intersections between furniture proxies and
partition geometry, checks key route envelopes, and creates visible review
markers for circulation paths. It does not move or delete architectural assets.
"""
import json
from itertools import combinations
from pathlib import Path

import bpy
from mathutils import Vector

PREFIX = "PDHQ_"
REPORT_NAME = "PDHQ_STAGE27_ROOM_CIRCULATION_REPORT"
GUIDE_COLLECTION = "PDHQ_STAGE27_CIRCULATION_REVIEW"
# Approximate route envelopes in metres: center, width, length, and floor z.
ROUTES = [
    {"name": "F1_PUBLIC_ENTRY_TO_RECEPTION", "center": (-15.0, -15.0), "width": 1.8, "length": 7.0, "z": 0.34},
    {"name": "F1_BOOKING_APPROACH", "center": (-5.0, -7.0), "width": 1.5, "length": 5.0, "z": 0.34},
    {"name": "F1_GARAGE_DRIVE_AISLE", "center": (0.0, 15.0), "width": 3.2, "length": 18.0, "z": 0.34},
    {"name": "F2_DISPATCH_APPROACH", "center": (1.0, 5.0), "width": 1.6, "length": 9.0, "z": 4.54},
    {"name": "F2_SECURE_STORAGE_APPROACH", "center": (-16.0, 5.0), "width": 1.6, "length": 9.0, "z": 4.54},
    {"name": "F3_INTERVIEW_APPROACH", "center": (-14.5, 5.0), "width": 1.6, "length": 9.0, "z": 8.74},
]
FLOOR_TOLERANCE = 1.8


def collection(name):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


def clear_collection(col):
    for obj in list(col.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def bounds(obj):
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return (
        min(p.x for p in corners), max(p.x for p in corners),
        min(p.y for p in corners), max(p.y for p in corners),
        min(p.z for p in corners), max(p.z for p in corners),
    )


def overlap(a, b, margin=0.0):
    return (
        a[0] < b[1] - margin and a[1] > b[0] + margin and
        a[2] < b[3] - margin and a[3] > b[2] + margin and
        a[4] < b[5] - margin and a[5] > b[4] + margin
    )


def floor_band(b):
    return (b[4] + b[5]) / 2


def make_marker(name, center, width, length, z, col):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(center[0], center[1], z))
    obj = bpy.context.object
    obj.name = PREFIX + "STAGE27_ROUTE_" + name
    obj.dimensions = (width, length, 0.035)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.display_type = "WIRE"
    obj.show_in_front = True
    obj.hide_render = True
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)
    obj["review_only"] = True
    obj["route_name"] = name
    return obj


def main():
    col = collection(GUIDE_COLLECTION)
    clear_collection(col)
    # Keep route markers in their own collection so they can be hidden before export.
    route_reports = []
    for route in ROUTES:
        marker = make_marker(route["name"], route["center"], route["width"], route["length"], route["z"], col)
        route_box = bounds(marker)
        blocked = []
        for obj in bpy.data.objects:
            if obj == marker or obj.name.startswith(PREFIX + "STAGE27_ROUTE_"):
                continue
            if obj.type != "MESH":
                continue
            name = obj.name
            if not (name.startswith(PREFIX + "F1_") or name.startswith(PREFIX + "F2_") or name.startswith(PREFIX + "F3_")):
                continue
            # Only compare against meshes close to the route's floor; this is a screening heuristic.
            obj_box = bounds(obj)
            if abs(floor_band(obj_box) - route["z"]) > FLOOR_TOLERANCE:
                continue
            if overlap(route_box, obj_box):
                blocked.append({"object": name, "bounds": [round(v, 3) for v in obj_box]})
        route_reports.append({
            "route": route["name"],
            "envelope_m": {"width": route["width"], "length": route["length"]},
            "possible_intersections": blocked,
            "status": "REVIEW_POSSIBLE_OBSTRUCTION" if blocked else "NO_AABB_INTERSECTION_FOUND",
        })

    # Broad proxy-to-partition intersection list. This is intentionally a screening
    # pass: bounding boxes can report false positives for angled/visual-only objects.
    furniture = [o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith(PREFIX)
                 and any(k in o.name for k in ("RECEPTION", "BOOKING", "HOLDING", "GARAGE",
                     "DISPATCH", "EVIDENCE", "ARMORY", "SWAT", "DETECTIVE", "INTERVIEW",
                     "CONFERENCE", "FILE_STORAGE"))]
    partitions = [o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith(PREFIX)
                  and ("PARTITION" in o.name or "CORRIDOR_" in o.name or "ROOM_DIV" in o.name)]
    intersections = []
    for furn, wall in combinations(furniture + partitions, 2):
        if furn in partitions or wall in furniture:
            continue
        if not (any(k in furn.name for k in ("RECEPTION", "BOOKING", "HOLDING", "GARAGE",
                "DISPATCH", "EVIDENCE", "ARMORY", "SWAT", "DETECTIVE", "INTERVIEW",
                "CONFERENCE", "FILE_STORAGE")) and
                ("PARTITION" in wall.name or "CORRIDOR_" in wall.name or "ROOM_DIV" in wall.name)):
            continue
        fb, wb = bounds(furn), bounds(wall)
        if abs(floor_band(fb) - floor_band(wb)) <= FLOOR_TOLERANCE and overlap(fb, wb):
            intersections.append({"fixture": furn.name, "partition": wall.name})

    report = {
        "stage": 27,
        "status": "REVIEW_REQUIRED",
        "routes": route_reports,
        "fixture_partition_aabb_intersections": intersections,
        "counts": {
            "route_envelopes": len(route_reports),
            "routes_with_possible_obstructions": sum(bool(r["possible_intersections"]) for r in route_reports),
            "fixture_partition_intersections": len(intersections),
        },
        "limitations": [
            "AABB screening can produce false positives and false negatives; it is not a physical collision engine.",
            "Route envelopes are provisional planning guides and must be adjusted after inspecting the actual floor plan.",
            "Door swings, stair headroom, accessibility, security zoning, and vehicle swept paths require manual review.",
            "Hide PDHQ_STAGE27_CIRCULATION_REVIEW before final export; it contains review-only wireframe markers.",
            "No Blender execution is implied by repository CI syntax checks.",
        ],
    }
    block = bpy.data.texts.get(REPORT_NAME) or bpy.data.texts.new(REPORT_NAME)
    block.clear()
    block.write(json.dumps(report, indent=2))
    print("[PDHQ Stage 27] Room circulation screening complete; review findings in " + REPORT_NAME)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
