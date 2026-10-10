"""Stage 19: non-destructive collision/export preflight audit for the active Blender scene.

This does not generate GTA collision meshes or export assets. It inventories likely
collision candidates and temporary guide geometry, then writes review reports.
"""
import bpy
import json
from mathutils import Vector

GUIDE_TOKENS = (
    "guide", "clearance", "proxy", "placeholder", "planning", "staging",
    "approach", "route", "transfer", "bay_line", "crossing", "review_envelope",
)
COLLISION_TOKENS = ("collision", "coll", "bound", "physics")
EXPORT_EXCLUDE_COLLECTION_TOKENS = (
    "GUIDE", "PROXY", "BLOCKOUT", "ACCESS_GUIDES", "CIRCULATION_GUIDES",
    "SITE_SECURITY_LANDSCAPE_GUIDES",
)

def object_collections(obj):
    return [c.name for c in obj.users_collection]

def world_bounds(obj):
    try:
        corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        return {
            "min": [round(min(v[i] for v in corners), 3) for i in range(3)],
            "max": [round(max(v[i] for v in corners), 3) for i in range(3)],
        }
    except Exception:
        return None

def is_guide_candidate(obj, collection_names):
    combined = (obj.name + " " + " ".join(collection_names)).upper()
    return any(token.upper() in combined for token in GUIDE_TOKENS + EXPORT_EXCLUDE_COLLECTION_TOKENS)

def is_collision_candidate(obj, collection_names):
    combined = (obj.name + " " + " ".join(collection_names)).lower()
    return obj.get("PDHQ_collision_candidate", False) or any(t in combined for t in COLLISION_TOKENS)

def main():
    scene = bpy.context.scene
    objects = list(scene.objects)
    mesh_objects = [o for o in objects if o.type == "MESH"]
    guide_candidates = []
    collision_candidates = []
    no_material = []
    unapplied_scale = []
    modifiers = []
    mesh_rows = []

    for obj in objects:
        collections = object_collections(obj)
        guide = is_guide_candidate(obj, collections)
        collision = is_collision_candidate(obj, collections)
        if guide:
            guide_candidates.append({
                "name": obj.name, "type": obj.type, "collections": collections,
                "reason": "Name/collection suggests temporary guide or proxy; manually confirm.",
            })
        if collision:
            collision_candidates.append({
                "name": obj.name, "type": obj.type, "collections": collections,
                "dimensions": [round(float(v), 3) for v in obj.dimensions],
                "note": "Candidate only; verify geometry and Sollumz collision flags manually.",
            })
        if obj.type == "MESH":
            if len(obj.data.materials) == 0:
                no_material.append(obj.name)
            scale = [float(v) for v in obj.scale]
            if any(abs(v - 1.0) > 0.001 for v in scale):
                unapplied_scale.append({"name": obj.name, "scale": [round(v, 4) for v in scale]})
            if len(obj.modifiers):
                modifiers.append({"name": obj.name, "modifiers": [m.name + ":" + m.type for m in obj.modifiers]})
            mesh_rows.append({
                "name": obj.name,
                "collections": collections,
                "vertices": len(obj.data.vertices),
                "polygons": len(obj.data.polygons),
                "material_slots": len(obj.data.materials),
                "dimensions": [round(float(v), 3) for v in obj.dimensions],
                "world_bounds": world_bounds(obj),
                "guide_candidate": guide,
                "collision_candidate": collision,
            })

    # Export manifest is deliberately advisory: it never hides, deletes, or exports objects.
    manifest = []
    for obj in sorted(objects, key=lambda item: item.name.lower()):
        collections = object_collections(obj)
        if is_guide_candidate(obj, collections):
            disposition = "REVIEW_EXCLUDE_TEMPORARY_GUIDE"
        elif is_collision_candidate(obj, collections):
            disposition = "REVIEW_COLLISION_CANDIDATE"
        else:
            disposition = "REVIEW_FOR_FINAL_EXPORT"
        manifest.append({
            "object": obj.name,
            "type": obj.type,
            "collections": collections,
            "suggested_disposition": disposition,
        })

    report = {
        "stage": 19,
        "scene": scene.name,
        "object_count": len(objects),
        "mesh_count": len(mesh_objects),
        "polygon_count_total": sum(len(o.data.polygons) for o in mesh_objects),
        "guide_or_proxy_review_count": len(guide_candidates),
        "collision_candidate_count": len(collision_candidates),
        "mesh_objects_without_materials": no_material,
        "mesh_objects_with_non_unit_object_scale": unapplied_scale,
        "mesh_objects_with_modifiers": modifiers,
        "guide_or_proxy_candidates": guide_candidates,
        "collision_candidates": collision_candidates,
        "mesh_inventory": mesh_rows,
        "important_limit": "Advisory preflight only; not a GTA collision, occlusion, portal, LOD, shader, or export validator.",
    }
    report_text = bpy.data.texts.get("PDHQ_STAGE19_EXPORT_PREFLIGHT_REPORT") or bpy.data.texts.new("PDHQ_STAGE19_EXPORT_PREFLIGHT_REPORT")
    report_text.clear()
    report_text.write(json.dumps(report, indent=2))
    manifest_text = bpy.data.texts.get("PDHQ_STAGE19_EXPORT_MANIFEST") or bpy.data.texts.new("PDHQ_STAGE19_EXPORT_MANIFEST")
    manifest_text.clear()
    manifest_text.write(json.dumps(manifest, indent=2))
    print("Stage 19 preflight:", {
        "objects": len(objects),
        "meshes": len(mesh_objects),
        "guide_review": len(guide_candidates),
        "collision_review": len(collision_candidates),
        "no_material": len(no_material),
    })

if __name__ == "__main__":
    main()
