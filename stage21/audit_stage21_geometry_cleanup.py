"""Stage 21: non-destructive geometry cleanup and export-preparation audit.

The audit flags review candidates only. It never deletes, joins, repairs, hides,
or exports scene objects. AABB overlap results are heuristic and may be false positives.
"""
import bpy
import json
from mathutils import Vector

GUIDE_TOKENS = (
    "guide", "clearance", "proxy", "placeholder", "planning", "staging",
    "approach", "route", "transfer", "bay_line", "crossing", "review_envelope",
    "blockout", "zone_label", "collision_proxy",
)
DIMENSION_EPSILON = 0.01
MAX_OVERLAP_PAIRS = 4000


def collection_names(obj):
    return sorted(c.name for c in obj.users_collection)


def world_bounds(obj):
    try:
        corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        return {
            "min": [round(min(v[i] for v in corners), 3) for i in range(3)],
            "max": [round(max(v[i] for v in corners), 3) for i in range(3)],
        }
    except Exception:
        return None


def is_guide(obj):
    combined = (obj.name + " " + " ".join(collection_names(obj))).lower()
    return any(token in combined for token in GUIDE_TOKENS)


def aabb_overlap(a, b):
    ba, bb = world_bounds(a), world_bounds(b)
    if not ba or not bb:
        return False
    for axis in range(3):
        # Require a small positive overlap; touching faces alone are not reported.
        if min(ba["max"][axis], bb["max"][axis]) - max(ba["min"][axis], bb["min"][axis]) <= DIMENSION_EPSILON:
            return False
    return True


def main():
    scene = bpy.context.scene
    objects = list(scene.objects)
    meshes = [obj for obj in objects if obj.type == "MESH"]
    guide_candidates = []
    zero_dimension = []
    extreme_dimensions = []
    non_manifold = []
    shared_mesh_data = []
    missing_material = []
    overlap_pairs = []

    for obj in objects:
        dims = [round(float(v), 4) for v in obj.dimensions]
        if is_guide(obj):
            guide_candidates.append({
                "object": obj.name, "type": obj.type, "collections": collection_names(obj),
                "note": "Name or collection suggests temporary guide/proxy; verify before exclusion.",
            })
        if obj.type != "MESH":
            continue
        if any(float(v) <= DIMENSION_EPSILON for v in obj.dimensions):
            zero_dimension.append({"object": obj.name, "dimensions": dims})
        if max((float(v) for v in obj.dimensions), default=0.0) >= 50.0:
            extreme_dimensions.append({"object": obj.name, "dimensions": dims, "note": "Confirm this is an intentional site/building-scale object."})
        if obj.data.users > 1:
            shared_mesh_data.append({"object": obj.name, "mesh_data": obj.data.name, "mesh_data_users": obj.data.users})
        if not any(obj.data.materials):
            missing_material.append(obj.name)
        try:
            bm = __import__("bmesh")
            temp_mesh = bm.new()
            temp_mesh.from_mesh(obj.data)
            bad_edges = sum(1 for edge in temp_mesh.edges if not edge.is_manifold)
            temp_mesh.free()
            if bad_edges:
                non_manifold.append({"object": obj.name, "non_manifold_edge_count": bad_edges})
        except Exception as exc:
            non_manifold.append({"object": obj.name, "check_error": str(exc)[:180]})

    # Restrict expensive overlap review to production-looking meshes, but retain
    # all candidate pairs up to a hard cap. False positives are expected for layered walls.
    overlap_meshes = [obj for obj in meshes if not is_guide(obj)]
    pairs_checked = 0
    capped = False
    for index, a in enumerate(overlap_meshes):
        for b in overlap_meshes[index + 1:]:
            if pairs_checked >= MAX_OVERLAP_PAIRS:
                capped = True
                break
            pairs_checked += 1
            if aabb_overlap(a, b):
                overlap_pairs.append({
                    "object_a": a.name,
                    "object_b": b.name,
                    "collections_a": collection_names(a),
                    "collections_b": collection_names(b),
                    "bounds_a": world_bounds(a),
                    "bounds_b": world_bounds(b),
                    "note": "AABB intersection only; may be intentional or a false positive. Inspect in Blender.",
                })
        if capped:
            break

    report = {
        "stage": 21,
        "scene": scene.name,
        "object_count": len(objects),
        "mesh_count": len(meshes),
        "temporary_guide_or_proxy_review_count": len(guide_candidates),
        "near_zero_dimension_mesh_count": len(zero_dimension),
        "extreme_dimension_review_count": len(extreme_dimensions),
        "non_manifold_edge_review_count": len(non_manifold),
        "shared_mesh_data_object_count": len(shared_mesh_data),
        "mesh_without_assigned_material_count": len(missing_material),
        "aabb_overlap_pairs_found": len(overlap_pairs),
        "aabb_pairs_checked": pairs_checked,
        "aabb_pair_scan_capped": capped,
        "temporary_guide_or_proxy_candidates": guide_candidates,
        "near_zero_dimension_meshes": zero_dimension,
        "extreme_dimension_objects": extreme_dimensions,
        "non_manifold_edge_candidates": non_manifold,
        "objects_sharing_mesh_data": shared_mesh_data,
        "mesh_objects_without_materials": missing_material,
        "aabb_overlap_review_pairs": overlap_pairs,
        "manual_critical_checks": [
            "Inspect every floor slab around the stairwell and elevator shaft; verify real openings and safe shaft boundaries.",
            "Inspect stairs, landings, door openings, and door leaves for clearance and physical continuity.",
            "Check facade fins, glazing mullions, canopy details, signs, emblems, and interior finish layers for z-fighting or accidental overlaps.",
            "Verify garage turning path, vehicle clearance, pedestrian separation, helipad access, and emergency approaches.",
            "Review guide/proxy objects manually; do not delete by name alone.",
            "Use Edit Mode and mesh analysis to confirm topology, normals, watertight collision meshes, and intended thickness.",
        ],
        "limitations": [
            "Non-destructive heuristic audit only; no geometry is repaired, hidden, joined, deleted, or exported.",
            "Axis-aligned bounding-box overlap is not an exact mesh intersection test and can report intentional overlaps.",
            "Non-manifold edge counts need manual interpretation, especially for open render surfaces.",
            "This report does not validate Sollumz archetypes, GTA collision, portals, occlusion, LODs, or in-game behavior.",
        ],
    }
    text = bpy.data.texts.get("PDHQ_STAGE21_GEOMETRY_CLEANUP_REPORT") or bpy.data.texts.new("PDHQ_STAGE21_GEOMETRY_CLEANUP_REPORT")
    text.clear()
    text.write(json.dumps(report, indent=2))
    print("Stage 21 geometry cleanup audit:", {
        "meshes": len(meshes),
        "guide_review": len(guide_candidates),
        "near_zero_dimensions": len(zero_dimension),
        "non_manifold_candidates": len(non_manifold),
        "aabb_overlap_pairs": len(overlap_pairs),
        "overlap_scan_capped": capped,
    })


if __name__ == "__main__":
    main()
