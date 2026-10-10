"""Stage 22: visibility and streaming preparation audit for a Blender MLO scene.

This script creates review lists only. Blender collection membership and object
bounds are not a substitute for GTA V portals, occlusion, archetypes, or streaming.
It does not modify objects or generate Sollumz metadata.
"""
import bpy
import json
from mathutils import Vector

VISIBILITY_TOKENS = (
    "window", "glass", "glazing", "door", "interior", "lobby", "corridor",
    "stair", "elevator", "roof", "helipad", "garage", "cell", "booking",
    "dispatch", "evidence", "armory", "interview", "detective", "locker",
)
TEMP_TOKENS = ("guide", "proxy", "placeholder", "clearance", "blockout", "planning", "staging")


def collections_for(obj):
    return sorted(c.name for c in obj.users_collection)


def bounds_for(obj):
    try:
        corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        return {
            "min": [round(min(v[i] for v in corners), 3) for i in range(3)],
            "max": [round(max(v[i] for v in corners), 3) for i in range(3)],
        }
    except Exception:
        return None


def main():
    scene = bpy.context.scene
    objects = list(scene.objects)
    mesh_objects = [obj for obj in objects if obj.type == "MESH"]
    likely_temporary = []
    likely_visibility_assets = []
    collection_summary = {}
    mesh_rows = []
    for obj in objects:
        names = collections_for(obj)
        for name in names:
            collection_summary[name] = collection_summary.get(name, 0) + 1
        combined = (obj.name + " " + " ".join(names)).lower()
        if any(token in combined for token in TEMP_TOKENS):
            likely_temporary.append({
                "object": obj.name,
                "type": obj.type,
                "collections": names,
                "note": "Potential guide/proxy; manually confirm before excluding from export.",
            })
        if any(token in combined for token in VISIBILITY_TOKENS):
            likely_visibility_assets.append({
                "object": obj.name,
                "type": obj.type,
                "collections": names,
                "bounds": bounds_for(obj),
                "note": "Name-based candidate for visibility and streaming review, not an automatic portal/occlusion assignment.",
            })
        if obj.type == "MESH":
            mesh_rows.append({
                "object": obj.name,
                "collections": names,
                "bounds": bounds_for(obj),
                "dimensions": [round(float(v), 3) for v in obj.dimensions],
                "polygon_count": len(obj.data.polygons),
                "material_slots": len(obj.data.materials),
            })

    report = {
        "stage": 22,
        "scene": scene.name,
        "object_count": len(objects),
        "mesh_count": len(mesh_objects),
        "collection_object_counts": collection_summary,
        "potential_temporary_export_exclusions": likely_temporary,
        "visibility_and_streaming_review_candidates": likely_visibility_assets,
        "mesh_inventory": mesh_rows,
        "manual_review_plan": [
            "Define the intended MLO/interior boundary and the relationship to the exterior world before authoring portals.",
            "Review each doorway, corridor junction, window, stair opening, garage entrance, and roof access as a visibility transition.",
            "Decide which spaces should remain visible from each doorway and which walls or floors should occlude them.",
            "Use the current compatible Sollumz/CodeWalker workflow to author and inspect required archetype, room, portal, and occlusion data; do not infer these from Blender collections.",
            "Verify the map placement and remove or hide overlapping default GTA building geometry only through a deliberate map/interior setup, not by deleting unrelated base assets.",
            "Check texture paths, material/shader assignments, asset names, bounds, and resource manifest/stream folder configuration.",
            "Test fresh join, respawn, interior entry/exit, reconnect, different viewing angles, and multiple clients on the target FiveM server.",
        ],
        "limitations": [
            "This script does not create portals, occlusion geometry, MLO archetypes, collision, LODs, or streaming configuration.",
            "Name-based candidate discovery may miss incorrectly named assets and may include irrelevant assets.",
            "Blender scene structure alone cannot prove that textures stream, interiors remain visible, or default GTA geometry is suppressed in game.",
            "A successful report is not a production-export or FiveM validation result.",
        ],
    }
    text = bpy.data.texts.get("PDHQ_STAGE22_VISIBILITY_STREAMING_REPORT") or bpy.data.texts.new("PDHQ_STAGE22_VISIBILITY_STREAMING_REPORT")
    text.clear()
    text.write(json.dumps(report, indent=2))
    print("Stage 22 visibility/streaming review:", {
        "objects": len(objects),
        "meshes": len(mesh_objects),
        "temporary_candidates": len(likely_temporary),
        "visibility_candidates": len(likely_visibility_assets),
        "collections": len(collection_summary),
    })


if __name__ == "__main__":
    main()
