"""Stage 26: repair major vertical-circulation conflicts in the blockout.

Run inside Blender after Stage 2 and before Stage 3. Replaces full-plate
floor/roof slabs with simple tile slabs around stair and elevator openings,
then converts solid stair/elevator core placeholders into non-solid guides.
This is a schematic correction, not final structural engineering or an MLO.
"""
import json
from pathlib import Path

import bpy

PREFIX = "PDHQ_"
FLOOR_H = 4.2
SLAB = 0.28
W = 54.0
D = 38.0
FLOORS = 3
STAIR_CENTRES_X = (-22.0, 22.0)
STAIR_WIDTH = 5.0
STAIR_LENGTH = 8.0
ELEVATOR_X = 0.0
ELEVATOR_Y = 0.0
ELEVATOR_SIZE = 3.2
# Grid boundaries align tile edges to openings; cells inside openings are omitted.
X_BOUNDS = (-27.0, -24.5, -19.5, -1.6, 1.6, 19.5, 24.5, 27.0)
Y_BOUNDS = (-19.0, -4.0, -1.6, 1.6, 4.0, 19.0)


def get_collection(name):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


def remove_object(name):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)


def make_tile(name, center, dims, material, collection):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    obj = bpy.context.object
    obj.name = PREFIX + name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        obj.data.materials.append(material)
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def in_opening(x, y):
    for sx in STAIR_CENTRES_X:
        if sx - STAIR_WIDTH / 2 <= x <= sx + STAIR_WIDTH / 2 and -STAIR_LENGTH / 2 <= y <= STAIR_LENGTH / 2:
            return True
    return (ELEVATOR_X - ELEVATOR_SIZE / 2 <= x <= ELEVATOR_X + ELEVATOR_SIZE / 2
            and ELEVATOR_Y - ELEVATOR_SIZE / 2 <= y <= ELEVATOR_Y + ELEVATOR_SIZE / 2)


def rebuild_slab(original_name, z, collection_name):
    old = bpy.data.objects.get(PREFIX + original_name)
    material = old.data.materials[0] if old and old.type == "MESH" and old.data.materials else None
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    col = get_collection(collection_name)
    count = 0
    for ix in range(len(X_BOUNDS) - 1):
        x1, x2 = X_BOUNDS[ix], X_BOUNDS[ix + 1]
        for iy in range(len(Y_BOUNDS) - 1):
            y1, y2 = Y_BOUNDS[iy], Y_BOUNDS[iy + 1]
            if in_opening((x1 + x2) / 2, (y1 + y2) / 2):
                continue
            make_tile(
                original_name + "_TILE_{:02d}_{:02d}".format(ix + 1, iy + 1),
                ((x1 + x2) / 2, (y1 + y2) / 2, z),
                (x2 - x1, y2 - y1, SLAB),
                material,
                col,
            )
            count += 1
    return count


def make_guide(name, location, dimensions, collection):
    obj = bpy.data.objects.new(PREFIX + name, None)
    obj.empty_display_type = "CUBE"
    obj.empty_display_size = 1.0
    obj.location = location
    obj.empty_display_size = 1.0
    obj["guide_dimensions_m"] = list(dimensions)
    collection.objects.link(obj)
    return obj


def main():
    structure = get_collection("PDHQ_STRUCTURE")
    interior = get_collection("PDHQ_INTERIOR_ZONES")
    roof_collection = get_collection("PDHQ_ROOF_EQUIPMENT")
    for obj in list(bpy.data.objects):
        if obj.name in (PREFIX + "STAIR_CORE_MASS_-22.0", PREFIX + "STAIR_CORE_MASS_22.0", PREFIX + "ELEVATOR_SHAFT_MASS"):
            bpy.data.objects.remove(obj, do_unlink=True)

    for obj in list(bpy.data.objects):
        if obj.name.startswith(PREFIX + "STAIR_CORE_GUIDE_") or obj.name == PREFIX + "ELEVATOR_SHAFT_GUIDE":
            bpy.data.objects.remove(obj, do_unlink=True)

    slab_counts = {}
    for floor in range(FLOORS):
        slab_counts["F{}_SLAB".format(floor + 1)] = rebuild_slab(
            "F{}_SLAB".format(floor + 1), floor * FLOOR_H, "PDHQ_STRUCTURE"
        )
    roof_z = FLOORS * FLOOR_H
    slab_counts["ROOF_DECK"] = rebuild_slab("ROOF_DECK", roof_z, "PDHQ_STRUCTURE")

    for sx in STAIR_CENTRES_X:
        make_guide("STAIR_CORE_GUIDE_{:+.1f}".format(sx).replace("+", "P").replace("-", "M"),
                   (sx, 0.0, roof_z / 2), (STAIR_WIDTH, STAIR_LENGTH, roof_z), interior)
    make_guide("ELEVATOR_SHAFT_GUIDE", (ELEVATOR_X, ELEVATOR_Y, roof_z / 2),
               (ELEVATOR_SIZE, ELEVATOR_SIZE, roof_z), interior)

    report = {
        "stage": 26,
        "status": "GEOMETRY_RECONCILIATION_APPLIED_REQUIRES_BLENDER_REVIEW",
        "slab_tiles_created": slab_counts,
        "stair_openings_m": [
            {"center": [x, 0.0], "size": [STAIR_WIDTH, STAIR_LENGTH]}
            for x in STAIR_CENTRES_X
        ],
        "elevator_opening_m": {"center": [ELEVATOR_X, ELEVATOR_Y], "size": [ELEVATOR_SIZE, ELEVATOR_SIZE]},
        "changes": [
            "Replaced each full floor plate and roof deck with slab tiles that omit stair/elevator openings.",
            "Removed solid stair-core and elevator-shaft masses that would obstruct circulation.",
            "Added non-solid guide empties documenting vertical-circulation footprints.",
        ],
        "limitations": [
            "Opening edges and structural support are schematic; a qualified review of the structure is still required.",
            "Stair steps, landings, elevator doors, railings, headroom, and accessible routes require visual review.",
            "Tile seams, floor-wall intersections, and roof access must be inspected in Blender.",
            "This does not create final GTA collision, MLO portals, occlusion, LODs, or Sollumz metadata.",
        ],
    }
    block_name = "PDHQ_STAGE26_GEOMETRY_RECONCILIATION_REPORT"
    block = bpy.data.texts.get(block_name) or bpy.data.texts.new(block_name)
    block.clear()
    block.write(json.dumps(report, indent=2))
    print("[PDHQ Stage 26] Applied slab openings and removed solid circulation-core blockers.")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
