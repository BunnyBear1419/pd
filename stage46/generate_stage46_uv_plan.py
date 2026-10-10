#!/usr/bin/env python3
"""Generate a conservative UV/atlas planning manifest from Stage 45 materials."""
from __future__ import annotations
import argparse, json
from pathlib import Path

ATLAS_PLANS = [
 {"atlas_id":"ATLAS_INTERIOR_NEUTRAL","texture_group":"paint_neutral","target_size":1024,"contents":["painted plaster","white paint","shared trim masks"],"reuse_policy":"one shared set across rooms; avoid per-room duplicates"},
 {"atlas_id":"ATLAS_CONCRETE","texture_group":"concrete_neutral","target_size":1024,"contents":["exterior concrete","sealed concrete","shared concrete variation"],"reuse_policy":"reuse tiling surface; atlas only unique trim/decals"},
 {"atlas_id":"ATLAS_METAL","texture_group":"metal_shared","target_size":1024,"contents":["brushed metal","stainless steel"],"reuse_policy":"share metal roughness/normal maps where appropriate"},
 {"atlas_id":"ATLAS_FLOORING","texture_group":"vinyl_grey","target_size":1024,"contents":["vinyl floor","rubber floor","tile"],"reuse_policy":"separate material response when needed; share packed maps only if authored consistently"},
 {"atlas_id":"ATLAS_SITE","texture_group":"asphalt_shared","target_size":1024,"contents":["asphalt","roof membrane","safety markings"],"reuse_policy":"keep large surfaces tiling; atlas compact markings and small props"},
 {"atlas_id":"ATLAS_GLASS","texture_group":"glass_shared","target_size":512,"contents":["glass tint and masks"],"reuse_policy":"prefer simple shared glass material; do not bake unique glass textures without a need"},
]
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--materials",default="build/stage45_material_manifest.json")
 ap.add_argument("--output",default="build/stage46_uv_atlas_plan.json")
 args=ap.parse_args()
 mats=json.loads(Path(args.materials).read_text(encoding="utf-8"))
 if mats.get("stage")!=45: raise SystemExit("Expected Stage 45 material manifest")
 known={m["texture_group"] for m in mats.get("materials",[])}
 plans=[p for p in ATLAS_PLANS if p["texture_group"] in known]
 data={"stage":46,"title":"UV Mapping and Texture Atlas Plan","units":"meters","production_ready":False,
 "source_stage":45,"uv_review_rules":{"uv_layer_required_for_export_meshes":True,"uv_coordinates_expected_range":[0.0,1.0],
 "allow_out_of_bounds_only_when_explicitly_tiling":True,"check_overlapping_uvs":"only when meshes are intended to use unique baked textures; intentional tile overlap is valid",
 "texel_density":"keep similar asset classes consistent; record target rather than assuming one value fits every asset",
 "padding":"leave mip-safe island padding appropriate to target texture size and compression"},
 "atlas_plans":plans,
 "mesh_class_guidance":[
 {"class":"large_architecture","uv_strategy":"world-aligned tiling materials for concrete/plaster; minimize seams and unique material slots","target_texture_size":"shared 1K tiling sets; validate at gameplay distance"},
 {"class":"small_repeated_props","uv_strategy":"shared atlas with consistent texel density; reuse materials","target_texture_size":"512px to 1K atlas"},
 {"class":"hero_props_and_signage","uv_strategy":"dedicated UVs only where unique detail justifies it; pack decals efficiently","target_texture_size":"up to 2K only after visual review"},
 {"class":"glass_and_metal_frames","uv_strategy":"simple UVs; share material response; avoid unnecessary unique maps","target_texture_size":"shared 512px to 1K where texture is needed"}],
 "counts":{"atlas_plans":len(plans),"material_groups":len(known)},
 "limitations":["This is a planning manifest, not generated UV coordinates or texture atlases.","UV overlaps may be intentional for tiling/mirrored assets; the Blender audit reports indicators, not automatic defects.","Production-ready remains false until UVs and textures are reviewed in Blender/Sollumz and in game."]}
 out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
 print(f"Wrote {out}: {len(plans)} atlas plans from {len(known)} material groups")
if __name__=="__main__": main()
