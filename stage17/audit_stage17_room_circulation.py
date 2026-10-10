"""Stage 17: room/circulation review report for the PDHQ Blender scene.

Non-destructive, heuristic only. Run after Stages 2-4 in Blender.
"""
import bpy, json
from datetime import datetime

REPORT_NAME = "PDHQ_STAGE17_ROOM_CIRCULATION_REPORT"
FLOOR_HEIGHT = 4.2
FLOOR_COUNT = 3


def bounds(obj):
    corners=[obj.matrix_world @ c for c in obj.bound_box]
    return (min(v.x for v in corners),max(v.x for v in corners),
            min(v.y for v in corners),max(v.y for v in corners),
            min(v.z for v in corners),max(v.z for v in corners))

def overlap(a,b,margin=0.0):
    return a[0] < b[1]-margin and a[1] > b[0]+margin and a[2] < b[3]-margin and a[3] > b[2]+margin and a[4] < b[5]-margin and a[5] > b[4]+margin

def main():
    scene=bpy.context.scene; objects=list(scene.objects); findings=[]; checks=[]
    def flag(level,code,title,detail,action):
        findings.append({"severity":level,"code":code,"title":title,"detail":detail,"recommended_action":action})
    required=["PDHQ_STRUCTURE","PDHQ_INTERIOR_ZONES","PDHQ_FURNITURE_BLOCKOUT"]
    for name in required:
        c=bpy.data.collections.get(name)
        checks.append({"check":"collection","name":name,"found":bool(c),"object_count":len(list(c.all_objects)) if c else 0})
        if not c: flag("WARNING","COLLECTION_MISSING",name+" missing","Expected collection not found.","Run the relevant earlier stage or verify the collection name.")
    names={o.name:o for o in objects}
    for floor in range(1,FLOOR_COUNT+1):
        slab=names.get("PDHQ_F%d_SLAB"%floor)
        checks.append({"check":"floor_anchor","name":"PDHQ_F%d_SLAB"%floor,"found":bool(slab)})
        if not slab: flag("BLOCKER","FLOOR_ANCHOR_MISSING","Floor %d slab anchor missing"%floor,"Floor slab object not found by expected name.","Run Stage 2 and confirm floor naming before room review.")
    expected_prefixes=["PDHQ_F1_RECEPTION_COUNTER","PDHQ_F1_BOOKING_INTAKE_","PDHQ_F1_GARAGE_VEHICLE_CLEARANCE_","PDHQ_F2_DISPATCH_CONSOLE_","PDHQ_F2_EVIDENCE_CABINET_","PDHQ_F2_ARMORY_LOCKER_","PDHQ_F3_DETECTIVE_DESK_","PDHQ_F3_INTERVIEW_TABLE_"]
    for prefix in expected_prefixes:
        count=sum(1 for o in objects if o.name.startswith(prefix))
        checks.append({"check":"furnishing_prefix","prefix":prefix,"count":count})
        if count==0: flag("REVIEW","FURNITURE_NOT_FOUND","No objects for "+prefix,"The expected furnishing name prefix had no matches; it may be a run-order, naming, or stage-generation issue.","Run Stage 4 and verify the objects in the Outliner.")
    # Test only likely major fixtures, ignoring small trim, labels, and hardware.
    major=[o for o in objects if o.type=="MESH" and any(k in o.name.upper() for k in ("DESK","COUNTER","CONSOLE","CABINET","LOCKER","BENCH","TABLE","VEHICLE_CLEARANCE")) and not any(k in o.name.upper() for k in ("_TOP","_LEG","_MONITOR","_KEYBOARD","_HANDLE","_LABEL","_GUIDE_LINE"))]
    candidates=[]
    for i,a in enumerate(major):
        ba=bounds(a)
        for b in major[i+1:]:
            # Ignore components with the same furniture prefix: tops/legs can intentionally touch.
            if a.name.rsplit("_",1)[0]==b.name.rsplit("_",1)[0]: continue
            bb=bounds(b)
            if overlap(ba,bb,margin=0.015):
                candidates.append({"a":a.name,"b":b.name})
    checks.append({"check":"major_fixture_aabb_pair_count","candidate_count":len(candidates),"tested_object_count":len(major)})
    if candidates:
        for pair in candidates[:80]:
            flag("REVIEW","POSSIBLE_FIXTURE_OVERLAP","Possible fixture overlap",pair["a"]+" overlaps "+pair["b"]+" by world-axis bounding boxes.","Inspect the pair in Blender; bounding boxes can report false positives and do not prove mesh intersection.")
        if len(candidates)>80: flag("INFO","OVERLAP_LIST_TRUNCATED","Overlap findings truncated",str(len(candidates)-80)+" additional pairs omitted from detailed findings.","Review the full scene if extensive clutter is present.")
    else:
        checks.append({"check":"fixture_overlap_result","result":"No candidate AABB overlaps found among selected major fixtures; this is not a full collision test."})
    # Count named door-gap/door-guide objects only as a prompt for inspection.
    door_named=[o.name for o in objects if any(k in o.name.upper() for k in ("DOOR","DOORGAP","DOOR_GAP","FRAME"))]
    checks.append({"check":"door_named_object_count","count":len(door_named)})
    flag("REVIEW","DOOR_CLEARANCE_MANUAL","Door and corridor clearance needs manual review","Names and AABB tests cannot establish passable width, door swing, accessible routes, security separation, or emergency egress.","Walk each floor in orthographic/top view and verify openings, route continuity, furniture clearance, and room access before final modeling.")
    flag("REVIEW","ROOM_MEMBERSHIP_MANUAL","Confirm furniture is inside intended rooms","Coordinates and object prefixes do not prove a fixture is actually within its intended room boundaries.","Inspect each floor plan and correct fixtures that cross partitions, block doors, or intrude into corridor space.")
    report={"report":REPORT_NAME,"generated_utc":datetime.utcnow().isoformat(timespec="seconds")+"Z","blend_file":bpy.data.filepath or "(unsaved Blender file)","scope":"Non-destructive naming and axis-aligned bounding-box heuristics; no geometry changed.","checks":checks,"findings":findings,"severity_counts":{s:sum(1 for f in findings if f["severity"]==s) for s in ("BLOCKER","WARNING","REVIEW","INFO")}}
    payload=json.dumps(report,indent=2)
    tb=bpy.data.texts.get(REPORT_NAME) or bpy.data.texts.new(REPORT_NAME)
    tb.clear(); tb.write(payload)
    print("\n=== PDHQ STAGE 17 ROOM / CIRCULATION REPORT ===\n"+payload)
    print("Report saved in Blender Text Editor as "+REPORT_NAME+". No geometry was modified.")

if __name__=="__main__": main()
