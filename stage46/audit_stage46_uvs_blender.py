"""Read-only UV audit for an open Blender scene. Run inside Blender.
Usage: blender --background scene.blend --python stage46/audit_stage46_uvs_blender.py -- --output build/stage46_uv_audit.json
This does not unwrap or alter meshes.
"""
import argparse, json, sys
from pathlib import Path
import bpy

def main():
 argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
 ap=argparse.ArgumentParser()
 ap.add_argument("--output",default="build/stage46_uv_audit.json")
 args=ap.parse_args(argv)
 rows=[]; issues=[]
 for obj in sorted(bpy.context.scene.objects,key=lambda o:o.name):
  if obj.type!="MESH": continue
  mesh=obj.data; uv=mesh.uv_layers.active
  mats=[s.material.name if s.material else None for s in obj.material_slots]
  row={"object":obj.name,"vertices":len(mesh.vertices),"polygons":len(mesh.polygons),
       "material_slots":len(obj.material_slots),"materials":mats,"uv_layer":uv.name if uv else None,
       "uv_loop_count":len(uv.data) if uv else 0,"uv_out_of_0_1":0,"uv_degenerate_count":0}
  if not uv:
   issues.append({"object":obj.name,"severity":"review","issue":"missing active UV layer"})
  else:
   for item in uv.data:
    u,v=item.uv
    if u < -0.0001 or v < -0.0001 or u > 1.0001 or v > 1.0001: row["uv_out_of_0_1"]+=1
   if row["uv_out_of_0_1"]:
    issues.append({"object":obj.name,"severity":"review","issue":"UV coordinates outside 0..1; may be intentional tiling"})
  if len(obj.material_slots)>4:
   issues.append({"object":obj.name,"severity":"optimization","issue":"more than four material slots; check whether slots can be consolidated"})
  row["polygon_count_zero_area"]=sum(1 for p in mesh.polygons if p.area <= 1e-10)
  if row["polygon_count_zero_area"]:
   issues.append({"object":obj.name,"severity":"review","issue":"zero-area polygons detected"})
  rows.append(row)
 report={"stage":46,"production_ready":False,"scene":bpy.context.scene.name,"mesh_objects":len(rows),
         "issues":issues,"objects":rows,"note":"Read-only diagnostic. Out-of-range UVs can be valid for tiling; review context before changing."}
 p=Path(args.output); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 print("Stage 46 UV audit:",{"mesh_objects":len(rows),"issues":len(issues),"output":str(p)})
if __name__=="__main__": main()
