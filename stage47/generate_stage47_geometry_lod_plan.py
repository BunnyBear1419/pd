#!/usr/bin/env python3
"""Generate an evidence-labeled geometry and LOD budget from schematic blockouts."""
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--shell",default="build/stage42_shell_geometry.json")
    ap.add_argument("--furniture",default="build/stage43_furniture_blockout.json")
    ap.add_argument("--output",default="build/stage47_geometry_lod_plan.json")
    args=ap.parse_args()
    shell=json.loads(Path(args.shell).read_text(encoding="utf-8"))
    furniture=json.loads(Path(args.furniture).read_text(encoding="utf-8"))
    if shell.get("stage")!=42 or furniture.get("stage")!=43:
        raise SystemExit("Expected Stage 42 shell and Stage 43 furniture manifests")
    geom=shell.get("geometry",[]); furn=furniture.get("geometry",[])
    role_counts={}
    for item in geom+furn:
        role=item.get("role",item.get("name","unknown"))
        role_counts[role]=role_counts.get(role,0)+1
    plan={"stage":47,"title":"Geometry Budget and LOD Review Plan","production_ready":False,
      "inputs":{"stage42_geometry_boxes":len(geom),"stage43_furniture_boxes":len(furn)},
      "schematic_counts_by_role":dict(sorted(role_counts.items())),
      "lod_policy":[
        {"class":"main_architecture","priority":"high","guidance":"Preserve gameplay-critical silhouette and openings; use simplified distant representations only if the target asset pipeline supports them."},
        {"class":"repeated_small_props","priority":"high","guidance":"Share meshes/materials where appropriate; prioritize distant detail reduction for repeated props."},
        {"class":"large_flat_surfaces","priority":"medium","guidance":"Avoid unnecessary subdivisions; remove hidden faces only after checking shared walls, portals and visibility."},
        {"class":"glass_and_thin_details","priority":"medium","guidance":"Check overdraw and thin geometry; preserve functional observation windows and collision-relevant frames."},
        {"class":"collision_meshes","priority":"high","guidance":"Keep collision simpler than render geometry, with walkable floors and clear vehicle corridors; validate in CodeWalker and FiveM."}],
      "review_thresholds":{"triangle_count_review":50000,"material_slots_review":4,"scale_component_review_min":0.001,"scale_component_review_max":1000},
      "required_evidence":["Blender scene triangle/object baseline","LOD distance and silhouette review","collision walk-through and vehicle-clearance test","CodeWalker export inspection","FiveM frame-time and memory comparison"],
      "limitations":["Stage 42 and Stage 43 inputs are schematic boxes, not final meshes.","Counts are planning signals, not a performance benchmark.","Do not mark production-ready until the external evidence above is recorded."]}
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(plan,indent=2)+"\n",encoding="utf-8")
    print(f"Wrote {out}: {len(geom)} shell boxes, {len(furn)} furniture placeholders")
if __name__=="__main__": main()
