"""Stage 35: floor-by-floor architectural coordination audit for Blender.

Checks schematic slab elevations, circulation openings, guide footprints and roof
helipad bounds. Non-destructive; all findings require manual Blender review.
"""
import json
from datetime import datetime, timezone
from mathutils import Vector
import bpy

PREFIX = "PDHQ_"
FLOOR_HEIGHT = 4.2
SLAB_THICKNESS = 0.28
BUILDING_WIDTH = 54.0
BUILDING_DEPTH = 38.0
FLOOR_COUNT = 3
STAIR_CENTRES_X = (-22.0, 22.0)
STAIR_SIZE = (5.0, 8.0)
ELEVATOR_CENTRE = (0.0, 0.0)
ELEVATOR_SIZE = (3.2, 3.2)
REPORT_NAME = "PDHQ_STAGE35_FLOOR_COORDINATION_REPORT"
EPS = 0.03


def bounds(obj):
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return {
        "min": [min(v[i] for v in corners) for i in range(3)],
        "max": [max(v[i] for v in corners) for i in range(3)],
    }


def xy_overlap(box, cx, cy, sx, sy):
    return (box["min"][0] < cx + sx / 2 - EPS and box["max"][0] > cx - sx / 2 + EPS
            and box["min"][1] < cy + sy / 2 - EPS and box["max"][1] > cy - sy / 2 + EPS)


