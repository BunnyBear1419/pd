#!/usr/bin/env python3
"""Validate optional texture paths without permitting project-root path escape."""
from __future__ import annotations
import argparse, json
from pathlib import Path

ALLOWED={".png",".jpg",".jpeg",".tga",".dds",".webp"}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("manifest",nargs="?",default="build/stage45_material_manifest.json")
    ap.add_argument("--project-root",default=".")
    ap.add_argument("--max-texture-mb",type=float,default=16.0)
    args=ap.parse_args()
    root=Path(args.project_root).resolve()
    data=json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    errors=[]; seen={}
    for mat in data.get("materials",[]):
        raw=mat.get("texture_set")
        if not raw: continue
        if not isinstance(raw,dict):
            errors.append(f"{mat.get('name')}: texture_set must be an object"); continue
        for slot, rel in raw.items():
            if not isinstance(rel,str) or not rel.strip():
                errors.append(f"{mat.get('name')}/{slot}: texture path must be a non-empty string"); continue
            p=(root/rel).resolve()
            if p != root and root not in p.parents:
                errors.append(f"{mat.get('name')}/{slot}: path escapes project root"); continue
            if not p.is_file():
                errors.append(f"{mat.get('name')}/{slot}: missing file {rel}"); continue
            if p.suffix.lower() not in ALLOWED:
                errors.append(f"{mat.get('name')}/{slot}: unsupported extension {p.suffix}"); continue
            if p.stat().st_size > args.max_texture_mb*1024*1024:
                errors.append(f"{mat.get('name')}/{slot}: file exceeds {args.max_texture_mb:g} MB")
            key=str(p)
            if key in seen:
                print(f"NOTICE: texture reused by {seen[key]} and {mat.get('name')}/{slot}")
            else: seen[key]=f"{mat.get('name')}/{slot}"
    report={"stage":45,"production_ready":False,"materials_checked":len(data.get("materials",[])),
            "texture_files_checked":len(seen),"errors":errors,"passed":not errors}
    print(json.dumps(report,indent=2))
    raise SystemExit(1 if errors else 0)
if __name__=="__main__": main()
