"""Stage 30: advisory exterior access, perimeter and helipad clearance review.

Run inside Blender after the scene generators. This is a name/dimension/AABB
screen only; it does not certify aviation, fire access, accessibility, security,
structural loading, or GTA/FiveM map correctness.
"""
import bpy
import json
from mathutils import Vector

REPORT_NAME = "PDHQ_STAGE30_EXTERIOR_HELIPAD_REPORT"
GUIDE_COLLECTIONS = (
    "PDHQ_EXTERIOR_ACCESS_GUIDES",
    "PDHQ_SITE_SECURITY_LANDSCAPE_GUIDES",
)


def world_bounds(obj):
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return {
        "min": [min(v[i] for v in corners) for i in range(3)],
        "max": [max(v[i] for v in corners) for i in range(3)],
        "dimensions": [max(v[i] for v in corners) - min(v[i] for v in corners) for i in range(3)],
    }


def intersects_xy(a, b, margin=0.0):
    return (
        a["min"][0] - margin <= b["max"][0]
        and a["max"][0] + margin >= b["min"][0]
        and a["min"][1] - margin <= b["max"][1]
        and a["max"][1] + margin >= b["min"][1]
    )


def main():
    objects = list(bpy.context.scene.objects)
    by_name = {obj.name: obj for obj in objects}
    required = {
        "helipad platform": "HELIPAD_PLATFORM",
        "roof deck": "ROOF_DECK",
        "HVAC unit 1": "HVAC_UNIT_1",
        "public approach guide": "Public_Pedestrian_Approach",
        "accessible landing guide": "Accessible_Entrance_Landing",
        "emergency access lane guide": "Emergency_Clear_Access_Lane",
        "main security gate guide": "PROVISIONAL_Main_Security_Gate_Zone",
        "service gate guide": "PROVISIONAL_Service_Security_Gate_Zone",
        "garage approach guide": "PROVISIONAL_Garage_Approach",
        "service approach guide": "PROVISIONAL_Service_Approach",
        "vehicle turning review guide": "Vehicle_Turning_Review_Envelope",
    }
    checks = []
    for label, name in required.items():
        obj = by_name.get(name)
        checks.append({
            "check": label,
            "object": name,
            "status": "PRESENT_REVIEW_REQUIRED" if obj else "MISSING",
            "bounds": world_bounds(obj) if obj else None,
        })

    pad = by_name.get("HELIPAD_PLATFORM")
    pad_bounds = world_bounds(pad) if pad else None
    hvac_findings = []
    for obj in objects:
        if obj.name.startswith("HVAC_UNIT_") or obj.name.startswith("HVAC_BASE_"):
            bounds = world_bounds(obj)
            hvac_findings.append({
                "object": obj.name,
                "bounds": bounds,
                "overlaps_helipad_xy": bool(pad_bounds and intersects_xy(pad_bounds, bounds)),
            })

    collections = {}
    for name in GUIDE_COLLECTIONS:
        col = bpy.data.collections.get(name)
        collections[name] = {
            "present": col is not None,
            "object_count": len(col.objects) if col else 0,
        }

    missing = [item["check"] for item in checks if item["status"] == "MISSING"]
    possible_hvac_conflicts = [item["object"] for item in hvac_findings if item["overlaps_helipad_xy"]]
    report = {
        "stage": 30,
        "purpose": "Advisory exterior/site/helipad review",
        "status": "REVIEW_REQUIRED" if missing or possible_hvac_conflicts else "INVENTORY_COMPLETE_REVIEW_REQUIRED",
        "checks": checks,
        "guide_collections": collections,
        "helipad": {"bounds": pad_bounds, "hvac_xy_overlap_candidates": possible_hvac_conflicts},
        "hvac_review": hvac_findings,
        "limitations": [
            "Axis-aligned bounds and object names are screening heuristics; false positives and false negatives are possible.",
            "No swept vehicle path, turning simulation, terrain grading, drainage, fire-engine access, or gate operation is computed.",
            "No aviation obstacle-surface, rotor clearance, wind, lighting, structural, or regulatory review is performed.",
            "All exterior routes and site gates remain provisional until the actual site and building geometry are inspected.",
            "This script does not repair geometry, remove guides, export GTA assets, or validate the map in FiveM.",
        ],
    }
    output = json.dumps(report, indent=2)
    block = bpy.data.texts.get(REPORT_NAME) or bpy.data.texts.new(REPORT_NAME)
    block.clear()
    block.write(output)
    print(output)
    print("Stage 30 complete: inspect the report and verify all routes/clearances visually in Blender.")


if __name__ == "__main__":
    main()
