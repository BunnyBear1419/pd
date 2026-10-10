#!/usr/bin/env python3
"""Stage 38: render Stage 37 room-fit proposals as reviewable SVG floor plans.

These diagrams are schematic review aids. They are not construction documents
and do not validate egress, accessibility, structure, fire protection, or GTA assets.
"""
import argparse
import html
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLORS = {
    "public": "#dbeafe", "public_support": "#dbeafe",
    "secure": "#fde68a", "high_security": "#fca5a5",
    "staff_secure": "#bbf7d0", "restricted_staff": "#c4b5fd",
    "vehicle_secure": "#fed7aa", "it_comms": "#a5f3fc",
    "airside_restricted": "#fecaca"
}
def esc(value):
    return html.escape(str(value), quote=True)

def svg_floor(floor, result, footprint, out):
    width_m, depth_m = footprint
    scale = 18
    pad = 70
    canvas_w, canvas_h = int(width_m * scale + pad * 2), int(depth_m * scale + pad * 2 + 60)
    def px(x): return pad + (x + width_m / 2) * scale
    def py(y, d=0): return pad + (depth_m / 2 - y - d) * scale
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}">',
      '<rect width="100%" height="100%" fill="#f8fafc"/>',
      f'<text x="{pad}" y="28" font-family="Arial,sans-serif" font-size="20" font-weight="700" fill="#0f172a">PDHQ — Floor {floor} schematic room-fit preview</text>',
      f'<text x="{pad}" y="48" font-family="Arial,sans-serif" font-size="11" fill="#475569">54 × 38 m reference footprint • front façade at negative Y • not construction documentation</text>',
      f'<rect x="{px(-width_m/2)}" y="{py(depth_m/2)}" width="{width_m*scale}" height="{depth_m*scale}" fill="#fff" stroke="#0f172a" stroke-width="3"/>']
    # Reserved central corridor spine, x = -1.2..+1.2
    parts.append(f'<rect x="{px(-1.2)}" y="{py(depth_m/2-0.5)}" width="2.4" height="{(depth_m-1)*scale}" fill="#e2e8f0" stroke="#64748b" stroke-dasharray="5 4"/>')
    parts.append(f'<text x="{px(0)}" y="{py(depth_m/2-1)}" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#334155">reserved 2.4m spine</text>')
    for p in result.get("placements", []):
        x, y, w, d = p["x"], p["y"], p["width"], p["depth"]
        fill = COLORS.get(p.get("zone"), "#e5e7eb")
        parts.append(f'<rect x="{px(x)}" y="{py(y,d)}" width="{w*scale}" height="{d*scale}" rx="2" fill="{fill}" stroke="#334155" stroke-width="1.2"><title>{esc(p["id"])} — {esc(p["name"])} ({w:g}×{d:g}m)</title></rect>')
        fs = 9 if w >= 4 and d >= 3 else 7
        cx, cy = px(x)+w*scale/2, py(y,d)+d*scale/2
        parts.append(f'<text x="{cx}" y="{cy-2}" text-anchor="middle" font-family="Arial,sans-serif" font-size="{fs}" font-weight="700" fill="#0f172a">{esc(p["id"])}</text>')
        parts.append(f'<text x="{cx}" y="{cy+9}" text-anchor="middle" font-family="Arial,sans-serif" font-size="{max(6,fs-1)}" fill="#334155">{esc(p["name"][:22])}</text>')
    # Front arrow / label
    parts.append(f'<path d="M {px(0)-5} {py(-depth_m/2)-18} l 5 10 l 5 -10" fill="none" stroke="#b91c1c" stroke-width="2"/>')
    parts.append(f'<text x="{px(0)}" y="{py(-depth_m/2)-22}" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#b91c1c">FRONT / PUBLIC ENTRY (−Y)</text>')
    parts.append(f'<text x="{pad}" y="{canvas_h-18}" font-family="Arial,sans-serif" font-size="10" fill="#475569">Fit screen: {"PASS" if result.get("fit_pass") else "REVIEW REQUIRED"} • Placed {result.get("placed_count",0)}/{result.get("room_count",0)} • Adjacency, doors, wall thickness and egress are not modeled.</text>')
    parts.append('</svg>')
    out.write_text("\n".join(parts)+"\n", encoding="utf-8")

