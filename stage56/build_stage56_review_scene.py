#!/usr/bin/env python3
"""Build a unified Blender REVIEW BLOCKOUT from Stage 42-45 manifests.

Run from repository root:
  blender --background --python stage56/build_stage56_review_scene.py -- --output build/pdhq_stage56_review.blend

This assembles schematic boxes, review materials, and placeholder lights. It is not a GTA-ready MLO.
It never deletes existing collections or writes over an existing output unless --overwrite-output is used.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

import bpy

MATERIAL_MANIFEST = "build/stage45_material_manifest.json"
INPUTS = {
    "shell": ("build/stage42_shell_geometry.json", 42, "geometry"),
    "furniture": ("build/stage43_furniture_blockout.json", 43, "geometry"),
    "lighting": ("build/stage44_lighting_manifest.json", 44, "lights"),
    "materials": (MATERIAL_MANIFEST, 45, "materials"),
}

def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", default="build/pdhq_stage56_review.blend")
    ap.add_argument("--overwrite-output", action="store_true")
    ap.add_argument("--collection-prefix", default="PDHQ_STAGE56_REVIEW")
    return ap.parse_args(argv)

def load_inputs(root: Path):
    loaded = {}
    for key, (rel, stage, list_key) in INPUTS.items():
        path = root / rel
        if not path.is_file():
            raise SystemExit(f"Required Stage {stage} manifest missing: {path}. Run that stage's generator first.")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON in {path}: {exc}")
        if data.get("stage") != stage or data.get("production_ready") is not False:
            raise SystemExit(f"Refusing unexpected or production-ready input: {path}")
        if not isinstance(data.get(list_key), list):
            raise SystemExit(f"Expected a list named {list_key!r} in {path}")
        loaded[key] = data
    return loaded

def make_collection(name):
    existing = bpy.data.collections.get(name)
    if existing:
        raise SystemExit(f"Collection {name!r} already exists; save a copy and use a fresh --collection-prefix.")
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)
    return collection

def create_materials(data, prefix):
    result = {}
    for item in data["materials"]:
        name = str(item["name"])
        mat = bpy.data.materials.get(name)
        if mat is None:
            mat = bpy.data.materials.new(name)
        mat.diffuse_color = tuple(item["base_color"])
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF") if mat.node_tree else None
        if bsdf:
            bsdf.inputs["Base Color"].default_value = tuple(item["base_color"])
            bsdf.inputs["Roughness"].default_value = float(item["roughness"])
            bsdf.inputs["Metallic"].default_value = float(item["metallic"])
        mat["PDHQ_STAGE56_REVIEW"] = True
        mat["PDHQ_production_ready"] = False
        result[name] = mat
    return result

def choose_material(item, materials, is_furniture=False):
    text = " ".join(str(item.get(k, "")) for k in ("role", "name", "use", "note")).lower()
    if is_furniture:
        if any(t in text for t in ("cell", "bunk", "sanitary", "shower", "locker")):
            wanted = "PDHQ_Stainless_Steel"
        elif any(t in text for t in ("garage", "vehicle", "safety", "tactical")):
            wanted = "PDHQ_Safety_Yellow" if "safety" in text else "PDHQ_Painted_Dark"
        else:
            wanted = "PDHQ_Painted_White"
    elif any(t in text for t in ("floor_slab", "concrete", "foundation")):
        wanted = "PDHQ_Concrete"
    elif any(t in text for t in ("door_lintel", "wall_segment")):
        wanted = "PDHQ_Concrete"
    elif any(t in text for t in ("coreplaceholder", "placeholder")):
        wanted = "PDHQ_Safety_Yellow"
    else:
        wanted = "PDHQ_Plaster"
    return materials.get(wanted) or next(iter(materials.values()))

def add_box(item, collection, materials, furniture=False):
    center = item.get("center_m")
    size = item.get("size_m")
    if not (isinstance(center, list) and len(center) == 3 and
            isinstance(size, list) and len(size) == 3):
        raise ValueError(f"Invalid center_m/size_m on {item.get('name', '<unnamed>')}")
    if any(not isinstance(v, (int, float)) for v in center + size) or any(v <= 0 for v in size):
        raise ValueError(f"Invalid dimensions on {item.get('name', '<unnamed>')}")
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=tuple(center))
    obj = bpy.context.object
    obj.name = str(item.get("name", "PDHQ_Blockout"))
    obj.dimensions = tuple(size)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for owner in list(obj.users_collection):
        owner.objects.unlink(obj)
    collection.objects.link(obj)
    mat = choose_material(item, materials, furniture)
    obj.data.materials.append(mat)
    obj["PDHQ_stage56_role"] = str(item.get("role", "furniture_placeholder" if furniture else "shell_blockout"))
    obj["PDHQ_production_ready"] = False
    for key in ("floor", "room_id", "use", "note"):
        if key in item and item[key] is not None:
            obj["PDHQ_" + key] = str(item[key])
    return obj

def add_lights(data, collection):
    created = 0
    for item in data["lights"]:
        loc = item.get("location_m")
        if not isinstance(loc, list) or len(loc) != 3:
            continue
        kind = item.get("type", "AREA")
        if kind not in {"AREA", "POINT", "SPOT", "SUN"}:
            continue
        light_data = bpy.data.lights.new(str(item.get("name", f"ReviewLight_{created}")), type=kind)
        light_data.energy = max(0.0, float(item.get("power_w", 400.0)))
        if kind == "AREA":
            light_data.shape = "DISK"
            light_data.size = max(0.1, float(item.get("size_m", 1.0)))
        light_data.color = tuple(item.get("color_rgb", [1.0, 1.0, 1.0]))
        obj = bpy.data.objects.new(light_data.name, light_data)
        obj.location = tuple(loc)
        collection.objects.link(obj)
        obj["PDHQ_production_ready"] = False
        obj["PDHQ_role"] = str(item.get("role", "review_light"))
        created += 1
    return created

def add_review_camera(scene, collection):
    data = bpy.data.cameras.new("PDHQ_Stage56_ReviewCamera")
    camera = bpy.data.objects.new("PDHQ_Stage56_ReviewCamera", data)
    collection.objects.link(camera)
    camera.location = (38.0, -46.0, 32.0)
    target = (0.0, 0.0, 5.0)
    direction = __import__("mathutils").Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    data.lens = 42
    scene.camera = camera
    camera["PDHQ_production_ready"] = False

def main():
    args = parse_args()
    root = Path.cwd()
    output = Path(args.output).expanduser()
    if not output.is_absolute():
        output = root / output
    output = output.resolve()
    if output.exists() and not args.overwrite_output:
        raise SystemExit(f"Output already exists: {output}. Use --overwrite-output only if you intend to replace it.")
    inputs = load_inputs(root)
    prefix = args.collection_prefix
    shell_collection = make_collection(prefix + "_SHELL")
    furniture_collection = make_collection(prefix + "_FURNITURE")
    lighting_collection = make_collection(prefix + "_LIGHTS")
    camera_collection = make_collection(prefix + "_CAMERA")
    materials = create_materials(inputs["materials"], prefix)
    shell_count = 0
    for item in inputs["shell"]["geometry"]:
        add_box(item, shell_collection, materials)
        shell_count += 1
    furniture_count = 0
    for item in inputs["furniture"]["geometry"]:
        add_box(item, furniture_collection, materials, furniture=True)
        furniture_count += 1
    light_count = add_lights(inputs["lighting"], lighting_collection)
    add_review_camera(bpy.context.scene, camera_collection)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES" if "CYCLES" in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items.keys() else scene.render.engine
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 50
    scene["PDHQ_STAGE56_REVIEW_SCENE"] = True
    scene["PDHQ_production_ready"] = False
    scene["PDHQ_stage56_summary"] = json.dumps({"shell_objects": shell_count, "furniture_objects": furniture_count,
                                                "review_lights": light_count, "production_ready": False})
    output.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(output))
    print(json.dumps({"output": str(output), "shell_objects": shell_count,
                      "furniture_objects": furniture_count, "review_lights": light_count,
                      "production_ready": False,
                      "note": "Schematic Blender review blockout only; not a GTA-ready MLO."}, indent=2))

if __name__ == "__main__":
    main()
