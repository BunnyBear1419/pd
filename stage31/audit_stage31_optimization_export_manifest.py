"""Stage 31: non-destructive optimization and production-export manifest.

Run inside Blender after the Stage 25 scene build. It does not delete, hide,
join, decimate, apply modifiers, change materials, or export GTA assets.
"""
import bpy
import csv
import io
import json
from mathutils import Vector

REPORT_NAME = "PDHQ_STAGE31_OPTIMIZATION_EXPORT_REPORT"
MANIFEST_NAME = "PDHQ_STAGE31_EXPORT_MANIFEST_CSV"
GUIDE_TOKENS = (
    "guide", "clearance", "proxy", "placeholder", "planning", "staging",
    "approach", "route", "transfer", "bay_line", "crossing", "review_envelope",
    "blockout", "zone_label", "collision_proxy", "review",
)
COLLECTION_EXCLUDE_TOKENS = (
    "GUIDE", "PROXY", "BLOCKOUT", "CIRCULATION_REVIEW",
    "ACCESS_GUIDES", "SITE_SECURITY_LANDSCAPE_GUIDES",
    "GARAGE_CIRCULATION_GUIDES", "GARAGE_SECURE_REVIEW",
)


def collection_names(obj):
    return sorted(collection.name for collection in obj.users_collection)


def world_bounds(obj):
    try:
        points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        return {
            "min": [round(min(point[axis] for point in points), 3) for axis in range(3)],
            "max": [round(max(point[axis] for point in points), 3) for axis in range(3)],
        }
    except Exception:
        return None


def classify(obj):
    collections = collection_names(obj)
    combined = (obj.name + " " + " ".join(collections)).upper()
    if any(token in combined for token in COLLECTION_EXCLUDE_TOKENS):
        return "REVIEW_EXCLUDE_OR_CONVERT_GUIDE"
    if any(token.upper() in combined for token in GUIDE_TOKENS):
        return "REVIEW_EXCLUDE_OR_CONVERT_GUIDE"
    if obj.type == "MESH" and ("COLLISION" in combined or "COLL" in combined or obj.get("PDHQ_collision_candidate", False)):
        return "REVIEW_COLLISION_ASSET"
    if obj.type == "MESH":
        return "REVIEW_RENDER_ASSET"
    return "REVIEW_NONMESH_DEPENDENCY"


