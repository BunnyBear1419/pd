#!/usr/bin/env python3
"""Stage 42: emit schematic room shell boxes for Blender import. Not a finished MLO."""
import argparse, json, subprocess, sys, tempfile
from collections import defaultdict
from pathlib import Path

WALL_T, WALL_H, DOOR_H, SLAB_T, EPS = 0.16, 3.2, 2.1, 0.16, 0.04

def merge(items):
    out=[]
    for a,b in sorted((min(a,b),max(a,b)) for a,b in items if abs(b-a)>EPS):
        if out and a <= out[-1][1]+EPS: out[-1]=(out[-1][0],max(out[-1][1],b))
        else: out.append((a,b))
    return out

def subtract(base,cuts):
    pieces=[base]
    for c,d in merge(cuts):
        nxt=[]
        for a,b in pieces:
            if d<=a+EPS or c>=b-EPS: nxt.append((a,b))
            else:
                if c>a+EPS: nxt.append((a,min(c,b)))
                if d<b-EPS: nxt.append((max(d,a),b))
        pieces=nxt
    return [(a,b) for a,b in pieces if b-a>EPS]

def box(role,name,floor,center,size,**extra):
    return {"role":role,"name":name,"floor":floor,"center_m":[round(float(v),4) for v in center],
            "size_m":[round(float(v),4) for v in size],**extra}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--schedule",default="stage36/room_program_and_adjacency.json")
    ap.add_argument("--fit-report",default="build/stage37_floor_fit.json")
    ap.add_argument("--door-report",default="build/stage40_wall_door_schedule.json")
    ap.add_argument("--output",default="build/stage42_shell_geometry.json")
    a=ap.parse_args()
    schedule=json.loads(Path(a.schedule).read_text(encoding="utf-8"))
    fp=Path(a.fit_report)
    if fp.exists(): fit=json.loads(fp.read_text(encoding="utf-8"))
    else:
        with tempfile.NamedTemporaryFile(suffix=".json",delete=False) as t: fp=Path(t.name)
        try:
            r=subprocess.run([sys.executable,"stage37/audit_stage37_floor_fit.py",a.schedule,"--output",str(fp)],capture_output=True,text=True)
            if r.returncode: raise SystemExit("Stage 37 failed: "+r.stderr[-1000:])
            fit=json.loads(fp.read_text(encoding="utf-8"))
        finally: fp.unlink(missing_ok=True)
    doors=json.loads(Path(a.door_report).read_text(encoding="utf-8")) if Path(a.door_report).exists() else {}
    placements=[p for f in fit.get("floor_results",{}).values() for p in f.get("placements",[])]
    placed={p["id"] for p in placements}; floor_roomids={r["id"] for r in schedule["rooms"] if r.get("floor") in (1,2,3)}
    roof_roomids={r["id"] for r in schedule["rooms"] if r.get("floor") not in (1,2,3)}
    geom=[]; walls=defaultdict(list); cuts=defaultdict(list); door_list=[]
    def side(f,o,c,s,e):
        walls[(int(f),o,round(float(c),3))].append((float(s),float(e)))
    for p in placements:
        f=int(p["floor"]); z=(f-1)*schedule["footprint_reference"]["floor_to_floor_height"]
        x,y,w,d=[float(p[k]) for k in ("x","y","width","depth")]
        geom.append(box("floor_slab","Floor_"+p["id"],f,(x+w/2,y+d/2,z-SLAB_T/2),(w,d,SLAB_T),room_id=p["id"]))
        side(f,"v",x,y,y+d); side(f,"v",x+w,y,y+d); side(f,"h",y,x,x+w); side(f,"h",y+d,x,x+w)
    def opening(f,o,c,center,width,record):
        key=(int(f),o,round(float(c),3)); cuts[key].append((center-width/2,center+width/2)); door_list.append(record)
    for d in doors.get("door_opening_candidates",[]):
        ids=d.get("rooms",[])
        if len(ids)!=2 or any(i not in placed for i in ids): continue
        e=d["edge"]; o="v" if e["orientation"]=="vertical" else "h"
        width=min(float(d["candidate_clear_width_m"]),float(e["length_m"])-0.1)
        if width<=0: continue
        opening(d["floor"],o,e["coordinate_m"],float(d["opening_center_m"]),width,
                {"door_id":d["door_id"],"rooms":ids,"floor":d["floor"],"type":"room_to_room_candidate","clear_width_m":round(width,3)})
    # Add a candidate entrance on each room wall facing the reserved central corridor.
    for p in placements:
        x,y,w,d=[float(p[k]) for k in ("x","y","width","depth")]; f=int(p["floor"])
        if x+w<=-1.2+EPS: o,c="v",x+w
        elif x>=1.2-EPS: o,c="v",x
        else: continue
        width=min(0.9,d-0.3)
        if width>0: opening(f,o,c,y+d/2,width,{"door_id":"COR-"+p["id"],"rooms":[p["id"]],"floor":f,"type":"corridor_access_candidate","clear_width_m":round(width,3)})
    for (f,o,c),raw in sorted(walls.items()):
        z=(f-1)*schedule["footprint_reference"]["floor_to_floor_height"]
        spans=merge(raw); openings=merge(cuts.get((f,o,c),[]))
        for s,e in spans:
            for lo,hi in subtract((s,e),openings):
                if o=="v": center,size=(c,(lo+hi)/2,z+WALL_H/2),(WALL_T,hi-lo,WALL_H)
                else: center,size=((lo+hi)/2,c,z+WALL_H/2),(hi-lo,WALL_T,WALL_H)
                geom.append(box("wall_segment",f"Wall_{f}_{o}_{c}_{lo}",f,center,size,orientation=o))
        for lo,hi in openings:
            if not any(lo>=s-EPS and hi<=e+EPS for s,e in spans): continue
            if o=="v": center,size=(c,(lo+hi)/2,z+(DOOR_H+WALL_H)/2),(WALL_T,hi-lo,WALL_H-DOOR_H)
            else: center,size=((lo+hi)/2,c,z+(DOOR_H+WALL_H)/2),(hi-lo,WALL_T,WALL_H-DOOR_H)
            geom.append(box("door_lintel",f"Lintel_{f}_{o}_{c}_{lo}",f,center,size))
    for r in schedule["rooms"]:
        if r.get("use")=="vertical_core" and r["id"] in placed:
            p=next(p for p in placements if p["id"]==r["id"]); f=int(p["floor"]); z=(f-1)*schedule["footprint_reference"]["floor_to_floor_height"]
            geom.append(box("vertical_core_placeholder","CorePlaceholder_"+r["id"],f,(p["x"]+p["width"]/2,p["y"]+p["depth"]/2,z+1.4),(min(1.8,p["width"]-0.4),min(2,p["depth"]-0.4),2.8),note="Replace with actual stair/elevator geometry"))
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    report={"stage":42,"status":"schematic_shell_geometry_generated","units":"metres","wall_thickness_m":WALL_T,"wall_height_m":WALL_H,"door_opening_height_m":DOOR_H,
            "room_count":len(schedule["rooms"]),"placed_room_count":len(placements),"unplaced_floor_room_ids":sorted(floor_roomids-placed),"roof_room_ids_not_floor_fitted":sorted(roof_roomids),
            "counts":{"geometry_boxes":len(geom),"floor_slabs":sum(g["role"]=="floor_slab" for g in geom),"wall_segments":sum(g["role"]=="wall_segment" for g in geom),"door_lintels":sum(g["role"]=="door_lintel" for g in geom),"door_candidates":len(door_list)},
            "door_candidates":door_list,"geometry":geom,"blender_import_script":"stage42/build_stage42_shells_blender.py","production_ready":False,
            "limitations":["Schematic blockout only; no façade, windows, roof, furniture, UVs, materials, collision proxies, Sollumz archetypes or GTA export.","Stage 37 placement is not a reviewed architectural plan; inspect all geometry and clearances in Blender."]}
    out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out),"counts":report["counts"],"unplaced_floor_room_ids":report["unplaced_floor_room_ids"],"roof_room_ids_not_floor_fitted":report["roof_room_ids_not_floor_fitted"],"production_ready":False},indent=2))
if __name__=="__main__": main()
