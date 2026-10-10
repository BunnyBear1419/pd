#!/usr/bin/env python3
"""Generate a reusable, optimization-minded material manifest for the police HQ."""
from __future__ import annotations
import argparse, json
from pathlib import Path

MATERIALS = [
    {"name":"PDHQ_Concrete_Exterior","purpose":"exterior walls and structural concrete","base_color":[0.48,0.49,0.47,1.0],"roughness":0.88,"metallic":0.0,"texture_group":"concrete_neutral","tiling_m":2.0,"texture_set":None},
    {"name":"PDHQ_Concrete_Sealed","purpose":"sealed service floors and utility areas","base_color":[0.34,0.35,0.34,1.0],"roughness":0.58,"metallic":0.0,"texture_group":"concrete_neutral","tiling_m":3.0,"texture_set":None},
    {"name":"PDHQ_Painted_Plaster_Light","purpose":"interior walls and ceilings","base_color":[0.78,0.79,0.76,1.0],"roughness":0.82,"metallic":0.0,"texture_group":"paint_neutral","tiling_m":2.0,"texture_set":None},
    {"name":"PDHQ_Painted_Plaster_Dark","purpose":"feature walls and secure-zone accents","base_color":[0.17,0.20,0.22,1.0],"roughness":0.8,"metallic":0.0,"texture_group":"paint_neutral","tiling_m":2.0,"texture_set":None},
    {"name":"PDHQ_Glass_Clear","purpose":"glazing and internal observation windows","base_color":[0.62,0.78,0.82,1.0],"roughness":0.16,"metallic":0.0,"texture_group":"glass_shared","tiling_m":1.0,"texture_set":None},
    {"name":"PDHQ_Metal_Brushed","purpose":"frames, railings and hardware","base_color":[0.42,0.44,0.45,1.0],"roughness":0.34,"metallic":0.72,"texture_group":"metal_shared","tiling_m":1.0,"texture_set":None},
    {"name":"PDHQ_Stainless_Steel","purpose":"booking fixtures and hygienic work surfaces","base_color":[0.68,0.70,0.71,1.0],"roughness":0.28,"metallic":0.82,"texture_group":"metal_shared","tiling_m":1.0,"texture_set":None},
    {"name":"PDHQ_Ceramic_Tile","purpose":"showers, washrooms and wet rooms","base_color":[0.72,0.74,0.72,1.0],"roughness":0.32,"metallic":0.0,"texture_group":"tile_light","tiling_m":0.5,"texture_set":None},
    {"name":"PDHQ_Rubber_Floor","purpose":"gym, locker and staff circulation floors","base_color":[0.12,0.13,0.13,1.0],"roughness":0.76,"metallic":0.0,"texture_group":"rubber_dark","tiling_m":1.0,"texture_set":None},
    {"name":"PDHQ_Vinyl_Floor","purpose":"office, dispatch and public interior floors","base_color":[0.30,0.33,0.34,1.0],"roughness":0.48,"metallic":0.0,"texture_group":"vinyl_grey","tiling_m":2.0,"texture_set":None},
    {"name":"PDHQ_Safety_Yellow","purpose":"garage lane edges and hazard markings","base_color":[0.95,0.66,0.05,1.0],"roughness":0.64,"metallic":0.0,"texture_group":"paint_safety","tiling_m":1.0,"texture_set":None},
    {"name":"PDHQ_Painted_White","purpose":"door leaves, trim and wayfinding backing","base_color":[0.88,0.89,0.86,1.0],"roughness":0.62,"metallic":0.0,"texture_group":"paint_neutral","tiling_m":2.0,"texture_set":None},
    {"name":"PDHQ_Roof_Membrane","purpose":"flat roof and helipad surrounding surface","base_color":[0.24,0.26,0.27,1.0],"roughness":0.86,"metallic":0.0,"texture_group":"roof_dark","tiling_m":3.0,"texture_set":None},
    {"name":"PDHQ_Asphalt","purpose":"site roads and parking apron","base_color":[0.16,0.17,0.17,1.0],"roughness":0.94,"metallic":0.0,"texture_group":"asphalt_shared","tiling_m":4.0,"texture_set":None},
]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="build/stage45_material_manifest.json")
    args=ap.parse_args()
    names=[m["name"] for m in MATERIALS]
    assert len(names)==len(set(names)), "material names must be unique"
    for m in MATERIALS:
        assert 0<=m["roughness"]<=1 and 0<=m["metallic"]<=1
        assert len(m["base_color"])==4 and all(0<=v<=1 for v in m["base_color"])
        assert m["tiling_m"]>0
    out={"stage":45,"title":"Reusable PBR Material Library","units":"meters","production_ready":False,
         "optimization_policy":{"reuse_materials":True,"unique_material_budget":len(MATERIALS),
         "texture_atlas_preferred":True,"avoid_unique_material_per_prop":True,
         "recommended_texture_sizes":"Use 512px/1K for most repeated props; reserve 2K for hero surfaces only after profiling",
         "note":"Material values are starting points for visual review; GTA shader conversion and texture baking remain external validation tasks."},
         "materials":MATERIALS,"counts":{"materials":len(MATERIALS),"unique_texture_groups":len(set(m["texture_group"] for m in MATERIALS))}}
    p=Path(args.output); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(f"Wrote {p}: {len(MATERIALS)} reusable material profiles")
if __name__=="__main__": main()
