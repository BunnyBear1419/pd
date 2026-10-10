"""Read-only geometry/LOD budget audit for an open Blender scene.
Run inside Blender; this script does not simplify, decimate, delete, or modify objects.
"""
import argparse, json, sys
from pathlib import Path
import bpy

def main():
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="build/stage47_blender_geometry_audit.json")
    ap.add_argument("--triangle-review",type=int,default=50000)
    ap.add_argument("--material-slot-review",type=int,default=4)
    args=ap.parse_args(argv)
    rows=[]; issues=[]; total_tri=0
    depsgraph=bpy.context.evaluated_depsgraph_get()
    for obj in sorted(bpy.context.scene.objects,key=lambda o:o.name):
        if obj.type!="MESH": continue
        mesh=obj.data; eval_obj=obj.evaluated_get(depsgraph); eval_mesh=None
        try:
            eval_mesh=eval_obj.to_mesh()
            tris=sum(max(0,len(poly.vertices)-2) for poly in eval_mesh.polygons)
        finally:
            if eval_mesh is not None: eval_obj.to_mesh_clear()
        total_tri+=tris
        scale=[round(float(v),5) for v in obj.scale]
        row={"object":obj.name,"vertices_base":len(mesh.vertices),"polygons_base":len(mesh.polygons),
             "triangles_evaluated_estimate":tris,"dimensions_scene_units":[round(float(v),4) for v in obj.dimensions],
             "scale":scale,"material_slots":len(obj.material_slots),"has_active_uv":bool(mesh.uv_layers.active),
             "modifier_types":[m.type for m in obj.modifiers],"collections":[c.name for c in obj.users_collection]}
        if tris>=args.triangle_review:
            issues.append({"object":obj.name,"severity":"review","issue":"high evaluated triangle count; inspect silhouette and possible LOD/simplification"})
            row["lod_candidate"]="review distance LOD or simplification; do not auto-decimate"
        if len(obj.material_slots)>args.material_slot_review:
            issues.append({"object":obj.name,"severity":"optimization","issue":"many material slots; assess safe consolidation"})
        if any(abs(v)<0.001 or abs(v)>1000 for v in scale):
            issues.append({"object":obj.name,"severity":"review","issue":"unusual object scale; confirm units and transforms before export"})
        if not mesh.uv_layers.active:
            issues.append({"object":obj.name,"severity":"review","issue":"no active UV layer"})
        rows.append(row)
    report={"stage":47,"production_ready":False,"scene":bpy.context.scene.name,"mesh_objects":len(rows),
            "evaluated_triangle_estimate_total":total_tri,"issues":issues,"objects":rows,
            "note":"Read-only review. Triangle counts and thresholds are triage indicators; decide LODs by silhouette, gameplay visibility and measured runtime performance."}
    p=Path(args.output); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("Stage 47 geometry audit:",{"mesh_objects":len(rows),"triangles":total_tri,"issues":len(issues),"output":str(p)})
if __name__=="__main__": main()
