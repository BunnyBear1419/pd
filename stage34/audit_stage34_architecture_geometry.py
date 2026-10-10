"""Stage 34: non-destructive architecture and geometry review for Blender.

Run inside Blender after the scene generators. All findings are heuristic candidates
for human inspection; this script never modifies or deletes scene objects.
"""
import json
from datetime import datetime, timezone

import bpy
from mathutils import Vector

REPORT_NAME = "PDHQ_STAGE34_ARCHITECTURE_GEOMETRY_REPORT"
REQUIRED_NAME_HINTS = ("WALL", "SLAB", "STAIR", "ELEVATOR", "HELIPAD", "GARAGE")
ZERO_EPSILON = 0.001


def world_bounds(obj):
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return {
        "min": [round(min(v[i] for v in corners), 3) for i in range(3)],
        "max": [round(max(v[i] for v in corners), 3) for i in range(3)],
        "size": [round(max(v[i] for v in corners) - min(v[i] for v in corners), 3) for i in range(3)],
    }


def overlap_volume(a, b):
    overlap = [min(a["max"][i], b["max"][i]) - max(a["min"][i], b["min"][i]) for i in range(3)]
    if any(value <= ZERO_EPSILON for value in overlap):
        return 0.0
    return round(overlap[0] * overlap[1] * overlap[2], 3)


def main():
    objects = list(bpy.context.scene.objects)
    meshes = [obj for obj in objects if obj.type == "MESH"]
    collections = {}
    zero_dimension = []
    large_bounds = []
    name_hints = {hint: [] for hint in REQUIRED_NAME_HINTS}
    bounds_by_name = {}

    for obj in objects:
        collection_names = sorted(collection.name for collection in obj.users_collection)
        for name in collection_names or ["(unlinked)"]:
            collections.setdefault(name, {"objects": 0, "meshes": 0, "polygons": 0})
            collections[name]["objects"] += 1
            if obj.type == "MESH":
                collections[name]["meshes"] += 1
                collections[name]["polygons"] += len(obj.data.polygons)

        if obj.type != "MESH":
            continue
        bounds = world_bounds(obj)
        bounds_by_name[obj.name] = bounds
        if any(dimension <= ZERO_EPSILON for dimension in bounds["size"]):
            zero_dimension.append({"object": obj.name, "size": bounds["size"], "collections": collection_names})
        if max(bounds["size"]) > 60:
            large_bounds.append({"object": obj.name, "size": bounds["size"], "collections": collection_names})
        upper = obj.name.upper()
        for hint in REQUIRED_NAME_HINTS:
            if hint in upper:
                name_hints[hint].append(obj.name)

    # Only report strong volumetric AABB overlaps between likely structural meshes.
    # Furniture, guide, collision, door, trim and proxy objects are excluded to reduce noise.
    structural = []
    excluded_tokens = ("GUIDE", "CLEARANCE", "PROXY", "FURNITURE", "DESK", "CHAIR",
                       "DOOR", "FRAME", "TRIM", "SIGN", "LIGHT", "WINDOW", "COLLISION")
    for obj in meshes:
        upper = obj.name.upper()
        if any(token in upper for token in excluded_tokens):
            continue
        if any(token in upper for token in ("WALL", "SLAB", "COLUMN", "BEAM", "STAIR", "ROOF", "HELIPAD")):
            structural.append(obj)
    overlaps = []
    for i, first in enumerate(structural):
        a = bounds_by_name[first.name]
        for second in structural[i + 1:]:
            # Shared collection is often an intentional modular assembly; still record only material overlaps.
            b = bounds_by_name[second.name]
            volume = overlap_volume(a, b)
            if volume >= 0.25:
                overlaps.append({
                    "object_a": first.name,
                    "object_b": second.name,
                    "overlap_volume_m3_estimate": volume,
                    "collections_a": sorted(c.name for c in first.users_collection),
                    "collections_b": sorted(c.name for c in second.users_collection),
                    "severity": "REVIEW_CANDIDATE",
                })
                if len(overlaps) >= 250:
                    break
        if len(overlaps) >= 250:
            break

    report = {
        "stage": 34,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "scene": bpy.context.scene.name,
        "status": "REVIEW_REQUIRED",
        "production_ready": False,
        "counts": {"objects": len(objects), "mesh_objects": len(meshes),
                   "estimated_scene_polygons": sum(len(obj.data.polygons) for obj in meshes)},
        "collection_summary": collections,
        "key_name_hints": name_hints,
        "zero_or_near_zero_world_dimensions": zero_dimension,
        "unusually_large_world_bounds_over_60m": large_bounds,
        "structural_aabb_overlap_candidates": overlaps,
        "overlap_candidate_limit": 250,
        "interpretation": [
            "Axis-aligned bounding boxes are coarse screening, not exact mesh intersection tests.",
            "Intentional wall/slab joins and modular construction may appear as overlaps.",
            "Absence of a finding does not prove clearances, structural soundness, or correct collision.",
            "Key-name matches are naming hints only, not proof that a required facility is complete.",
            "No scene objects, transforms, meshes, modifiers, materials, or collections were changed."
        ],
    }
    block = bpy.data.texts.get(REPORT_NAME) or bpy.data.texts.new(REPORT_NAME)
    block.clear()
    block.write(json.dumps(report, indent=2))
    print("[PDHQ Stage 34] Non-destructive architecture review written to " + REPORT_NAME)
    print("[PDHQ Stage 34] Objects: %d; meshes: %d; overlap candidates: %d" %
          (len(objects), len(meshes), len(overlaps)))


if __name__ == "__main__":
    main()
