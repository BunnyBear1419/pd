"""Stage 20: non-destructive LOD and performance planning audit for Blender.

This creates a heuristic review report only. It does not build LOD meshes, change
objects, assign materials, or measure FiveM/GTA runtime performance.
"""
import bpy
import json
from math import prod
from mathutils import Vector

POLYGON_REVIEW_THRESHOLD = 5000
MATERIAL_SLOT_REVIEW_THRESHOLD = 4
SMALL_PROP_MAX_DIMENSION = 1.25


def object_collections(obj):
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


def max_dimension(obj):
    return max((float(v) for v in obj.dimensions), default=0.0)


def priority_for(obj, polygon_count):
    dim = max_dimension(obj)
    if polygon_count >= POLYGON_REVIEW_THRESHOLD:
        return "HIGH_POLYGON_REVIEW"
    if polygon_count >= 1500 and dim >= 4.0:
        return "MEDIUM_LOD_REVIEW"
    if dim <= SMALL_PROP_MAX_DIMENSION and polygon_count >= 500:
        return "SMALL_PROP_SIMPLIFICATION_REVIEW"
    if dim >= 15.0 and polygon_count >= 500:
        return "LARGE_ASSET_DISTANCE_LOD_REVIEW"
    return "STANDARD_MANUAL_REVIEW"


def main():
    scene = bpy.context.scene
    objects = list(scene.objects)
    meshes = [obj for obj in objects if obj.type == "MESH"]
    material_usage = {}
    rows = []
    high_poly = []
    many_slots = []
    unapplied_scale = []
    modifiers = []
    no_material = []

    for obj in meshes:
        polygons = len(obj.data.polygons)
        materials = [mat.name if mat else None for mat in obj.data.materials]
        for material_name in materials:
            if material_name:
                material_usage[material_name] = material_usage.get(material_name, 0) + 1
        priority = priority_for(obj, polygons)
        row = {
            "object": obj.name,
            "collections": object_collections(obj),
            "vertices": len(obj.data.vertices),
            "polygons": polygons,
            "dimensions": [round(float(v), 3) for v in obj.dimensions],
            "max_dimension": round(max_dimension(obj), 3),
            "world_bounds": world_bounds(obj),
            "material_slots": len(obj.data.materials),
            "materials": materials,
            "modifier_types": [m.type for m in obj.modifiers],
            "object_scale": [round(float(v), 4) for v in obj.scale],
            "lod_review_priority": priority,
            "recommendation": (
                "Inspect silhouette and remove hidden/internal geometry before considering a manual LOD."
                if priority in ("HIGH_POLYGON_REVIEW", "MEDIUM_LOD_REVIEW", "LARGE_ASSET_DISTANCE_LOD_REVIEW")
                else "Check whether this object is visible at distance and whether its detail is necessary."
            ),
        }
        rows.append(row)
        if polygons >= POLYGON_REVIEW_THRESHOLD:
            high_poly.append({"object": obj.name, "polygons": polygons, "priority": priority})
        if len(obj.data.materials) >= MATERIAL_SLOT_REVIEW_THRESHOLD:
            many_slots.append({"object": obj.name, "material_slots": len(obj.data.materials)})
        if any(abs(float(v) - 1.0) > 0.001 for v in obj.scale):
            unapplied_scale.append({"object": obj.name, "scale": row["object_scale"]})
        if len(obj.modifiers):
            modifiers.append({"object": obj.name, "modifiers": [m.name + ":" + m.type for m in obj.modifiers]})
        if not any(materials):
            no_material.append(obj.name)

    all_material_names = sorted(mat.name for mat in bpy.data.materials)
    unused_materials = [name for name in all_material_names if material_usage.get(name, 0) == 0]
    rows.sort(key=lambda r: (-r["polygons"], r["object"].lower()))
    manifest = [{
        "object": row["object"],
        "collections": row["collections"],
        "polygons": row["polygons"],
        "lod_review_priority": row["lod_review_priority"],
        "suggested_action": row["recommendation"],
        "automatically_modified": False,
    } for row in rows]

    report = {
        "stage": 20,
        "scene": scene.name,
        "object_count": len(objects),
        "mesh_count": len(meshes),
        "polygon_count_total": sum(len(obj.data.polygons) for obj in meshes),
        "high_polygon_review_count": len(high_poly),
        "objects_with_many_material_slots_count": len(many_slots),
        "mesh_objects_with_non_unit_scale_count": len(unapplied_scale),
        "mesh_objects_with_modifiers_count": len(modifiers),
        "mesh_objects_without_materials": no_material,
        "materials_without_mesh_slot_users": unused_materials,
        "material_slot_user_counts": material_usage,
        "high_polygon_objects": high_poly,
        "objects_with_many_material_slots": many_slots,
        "non_unit_scale_objects": unapplied_scale,
        "objects_with_modifiers": modifiers,
        "mesh_inventory_sorted_by_polygon_count": rows,
        "limitations": [
            "Polygon and size thresholds are heuristics, not platform budgets or measured performance.",
            "No LOD geometry is generated and no source objects are modified.",
            "Material usage counts mesh slots, not draw calls or final GTA shader batches.",
            "Blender scene metrics do not establish FiveM frame time, streaming memory, collision cost, or network impact.",
            "Create and validate LODs, material atlases, collision, occlusion, portals, and Sollumz exports manually; test in game at representative distances.",
        ],
    }
    report_text = bpy.data.texts.get("PDHQ_STAGE20_LOD_PERFORMANCE_REPORT") or bpy.data.texts.new("PDHQ_STAGE20_LOD_PERFORMANCE_REPORT")
    report_text.clear()
    report_text.write(json.dumps(report, indent=2))
    manifest_text = bpy.data.texts.get("PDHQ_STAGE20_LOD_MANIFEST") or bpy.data.texts.new("PDHQ_STAGE20_LOD_MANIFEST")
    manifest_text.clear()
    manifest_text.write(json.dumps(manifest, indent=2))
    print("Stage 20 LOD/performance review:", {
        "meshes": len(meshes),
        "total_polygons": report["polygon_count_total"],
        "high_poly_review": len(high_poly),
        "many_material_slots": len(many_slots),
        "unused_materials": len(unused_materials),
    })


if __name__ == "__main__":
    main()