def main():
    scene_objects = list(bpy.context.scene.objects)
    by_name = {obj.name: obj for obj in scene_objects}
    slab_reports = []
    missing_slabs = []
    bad_elevations = []
    opening_conflicts = []
    guide_checks = []

    for floor in range(1, FLOOR_COUNT + 1):
        expected_z = (floor - 1) * FLOOR_HEIGHT
        prefix = PREFIX + "F{}_SLAB_TILE_".format(floor)
        tiles = [obj for obj in scene_objects if obj.type == "MESH" and obj.name.startswith(prefix)]
        if not tiles:
            missing_slabs.append("F{}_SLAB_TILE_*".format(floor))
        z_values = []
        for tile in tiles:
            b = bounds(tile)
            center_z = (b["min"][2] + b["max"][2]) / 2
            z_values.append(round(center_z, 3))
            if abs(center_z - expected_z) > 0.08:
                bad_elevations.append({"object": tile.name, "expected_center_z_m": expected_z,
                                       "actual_center_z_m": round(center_z, 3)})
            for sx in STAIR_CENTRES_X:
                if xy_overlap(b, sx, 0.0, *STAIR_SIZE):
                    opening_conflicts.append({"object": tile.name, "opening": "stair",
                                              "center_xy_m": [sx, 0.0]})
            if xy_overlap(b, *ELEVATOR_CENTRE, ELEVATOR_SIZE, ELEVATOR_SIZE):
                opening_conflicts.append({"object": tile.name, "opening": "elevator",
                                          "center_xy_m": list(ELEVATOR_CENTRE)})
        slab_reports.append({"floor": floor, "expected_center_z_m": expected_z,
                             "tile_count": len(tiles),
                             "observed_center_z_range_m": [min(z_values), max(z_values)] if z_values else None})

    roof_z = FLOOR_COUNT * FLOOR_HEIGHT
    roof_tiles = [obj for obj in scene_objects if obj.type == "MESH" and obj.name.startswith(PREFIX + "ROOF_DECK_TILE_")]
    if not roof_tiles:
        missing_slabs.append("ROOF_DECK_TILE_*")
    roof_bounds = [bounds(obj) for obj in roof_tiles]
    for tile, b in zip(roof_tiles, roof_bounds):
        center_z = (b["min"][2] + b["max"][2]) / 2
        if abs(center_z - roof_z) > 0.08:
            bad_elevations.append({"object": tile.name, "expected_center_z_m": roof_z,
                                   "actual_center_z_m": round(center_z, 3)})

    for label, x, y, sx, sy, expected_z in [
        ("stair_left", STAIR_CENTRES_X[0], 0.0, *STAIR_SIZE, roof_z / 2),
        ("stair_right", STAIR_CENTRES_X[1], 0.0, *STAIR_SIZE, roof_z / 2),
        ("elevator", *ELEVATOR_CENTRE, ELEVATOR_SIZE, ELEVATOR_SIZE, roof_z / 2),
    ]:
        candidates = [obj for obj in scene_objects if obj.name.startswith(PREFIX) and
                      (label == "elevator" and "ELEVATOR_SHAFT_GUIDE" in obj.name or
                       label.startswith("stair") and "STAIR_CORE_GUIDE" in obj.name and
                       (("M22" in obj.name) if label == "stair_left" else ("P22" in obj.name)))]
        if not candidates:
            guide_checks.append({"guide": label, "status": "MISSING"})
            continue
        obj = candidates[0]
        expected_xy = [x, y]
        actual_xy = [round(obj.location.x, 3), round(obj.location.y, 3)]
        dimensions = list(obj.get("guide_dimensions_m", []))
        guide_checks.append({"guide": label, "status": "FOUND", "expected_xy_m": expected_xy,
                             "actual_xy_m": actual_xy, "guide_dimensions_m": dimensions,
                             "center_xy_matches": all(abs(actual_xy[i] - expected_xy[i]) < 0.05 for i in range(2))})

    heli = by_name.get(PREFIX + "HELIPAD_PLATFORM")
    helipad_check = {"status": "MISSING"}
    if heli:
        hb = bounds(heli)
        hx = (hb["min"][0] + hb["max"][0]) / 2
        hy = (hb["min"][1] + hb["max"][1]) / 2
        hw = hb["max"][0] - hb["min"][0]
        hd = hb["max"][1] - hb["min"][1]
        # Roof outer footprint is nominally x +/-27 and y +/-19.
        inside = (hb["min"][0] >= -BUILDING_WIDTH/2 - EPS and hb["max"][0] <= BUILDING_WIDTH/2 + EPS
                  and hb["min"][1] >= -BUILDING_DEPTH/2 - EPS and hb["max"][1] <= BUILDING_DEPTH/2 + EPS)
        helipad_check = {"status": "FOUND", "center_xy_m": [round(hx, 3), round(hy, 3)],
                         "size_xy_m": [round(hw, 3), round(hd, 3)],
                         "inside_nominal_roof_footprint": inside,
                         "note": "Footprint containment only; safe approach, obstacle clearance and bearing capacity are not assessed."}

    errors = len(missing_slabs) + len(bad_elevations) + len(opening_conflicts)
    report = {
        "stage": 35,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "scene": bpy.context.scene.name,
        "status": "REVIEW_REQUIRED" if errors or any(g["status"] == "MISSING" for g in guide_checks) or helipad_check["status"] == "MISSING" else "SCREENING_COMPLETE_MANUAL_REVIEW_REQUIRED",
        "production_ready": False,
        "floor_slab_coordination": slab_reports,
        "missing_slab_groups": missing_slabs,
        "unexpected_slab_elevations": bad_elevations,
        "slab_tiles_intersecting_circulation_opening_footprints": opening_conflicts,
        "vertical_circulation_guides": guide_checks,
        "helipad_roof_footprint_check": helipad_check,
        "interpretation": [
            "Checks are based on expected schematic coordinates and world-space AABBs, not exact mesh topology.",
            "No report finding proves that a stair is walkable, an elevator is functional, or a slab is structurally adequate.",
            "The helipad test checks only whether its bounding box fits inside the nominal roof footprint; it is not aviation or structural clearance approval.",
            "Review each floor in Blender and validate doors, landings, headroom, accessible paths, roof access and real collision.",
            "This script makes no changes to scene objects, transforms, meshes, materials, modifiers or collections."
        ]
    }
    block = bpy.data.texts.get(REPORT_NAME) or bpy.data.texts.new(REPORT_NAME)
    block.clear()
    block.write(json.dumps(report, indent=2))
    print("[PDHQ Stage 35] Floor coordination report written to " + REPORT_NAME)
    print("[PDHQ Stage 35] Missing slab groups: %d; elevation anomalies: %d; opening conflicts: %d" %
          (len(missing_slabs), len(bad_elevations), len(opening_conflicts)))


if __name__ == "__main__":
    main()
