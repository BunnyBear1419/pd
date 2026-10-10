#!/usr/bin/env python3
"""Stage 48: integrate review manifests and produce a conservative pre-export report."""
import argparse, json
from pathlib import Path
INPUTS={"shell":("build/stage42_shell_geometry.json",42,"geometry"),"furniture":("build/stage43_furniture_blockout.json",43,"geometry"),"lighting":("build/stage44_lighting_manifest.json",44,"lights"),"materials":("build/stage45_material_manifest.json",45,"materials"),"uv_plan":("build/stage46_uv_atlas_plan.json",46,"atlas_plans"),"geometry_lod":("build/stage47_geometry_lod_plan.json",47,"lod_policy")}
def main():
 p=argparse.ArgumentParser(description=__doc__); p.add_argument('--root',default='.'); p.add_argument('--output',default='build/stage48_pre_export_report.json'); a=p.parse_args(); root=Path(a.root).resolve(); checks=[]; summaries={}; blockers=[]
 for key,(rel,stage,field) in INPUTS.items():
  path=root/rel; c={'input':key,'path':rel,'present':path.is_file(),'expected_stage':stage}
  if not path.is_file(): c.update(valid=False,reason='required generated manifest is missing'); blockers.append(rel); checks.append(c); continue
  try:
   data=json.loads(path.read_text(encoding='utf-8')); actual=data.get('stage')
   count=(data.get('counts',{}).get(field,0) if key=='uv_plan' else len(data.get(field,[])))
   valid=actual==stage and data.get('production_ready') is False and count>=0
   c.update(actual_stage=actual,production_ready=data.get('production_ready'),item_count_or_plan_count=count,valid=valid)
   if not valid: c['reason']='stage marker, production_ready flag, or expected collection is invalid'; blockers.append(rel)
   summaries[key]={'stage':stage,'count':count}
  except (OSError,json.JSONDecodeError,TypeError,AttributeError) as exc: c.update(valid=False,reason='cannot parse manifest: '+str(exc)); blockers.append(rel)
  checks.append(c)
 report={'stage':48,'title':'Integrated Pre-Export Review','production_ready':False,'status':'BLOCKED_INPUT_MANIFESTS' if blockers else 'MANIFESTS_PRESENT_EXTERNAL_REVIEW_REQUIRED','inputs':summaries,'checks':checks,'blocking_inputs':blockers,'required_external_reviews':['Inspect the saved Blender scene, collections and transforms.','Review actual mesh UVs, materials, collision and LODs in the selected toolchain.','Verify room transitions, visibility, portals/occlusion and garage/roof clearances.','Export actual assets and inspect in CodeWalker.','Test join, spawn, respawn, reconnect, resource restart and multiple FiveM clients.','Record measured frame time, memory, defects, tool versions and rollback instructions.'],'limitations':['This checks planning manifests only.','It does not create or certify Blender geometry, GTA archetypes, portals, streamed assets or a working FiveM resource.','CI success is not proof of export or in-game validity.']}
 out=Path(a.output); out=out if out.is_absolute() else root/out; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8'); print(json.dumps({'status':report['status'],'manifest_checks':len(checks),'blocking_inputs':len(blockers),'production_ready':False,'output':str(out)},indent=2))
if __name__=='__main__': main()
