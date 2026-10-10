#!/usr/bin/env python3
"""Import Stage 42 schematic shell boxes into Blender; this is a non-destructive blockout."""
import argparse
import json
import sys
from pathlib import Path

import bpy


def arguments():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default="build/stage42_shell_geometry.json")
    parser.add_argument("--collection", default="PDHQ_STAGE42_SHELL")
    parser.add_argument("--replace-collection", action="store_true",
                        help="Delete only the named Stage 42 collection before importing.")
    return parser.parse_args(argv)


def main():
    args = arguments()
    manifest_path = Path(args.manifest)
    if not manifest_path.is_file():
        raise SystemExit(f"Manifest not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    stage_number = manifest.get("stage")
    if stage_number not in (42, 43) or not isinstance(manifest.get("geometry"), list):
        raise SystemExit("Input must be a Stage 42 shell or Stage 43 furniture blockout manifest.")
    if manifest.get("production_ready") is not False:
        raise SystemExit("Refusing import: manifest must explicitly remain marked not production-ready.")

    existing = bpy.data.collections.get(args.collection)
    if existing and not args.replace_collection:
        raise SystemExit(
            f"Collection {args.collection!r} already exists. Use --replace-collection only on a saved copy."
        )
    if existing:
        for obj in list(existing.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(existing)

    collection = bpy.data.collections.new(args.collection)
    bpy.context.scene.collection.children.link(collection)
    created = 0
    for index, item in enumerate(manifest["geometry"]):
        center = item.get("center_m")
        size = item.get("size_m")
        if not (isinstance(center, list) and len(center) == 3 and
                isinstance(size, list) and len(size) == 3):
            raise SystemExit(f"Geometry item {index} has invalid center/size.")
        if any(not isinstance(v, (int, float)) for v in center + size) or any(v <= 0 for v in size):
            raise SystemExit(f"Geometry item {index} has non-numeric coordinates or non-positive dimensions.")

        mesh = bpy.data.meshes.new(f"Stage42Mesh_{index:04d}")
        hx, hy, hz = (float(v) / 2.0 for v in size)
        verts = [(-hx,-hy,-hz), (hx,-hy,-hz), (hx,hy,-hz), (-hx,hy,-hz),
                 (-hx,-hy,hz), (hx,-hy,hz), (hx,hy,hz), (-hx,hy,hz)]
        faces = [(0,3,2,1), (4,5,6,7), (0,1,5,4), (1,2,6,5), (2,3,7,6), (3,0,4,7)]
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        obj = bpy.data.objects.new(str(item.get("name") or f"Stage42_{index:04d}"), mesh)
        obj.location = tuple(float(v) for v in center)
        obj["stage_blockout_stage"] = int(stage_number)
        obj["stage_blockout_role"] = str(item.get("role", "unspecified"))
        obj["stage_blockout_floor"] = int(item.get("floor", 0))
        if item.get("room_id") is not None:
            obj["stage_blockout_room_id"] = str(item["room_id"])
        collection.objects.link(obj)
        created += 1

    collection["stage_blockout_source_manifest"] = str(manifest_path)
    collection["stage_blockout_stage"] = int(stage_number)
    collection["stage_blockout_production_ready"] = False
    print(json.dumps({"stage": stage_number, "collection": args.collection, "objects_created": created,
                      "production_ready": False, "note": "Schematic blockout only; review in Blender."}, indent=2))


if __name__ == "__main__":
    main()