def svg_roof(roof, footprint, out):
    width_m, depth_m = footprint; scale=18; pad=70
    cw=int(width_m*scale+pad*2); ch=int(depth_m*scale+pad*2+60)
    def px(x): return pad+(x+width_m/2)*scale
    def py(y,d=0): return pad+(depth_m/2-y-d)*scale
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'%(cw,ch,cw,ch),
      '<rect width="100%" height="100%" fill="#f8fafc"/>',
      f'<text x="{pad}" y="28" font-family="Arial,sans-serif" font-size="20" font-weight="700" fill="#0f172a">PDHQ — Roof / helipad envelope preview</text>',
      f'<text x="{pad}" y="48" font-family="Arial,sans-serif" font-size="11" fill="#475569">Nominal envelope only • aircraft/structural/obstacle reviews required</text>',
      f'<rect x="{px(-width_m/2)}" y="{py(depth_m/2)}" width="{width_m*scale}" height="{depth_m*scale}" fill="#e2e8f0" stroke="#0f172a" stroke-width="3"/>']
    for item in roof:
        w,d=item["dimensions_m"]; x=-w/2; y=d/2
        parts.append(f'<rect x="{px(x)}" y="{py(y,d)}" width="{w*scale}" height="{d*scale}" fill="#bbf7d0" stroke="#166534" stroke-width="2"/>')
        parts.append(f'<text x="{px(0)}" y="{py(0)+4}" text-anchor="middle" font-family="Arial,sans-serif" font-size="13" font-weight="700" fill="#14532d">{esc(item["id"])} • {w}×{d} m</text>')
    parts += [f'<text x="{pad}" y="{ch-18}" font-family="Arial,sans-serif" font-size="10" fill="#475569">Do not treat this diagram as an approved helipad design.</text>','</svg>']
    out.write_text("\n".join(parts)+"\n",encoding="utf-8")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schedule",default=str(ROOT/"stage36/room_program_and_adjacency.json"))
    parser.add_argument("--output-dir",default="build/stage38-floorplans")
    args=parser.parse_args()
    outdir=Path(args.output_dir)
    if not outdir.is_absolute(): outdir=(Path.cwd()/outdir).resolve()
    outdir.mkdir(parents=True,exist_ok=True)
    schedule=json.loads(Path(args.schedule).read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="pdhq_stage37_") as td:
        fitfile=Path(td)/"fit.json"
        proc=subprocess.run([sys.executable,str(ROOT/"stage37/audit_stage37_floor_fit.py"),args.schedule,"--output",str(fitfile)],capture_output=True,text=True)
        if not fitfile.exists():
            raise RuntimeError("Stage 37 did not produce its JSON fit report: "+proc.stderr)
        fit=json.loads(fitfile.read_text(encoding="utf-8"))
        if proc.returncode:
            print("WARNING: Stage 37 reports fit-screen issues; SVGs will still be produced for review.",file=sys.stderr)
    footprint=schedule["footprint_reference"]
    dims=[footprint["width"],footprint["depth"]]
    generated=[]
    for floor in (1,2,3):
        path=outdir/f"floor_{floor}.svg"
        svg_floor(floor,fit["floor_results"][str(floor)],dims,path); generated.append(str(path))
    roofpath=outdir/"roof_helipad.svg"
    svg_roof(fit.get("roof_envelopes",[]),dims,roofpath); generated.append(str(roofpath))
    index=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDHQ floor-plan review</title>',
      '<style>body{font:16px system-ui;margin:2rem;background:#eef2f7;color:#0f172a}main{max-width:1200px;margin:auto}section{background:white;padding:1rem;margin:1rem 0;border-radius:12px}img{width:100%;height:auto;border:1px solid #cbd5e1}a{color:#1d4ed8}</style><main><h1>Police HQ — schematic floor-plan review</h1>',
      '<p>SVG previews generated from Stage 37 rectangle packing. This is a planning aid, not a build-ready architectural plan. Check all room adjacency, circulation, security boundaries, doors, wall thickness, accessible routes, stairs, lift, furniture, egress, structure and services in Blender.</p>']
    for name in ["floor_1.svg","floor_2.svg","floor_3.svg","roof_helipad.svg"]:
        index.append(f'<section><h2>{esc(name.replace("_"," ").replace(".svg","").title())}</h2><p><a href="{name}">Open SVG</a></p><img src="{name}" alt="{esc(name)}"></section>')
    index.append('</main></html>')
    (outdir/"index.html").write_text("\n".join(index)+"\n",encoding="utf-8")
    summary={"stage":38,"generated_files":generated+[str(outdir/"index.html")],"fit_screen_pass":fit.get("fit_screen_pass",False),"floor_results":{k:{"placed":v["placed_count"],"rooms":v["room_count"],"unplaced":len(v["unplaced_rooms"]),"overlaps":len(v["overlap_pairs"])} for k,v in fit["floor_results"].items()},"production_ready":False}
    (outdir/"stage38_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