def main():
    scene = bpy.context.scene
    objects = sorted(list(scene.objects), key=lambda item: item.name.casefold())
    rows = []
    collection_stats = {}
    material_users = {}
    total_polygons = 0
    high_poly = []
    modifiers = []
    non_unit_scale = []
    no_materials = []
    guides = []
    collision = []

    for obj in objects:
        collections = collection_names(obj)
        disposition = classify(obj)
        polygon_count = len(obj.data.polygons) if obj.type == "MESH" else 0
        vertex_count = len(obj.data.vertices) if obj.type == "MESH" else 0
        total_polygons += polygon_count
        materials = [mat.name if mat else "" for mat in obj.data.materials] if obj.type == "MESH" else []
        for material_name in materials:
            if material_name:
                material_users[material_name] = material_users.get(material_name, 0) + 1
        row = {
            "object": obj.name, "type": obj.type, "collections": collections,
            "suggested_disposition": disposition, "vertices": vertex_count,
            "polygons": polygon_count,
            "dimensions": [round(float(value), 3) for value in obj.dimensions],
            "world_bounds": world_bounds(obj), "materials": materials,
            "modifier_types": [modifier.type for modifier in obj.modifiers],
            "scale": [round(float(value), 4) for value in obj.scale],
            "automatic_changes": False,
        }
        rows.append(row)
        for collection in collections:
            stat = collection_stats.setdefault(collection, {"objects": 0, "meshes": 0, "polygons": 0})
            stat["objects"] += 1
            if obj.type == "MESH":
                stat["meshes"] += 1
                stat["polygons"] += polygon_count
        if disposition == "REVIEW_EXCLUDE_OR_CONVERT_GUIDE":
            guides.append(obj.name)
        if disposition == "REVIEW_COLLISION_ASSET":
            collision.append(obj.name)
        if obj.type == "MESH" and polygon_count >= 1500:
            high_poly.append({"object": obj.name, "polygons": polygon_count, "collections": collections})
        if obj.type == "MESH" and obj.modifiers:
            modifiers.append({"object": obj.name, "modifiers": [modifier.name + ":" + modifier.type for modifier in obj.modifiers]})
        if obj.type == "MESH" and any(abs(float(value) - 1.0) > 0.001 for value in obj.scale):
            non_unit_scale.append({"object": obj.name, "scale": row["scale"]})
        if obj.type == "MESH" and not any(materials):
            no_materials.append(obj.name)

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["object", "type", "collections", "suggested_disposition", "vertices", "polygons", "dimensions_xyz", "material_names", "modifier_types", "scale_xyz", "automatic_changes"])
    for row in rows:
        writer.writerow([
            row["object"], row["type"], ";".join(row["collections"]),
            row["suggested_disposition"], row["vertices"], row["polygons"],
            "x".join(str(value) for value in row["dimensions"]),
            ";".join(row["materials"]), ";".join(row["modifier_types"]),
            "x".join(str(value) for value in row["scale"]), "false",
        ])
    csv_text = bpy.data.texts.get(MANIFEST_NAME) or bpy.data.texts.new(MANIFEST_NAME)
    csv_text.clear()
    csv_text.write(buffer.getvalue())

    report = {
        "stage": 31, "scene": scene.name, "object_count": len(objects),
        "mesh_count": sum(1 for obj in objects if obj.type == "MESH"),
        "polygon_count_total": total_polygons,
        "guide_or_proxy_review_count": len(guides),
        "collision_asset_review_count": len(collision),
        "mesh_objects_over_1500_polygons_count": len(high_poly),
        "mesh_objects_with_modifiers_count": len(modifiers),
        "mesh_objects_with_non_unit_scale_count": len(non_unit_scale),
        "mesh_objects_without_materials_count": len(no_materials),
        "material_mesh_slot_users": material_users,
        "collection_statistics": collection_stats,
        "high_polygon_review": high_poly, "modifier_review": modifiers,
        "non_unit_scale_review": non_unit_scale, "missing_material_review": no_materials,
        "suggested_export_manifest": rows,
        "manual_next_actions": [
            "Back up the .blend file before any cleanup or optimization.",
            "Review guide/proxy suggestions object-by-object; never exclude solely by name.",
            "Resolve duplicate/hidden/internal geometry only after checking visible and collision roles.",
            "Reduce detail and material variety selectively; use visual comparison and measure the actual export.",
            "Apply transforms only when safe for the current workflow; inspect object origins and modifier results.",
            "Build appropriate collision and LOD assets with compatible Sollumz tooling; this report does not create them.",
            "Export a test batch and inspect it in CodeWalker before exporting the full building.",
            "Record in-game streaming/performance tests on the target FiveM server.",
        ],
        "limitations": [
            "The manifest is advisory; every object requires a human export-inclusion decision.",
            "Polygon counts are Blender mesh polygon counts, not measured GTA draw calls, memory, or FiveM frame time.",
            "No mesh optimization, deletion, modifier application, collision generation, LOD creation, or GTA export occurs.",
        ],
    }
    report_text = bpy.data.texts.get(REPORT_NAME) or bpy.data.texts.new(REPORT_NAME)
    report_text.clear()
    report_text.write(json.dumps(report, indent=2))
    print("Stage 31 optimization/export review:", {
        "objects": len(objects), "meshes": report["mesh_count"],
        "polygons": total_polygons, "guide_review": len(guides),
        "high_polygon_review": len(high_poly), "manifest": MANIFEST_NAME,
    })


if __name__ == "__main__":
    main()
