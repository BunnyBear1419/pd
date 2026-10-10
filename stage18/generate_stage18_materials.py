"""Stage 18: create a reusable, lightweight material library in the active Blender scene.

Run after Stages 2-17. Shared materials are created only by default; geometry is
not replaced or automatically repainted. Set AUTO_ASSIGN=True to enable optional
conservative name-based assignment after reviewing the keyword map.
"""
import bpy
import json

CONFIG = {
    "AUTO_ASSIGN": False,
    "COLLECTION_PREFIXES": ("PDHQ_",),
    "MATERIALS": {
        "PDHQ_MAT_Concrete_Light": ((0.48, 0.50, 0.51, 1.0), 0.82, 0.0),
        "PDHQ_MAT_Concrete_Dark": ((0.22, 0.25, 0.27, 1.0), 0.88, 0.0),
        "PDHQ_MAT_Glass_Tint": ((0.055, 0.20, 0.27, 1.0), 0.22, 0.0),
        "PDHQ_MAT_Aluminum": ((0.34, 0.39, 0.42, 1.0), 0.32, 0.72),
        "PDHQ_MAT_Black_Metal": ((0.035, 0.045, 0.052, 1.0), 0.42, 0.45),
        "PDHQ_MAT_Interior_Wall": ((0.72, 0.74, 0.73, 1.0), 0.88, 0.0),
        "PDHQ_MAT_Floor_Stone": ((0.36, 0.39, 0.40, 1.0), 0.65, 0.0),
        "PDHQ_MAT_Floor_Secure": ((0.16, 0.20, 0.22, 1.0), 0.72, 0.0),
        "PDHQ_MAT_Agency_Primary": ((0.035, 0.13, 0.20, 1.0), 0.48, 0.18),
        "PDHQ_MAT_Agency_Accent": ((0.80, 0.39, 0.10, 1.0), 0.42, 0.22),
        "PDHQ_MAT_Signage_Back": ((0.025, 0.035, 0.045, 1.0), 0.55, 0.15),
        "PDHQ_MAT_Guide_Yellow": ((0.95, 0.62, 0.04, 1.0), 0.6, 0.0),
        "PDHQ_MAT_Landscape": ((0.12, 0.25, 0.14, 1.0), 0.92, 0.0),
        "PDHQ_MAT_Roof_Membrane": ((0.17, 0.19, 0.20, 1.0), 0.82, 0.0),
    },
}

def make_material(name, rgba, roughness, metallic):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = rgba
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = rgba
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    mat["PDHQ_stage"] = 18
    mat["PDHQ_role"] = name.replace("PDHQ_MAT_", "").replace("_", " ")
    return mat

def material_for_object(obj):
    name = obj.name.lower()
    if any(word in name for word in ("glass", "glazing", "window", "vision_panel")):
        return "PDHQ_MAT_Glass_Tint"
    if any(word in name for word in ("sign", "plaque", "directory", "emblem", "crest", "badge")):
        return "PDHQ_MAT_Signage_Back"
    if any(word in name for word in ("bollard", "mullion", "metal", "reader", "handle", "fence", "gate")):
        return "PDHQ_MAT_Black_Metal"
    if any(word in name for word in ("yellow", "clearance", "guide", "bay_line", "crossing")):
        return "PDHQ_MAT_Guide_Yellow"
    if any(word in name for word in ("landscape", "plant", "bed", "tree", "grass")):
        return "PDHQ_MAT_Landscape"
    if any(word in name for word in ("roof", "helipad", "hvac")):
        return "PDHQ_MAT_Roof_Membrane"
    if any(word in name for word in ("desk", "cabinet", "console", "locker", "furniture")):
        return "PDHQ_MAT_Floor_Secure"
    if any(word in name for word in ("floor", "slab", "apron", "pavement", "landing")):
        return "PDHQ_MAT_Floor_Stone"
    if any(word in name for word in ("wall", "partition", "interior", "lobby")):
        return "PDHQ_MAT_Interior_Wall"
    if any(word in name for word in ("accent", "stripe", "primary")):
        return "PDHQ_MAT_Agency_Accent"
    return "PDHQ_MAT_Concrete_Light"

def main():
    materials = {name: make_material(name, rgba, roughness, metallic)
                 for name, (rgba, roughness, metallic) in CONFIG["MATERIALS"].items()}
    assigned = 0
    eligible = 0
    if CONFIG["AUTO_ASSIGN"]:
        prefixes = CONFIG["COLLECTION_PREFIXES"]
        for obj in bpy.context.scene.objects:
            if obj.type != "MESH":
                continue
            if not any(col.name.startswith(prefixes) for col in obj.users_collection):
                continue
            eligible += 1
            mat = materials[material_for_object(obj)]
            if len(obj.data.materials) == 0:
                obj.data.materials.append(mat)
            else:
                obj.data.materials[0] = mat
            assigned += 1
    report = {
        "stage": 18,
        "material_count": len(materials),
        "auto_assign_enabled": CONFIG["AUTO_ASSIGN"],
        "eligible_mesh_count": eligible,
        "assigned_mesh_count": assigned,
        "note": "Shared material library created; review surfaces and export settings in Blender/Sollumz.",
    }
    text_block = bpy.data.texts.get("PDHQ_STAGE18_MATERIAL_REPORT") or bpy.data.texts.new("PDHQ_STAGE18_MATERIAL_REPORT")
    text_block.clear()
    text_block.write(json.dumps(report, indent=2))
    print("Stage 18 material library:", report)

if __name__ == "__main__":
    main()
