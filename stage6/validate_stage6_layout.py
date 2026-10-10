"""Stage 6: layout validation for the PDHQ schematic Blender scene.

Run after stages 2-4. Non-destructive: reports heuristic layout risks only.
It does not prove accessibility, game collision, or actual FiveM playability.
"""
import bpy
from mathutils import Vector

PREFIX = "PDHQ_"
lines = []
def out(s=""): lines.append(str(s))

scene = bpy.context.scene
objs = list(scene.objects)
by_name = {o.name: o for o in objs}
out("PDHQ STAGE 6 — LAYOUT VALIDATION")
out("=" * 72)

# Check that expected collections and stages' anchor objects exist.
expected_collections = [
    "PDHQ_STRUCTURE", "PDHQ_INTERIOR_ZONES", "PDHQ_ROOF_EQUIPMENT",
    "PDHQ_EXTERIOR_ASSETS", "PDHQ_COLLISION_PROXIES", "PDHQ_GUIDES",
    "PDHQ_FURNITURE_BLOCKOUT",
]
out("\nCOLLECTION PRESENCE")
for name in expected_collections:
    col = bpy.data.collections.get(name)
    out("%s: %s" % (name, "OK (%d objects)" % len(list(col.all_objects)) if col else "MISSING"))

out("\nANCHOR OBJECTS")
anchors = [
    "PDHQ_F1_SL A B",
]
# Explicit anchors avoid silently assuming that every stage has been run.
anchor_names = [
    "PDHQ_F1_SLAB", "PDHQ_F2_SLAB", "PDHQ_F3_SLAB", "PDHQ_ROOF_DECK",
    "PDHQ_ENTRANCE_CANOPY", "PDHQ_HELIPAD_PLATFORM",
    "PDHQ_F1_RECEPTION_COUNTER_TOP", "PDHQ_F2_DISPATCH_CONSOLE_1_TOP",
    "PDHQ_F3_DETECTIVE_DESK_1_TOP",
]
for name in anchor_names:
    out("%s: %s" % (name, "FOUND" if name in by_name else "NOT FOUND (check run order or naming)"))

out("\nFURNITURE / CLEARANCE COUNTS")
for prefix in [
    "PDHQ_F1_GARAGE_VEHICLE_CLEARANCE_",
    "PDHQ_F1_BOOKING_INTAKE_",
    "PDHQ_F1_HOLDING_BENCH_",
    "PDHQ_F2_DISPATCH_CONSOLE_",
    "PDHQ_F2_EVIDENCE_CABINET_",
    "PDHQ_F2_ARMORY_LOCKER_",
    "PDHQ_F3_DETECTIVE_DESK_",
    "PDHQ_F3_INTERVIEW_TABLE_",
]:
    matches = [o for o in objs if o.name.startswith(prefix)]
    out("%-42s %d objects" % (prefix, len(matches)))

# Axis-aligned bounding box overlap heuristic for major floor furnishings.
# It intentionally ignores vertical overlap and uses conservative X/Y bounds.
def bounds_xy(obj):
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return (min(v.x for v in corners), max(v.x for v in corners),
            min(v.y for v in corners), max(v.y for v in corners),
            min(v.z for v in corners), max(v.z for v in corners))

clearance = [o for o in objs if o.name.startswith("PDHQ_F1_GARAGE_VEHICLE_CLEARANCE_")]
desks = [o for o in objs if o.type == "MESH" and (
    "_DESK_" in o.name or "_COUNTER_" in o.name or "_CONSOLE_" in o.name
) and not o.name.endswith(("_TOP","_MONITOR","_KEYBOARD","_PEDESTAL","_LEG"))]
out("\nGARAGE CLEARANCE GUIDE INTERSECTION CHECK")
out("This is a coarse bounding-box test against furniture/counters/consoles only.")
intersections = []
for guide in clearance:
    gx0,gx1,gy0,gy1,gz0,gz1 = bounds_xy(guide)
    for other in desks:
        ox0,ox1,oy0,oy1,oz0,oz1 = bounds_xy(other)
        overlap = gx0 < ox1 and gx1 > ox0 and gy0 < oy1 and gy1 > oy0 and gz0 < oz1 and gz1 > oz0
        if overlap:
            intersections.append("%s overlaps %s (coarse bounds)" % (guide.name, other.name))
if intersections:
    for item in intersections[:100]: out("REVIEW: " + item)
    if len(intersections) > 100: out("... and %d more" % (len(intersections)-100))
else:
    out("No overlaps detected against selected furniture types (not a full collision test).")

out("\nREVIEW REMINDERS")
out("- Check Stage 2 perimeter walls and Stage 3 partitions for duplicate/overlapping geometry.")
out("- Confirm door openings connect rooms and do not terminate into walls or furniture.")
out("- Inspect stairs for landing continuity, headroom, and plausible rise/run.")
out("- Confirm each floor's furniture is placed inside its intended room; coordinates alone do not prove room membership.")
out("- Check garage vehicle turning paths and pedestrian separation with representative vehicle dimensions.")
out("- Test visibility, collision, texture streaming, and frame-time in a real FiveM server after export.")
report = "\n".join(lines)
tb = bpy.data.texts.get("PDHQ_STAGE6_LAYOUT_REPORT") or bpy.data.texts.new("PDHQ_STAGE6_LAYOUT_REPORT")
tb.clear()
tb.write(report)
print(report)
