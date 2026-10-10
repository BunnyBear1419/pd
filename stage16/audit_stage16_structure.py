"""Stage 16: non-destructive structural/circulation audit for the PDHQ Blender scene."""
import bpy, json
from datetime import datetime

EXPECTED_LEVELS = 3
FLOOR_HEIGHT = 4.2
SLAB_THICKNESS = 0.28
STRUCTURE_COLLECTION = "PDHQ_STRUCTURE"
INTERIOR_COLLECTION = "PDHQ_INTERIOR_ZONES"
REPORT_NAME = "PDHQ_STAGE16_STRUCTURAL_AUDIT"

def dims(obj): return tuple(round(float(v), 3) for v in obj.dimensions)
def main():
    findings, checks = [], []
    def flag(severity, code, title, detail, recommendation):
        findings.append({"severity":severity,"code":code,"title":title,"detail":detail,"recommendation":recommendation})
    scene=bpy.context.scene
    structure=bpy.data.collections.get(STRUCTURE_COLLECTION)
    interior=bpy.data.collections.get(INTERIOR_COLLECTION)
    objects=list(scene.objects)
    checks.extend([{"name":"scene_object_count","result":len(objects)},
                   {"name":"structure_object_count","result":len(structure.objects) if structure else 0},
                   {"name":"interior_object_count","result":len(interior.objects) if interior else 0}])
    if not structure: flag("BLOCKER","MISSING_STRUCTURE","Structure collection missing",STRUCTURE_COLLECTION+" not found.","Run Stage 2 before this audit.")
    if not interior: flag("WARNING","MISSING_INTERIOR","Interior collection missing",INTERIOR_COLLECTION+" not found.","Run Stage 3 before reviewing interior circulation.")
    if structure:
        by_name={o.name:o for o in structure.objects}
        for floor in range(1,EXPECTED_LEVELS+1):
            name=f"F{floor}_SLAB"; slab=by_name.get(name)
            if not slab:
                flag("BLOCKER","FLOOR_SLAB_MISSING",f"Missing {name}","Expected floor slab not found in PDHQ_STRUCTURE.","Check Stage 2 generation and object naming.")
                continue
            d=dims(slab); expected_z=(floor-1)*FLOOR_HEIGHT
            checks.append({"name":name,"dimensions":d,"origin":[round(float(v),3) for v in slab.location]})
            if abs(d[2]-SLAB_THICKNESS)>0.08:
                flag("WARNING","SLAB_THICKNESS_REVIEW",f"Review {name} thickness",f"Observed dimensions {d}; expected approximately {SLAB_THICKNESS} m thickness.","Inspect slab side profile and confirm intentional thickness.")
            if abs(slab.location.z-expected_z)>0.15:
                flag("WARNING","SLAB_LEVEL_REVIEW",f"Review {name} elevation",f"Origin Z {slab.location.z:.3f} m; expected near {expected_z:.3f} m.","Align floor elevations and stair landing levels.")
        roof=by_name.get("ROOF_DECK")
        if not roof: flag("WARNING","ROOF_DECK_MISSING","Roof deck missing","ROOF_DECK not found.","Check Stage 2 output and naming.")
        else: checks.append({"name":"ROOF_DECK","dimensions":dims(roof)})
    if any("ELEVATOR_SHAFT_MASS" in o.name for o in objects):
        flag("REVIEW","ELEVATOR_OPENINGS","Verify elevator shaft and slab openings","The scene has an elevator shaft placeholder; this audit cannot cut or verify slab openings.","Inspect each floor and roof in section view and create aligned openings before final collision work.")
    stair_masses=[o for o in objects if "STAIR_CORE_MASS" in o.name]
    if stair_masses:
        flag("REVIEW","STAIR_CORE_PLACEHOLDERS","Review stair-core placeholder masses",f"Found {len(stair_masses)} stair-core mass object(s). They may obscure detailed stair flights.","Inspect each core in section view; hide or remove blocking placeholders only after confirming enclosure and landing design.")
    steps=[o for o in objects if "STAIR_" in o.name.upper() and "STEP" in o.name.upper()]
    landings=[o for o in objects if "LANDING" in o.name.upper()]
    doors=[o for o in objects if "DOOR" in o.name.upper() or "FRAME" in o.name.upper()]
    checks.extend([{"name":"stair_step_count","result":len(steps)},{"name":"stair_landing_count","result":len(landings)},{"name":"door_or_frame_named_objects","result":len(doors)}])
    if not steps or not landings:
        flag("WARNING","STAIR_GEOMETRY_REVIEW","Stair steps or landings not detected",f"Detected {len(steps)} step(s) and {len(landings)} landing(s) by object name.","Inspect stairs and confirm each flight reaches the next level with clear headroom and door alignment.")
    if not doors:
        flag("WARNING","DOOR_GAPS_REVIEW","Door gaps need manual inspection","No door/frame objects detected by name; partition openings may still exist.","Inspect partition gaps, planned door leaf width, accessible circulation, and egress routes.")
    flag("REVIEW","FULL_FOOTPRINT_SLAB_PENETRATIONS","Verify slab cuts and vertical penetrations","The blockout uses broad floor plates. This script does not detect or cut openings for stairs, elevator, ducts, or services.","Manually verify all vertical openings, wall intersections, and service penetrations before final collision geometry.")
    if not findings: flag("INFO","NO_HEURISTIC_FLAGS","No heuristic flags raised","Only limited naming and dimension checks were performed.","Continue manual Blender, Sollumz, CodeWalker, and FiveM validation.")
    report={"report":REPORT_NAME,"generated_utc":datetime.utcnow().isoformat(timespec="seconds")+"Z","blend_file":bpy.data.filepath or "(unsaved Blender file)","scope":"Non-destructive heuristic review; not geometry certification.","checks":checks,"findings":findings,"severity_counts":{s:sum(1 for f in findings if f["severity"]==s) for s in ("BLOCKER","WARNING","REVIEW","INFO")}}
    payload=json.dumps(report,indent=2)
    block=bpy.data.texts.get(REPORT_NAME) or bpy.data.texts.new(REPORT_NAME)
    block.clear(); block.write(payload)
    print("\n=== PDHQ STAGE 16 STRUCTURAL AUDIT ===\n"+payload)
    print("Report saved in Blender Text Editor as "+REPORT_NAME+". No geometry was modified.")
if __name__=="__main__": main()
