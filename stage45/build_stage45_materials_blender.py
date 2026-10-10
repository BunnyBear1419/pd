"""Run inside Blender: create review materials from Stage 45 JSON manifest.
Usage: blender --background scene.blend --python stage45/build_stage45_materials_blender.py -- --manifest build/stage45_material_manifest.json
Does not create geometry, GTA shaders, textures, or overwrite existing materials by default.
"""
import argparse, json, sys
from pathlib import Path
import bpy

def main():
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",default="build/stage45_material_manifest.json")
    ap.add_argument("--replace-prefix",action="store_true",help="replace only materials carrying PDHQ_STAGE45_REVIEW=True")
    args=ap.parse_args(argv)
    data=json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    if data.get("stage")!=45 or data.get("production_ready") is not False:
        raise SystemExit("Refusing unexpected or production-ready manifest")
    if args.replace_prefix:
        for mat in list(bpy.data.materials):
            if mat.get("PDHQ_STAGE45_REVIEW") is True:
                bpy.data.materials.remove(mat)
    created=0; reused=0
    for item in data["materials"]:
        mat=bpy.data.materials.get(item["name"])
        if mat is None:
            mat=bpy.data.materials.new(item["name"]); created+=1
        else:
            reused+=1
        mat.diffuse_color=tuple(item["base_color"])
        mat.use_nodes=True
        bsdf=mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value=tuple(item["base_color"])
            bsdf.inputs["Roughness"].default_value=float(item["roughness"])
            bsdf.inputs["Metallic"].default_value=float(item["metallic"])
        mat["PDHQ_STAGE45_REVIEW"]=True
        mat["PDHQ_texture_group"]=item["texture_group"]
        mat["PDHQ_production_ready"]=False
    print("Stage 45 material review import:", {"created":created,"reused":reused,"production_ready":False})
if __name__=="__main__": main()
