#!/usr/bin/env python3
"""Import Stage 44 review lights into a dedicated Blender collection."""
import argparse
import json
import sys
from pathlib import Path

import bpy


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default="build/stage44_lighting_manifest.json")
    parser.add_argument("--collection", default="PDHQ_STAGE44_LIGHTING_REVIEW")
    parser.add_argument("--replace-collection", action="store_true")
    args = parser.parse_args(argv)
    path = Path(args.manifest)
    if not path.is_file():
        raise SystemExit(f"Lighting manifest not found: {path}")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("stage") != 44 or not isinstance(manifest.get("lights"), list):
        raise SystemExit("Input is not a Stage 44 lighting manifest.")
    if manifest.get("production_ready") is not False:
        raise SystemExit("Refusing import: lighting manifest must be marked not production-ready.")
    existing = bpy.data.collections.get(args.collection)
    if existing and not args.replace_collection:
        raise SystemExit(f"Collection {args.collection!r} already exists. Use --replace-collection only on a saved copy.")
    if existing:
        for obj in list(existing.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(existing)
    collection = bpy.data.collections.new(args.collection)
    bpy.context.scene.collection.children.link(collection)
    created = 0
    for index, item in enumerate(manifest["lights"]):
        loc = item.get("location_m")
        color = item.get("color_rgb", [1.0, 1.0, 1.0])
        if not isinstance(loc, list) or len(loc) != 3 or not isinstance(color, list) or len(color) != 3:
            raise SystemExit(f"Light entry {index} has invalid location/color.")
        if any(not isinstance(v, (int, float)) for v in loc + color):
            raise SystemExit(f"Light entry {index} has non-numeric location/color.")
        kind = item.get("type", "AREA")
        if kind not in {"AREA", "POINT", "SPOT", "SUN"}:
            raise SystemExit(f"Unsupported light type {kind!r}.")
        data = bpy.data.lights.new(str(item.get("name", f"Stage44Light_{index:04d}")), type=kind)
        data.energy = max(0.0, float(item.get("power_w", 500.0)))
        data.color = tuple(max(0.0, min(1.0, float(v))) for v in color)
        if kind == "AREA":
            data.shape = "DISK"
            data.size = max(0.1, float(item.get("size_m", 1.0)))
        elif kind in {"POINT", "SPOT"}:
            data.shadow_soft_size = max(0.0, float(item.get("radius_m", 1.0)) * 0.1)
        obj = bpy.data.objects.new(data.name, data)
        obj.location = tuple(float(v) for v in loc)
        obj["stage_blockout_stage"] = 44
        obj["stage_blockout_role"] = str(item.get("role", "lighting_review"))
        obj["stage_blockout_production_ready"] = False
        if item.get("room_id") is not None:
            obj["stage_blockout_room_id"] = str(item["room_id"])
        collection.objects.link(obj)
        created += 1
    collection["stage_blockout_stage"] = 44
    collection["stage_blockout_source_manifest"] = str(path)
    collection["stage_blockout_production_ready"] = False
    print(json.dumps({"stage": 44, "collection": args.collection, "lights_created": created,
                      "production_ready": False, "note": "Review lights only; exclude from GTA export until converted and validated."}, indent=2))


if __name__ == "__main__":
    main()
