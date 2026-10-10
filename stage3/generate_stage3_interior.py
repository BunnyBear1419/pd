"""Stage 3 interior pass for PDHQ Stage 2 Blender scene.

Run Stage 2 generator first, then run this script in the same Blender scene.
Rebuilds the schematic interior collection with door-gap partitions, labelled
room-zone guides, and stepped stair blockouts. This is still not a final MLO.
"""
import bpy
from mathutils import Vector

PREFIX = "PDHQ_"
FLOOR_H = 4.2
SLAB = 0.28
W = 54.0
D = 38.0

scene = bpy.context.scene

def get_collection(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        scene.collection.children.link(c)
    return c

def clear_collection(col):
    for obj in list(col.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

def material(name, color, roughness=0.75, metallic=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return m

MAT_PARTITION = material("MAT_Stage3_Partition", (0.30, 0.48, 0.56))
MAT_FRAME = material("MAT_Stage3_DoorFrame", (0.10, 0.13, 0.15), 0.4, 0.35)
MAT_STEP = material("MAT_Stage3_Stair", (0.48, 0.50, 0.50))
MAT_LABEL = material("MAT_Stage3_Label", (0.95, 0.65, 0.12))

interior = get_collection("PDHQ_INTERIOR_ZONES")
guides = get_collection("PDHQ_GUIDES")
clear_collection(interior)

# Stage 3 can be re-run safely: remove only its own generated zone-label empties.
# Preserve Stage 2's broader site/roof guides and any user-created guide objects.
for obj in list(guides.objects):
    if obj.name.startswith(PREFIX + "ZONE_F"):
        bpy.data.objects.remove(obj, do_unlink=True)

def move_to(obj, col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)
    return obj

def cube(name, loc, dims, mat, col, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = PREFIX + name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    if bevel:
        mod = obj.modifiers.new("Blockout_Edge", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    return move_to(obj, col)

def partition_x(name, x1, x2, y, z, height=2.9, thick=0.14, door_centres=(), door_width=1.0):
    """Wall running along X, with real gaps left for door openings."""
    lo, hi = min(x1, x2), max(x1, x2)
    openings = sorted((max(lo, c-door_width/2), min(hi, c+door_width/2)) for c in door_centres)
    cursor = lo
    for idx, (a, b) in enumerate(openings):
        if a > cursor:
            cube(f"{name}_SEG_{idx}", ((cursor+a)/2, y, z+height/2), (a-cursor, thick, height), MAT_PARTITION, interior)
        cube(f"{name}_LINTEL_{idx}", ((a+b)/2, y, z+height-0.16), (b-a, thick, 0.32), MAT_PARTITION, interior)
        # Side frame posts are visual markers only; replace with detailed door/frame assets later.
        cube(f"{name}_FRAME_L_{idx}", (a, y, z+1.05), (0.07, thick+0.04, 2.1), MAT_FRAME, interior)
        cube(f"{name}_FRAME_R_{idx}", (b, y, z+1.05), (0.07, thick+0.04, 2.1), MAT_FRAME, interior)
        cursor = b
    if cursor < hi:
        cube(f"{name}_SEG_END", ((cursor+hi)/2, y, z+height/2), (hi-cursor, thick, height), MAT_PARTITION, interior)

def partition_y(name, x, y1, y2, z, height=2.9, thick=0.14, door_centres=(), door_width=1.0):
    """Wall running along Y, with real gaps left for door openings."""
    lo, hi = min(y1, y2), max(y1, y2)
    openings = sorted((max(lo, c-door_width/2), min(hi, c+door_width/2)) for c in door_centres)
    cursor = lo
    for idx, (a, b) in enumerate(openings):
        if a > cursor:
            cube(f"{name}_SEG_{idx}", (x, (cursor+a)/2, z+height/2), (thick, a-cursor, height), MAT_PARTITION, interior)
        cube(f"{name}_LINTEL_{idx}", (x, (a+b)/2, z+height-0.16), (thick, b-a, 0.32), MAT_PARTITION, interior)
        cube(f"{name}_FRAME_L_{idx}", (x, a, z+1.05), (thick+0.04, 0.07, 2.1), MAT_FRAME, interior)
        cube(f"{name}_FRAME_R_{idx}", (x, b, z+1.05), (thick+0.04, 0.07, 2.1), MAT_FRAME, interior)
        cursor = b
    if cursor < hi:
        cube(f"{name}_SEG_END", (x, (cursor+hi)/2, z+height/2), (thick, hi-cursor, height), MAT_PARTITION, interior)

# Each floor gets a central corridor spine and room partitions. Door gaps are
# deliberately staggered; final room-by-room design will refine exact positions.
for floor in range(3):
    z = floor * FLOOR_H
    partition_x(f"F{floor+1}_CORRIDOR_N", -26, 26, 2.8, z, door_centres=(-20,-10,0,10,20))
    partition_x(f"F{floor+1}_CORRIDOR_S", -26, 26, -2.8, z, door_centres=(-20,-10,0,10,20))
    for i, x in enumerate((-16,-5,6,17)):
        partition_y(f"F{floor+1}_ROOM_DIV_{i}", x, -18, -2.8, z, door_centres=(-12,-7))
        partition_y(f"F{floor+1}_ROOM_DIV_REAR_{i}", x, 2.8, 18, z, door_centres=(7,12))

# Stair flights: simplified solid steps in two aligned cores. These are visible
# blockout steps, not final walkable collision. Each floor uses two short flights.
for sx in (-22.0, 22.0):
    for floor in range(3):
        base = floor * FLOOR_H
        # Two flights, each 12 steps, rise about 2.1 m, with a landing between.
        for flight in range(2):
            # Lower flight climbs toward the central landing; upper flight
            # returns in the opposite direction to meet the next floor.
            start_y = -3.4 if flight == 0 else 3.4
            start_z = base + (0.0 if flight == 0 else 2.1)
            direction = 1 if flight == 0 else -1
            for step in range(12):
                rise = 2.1 / 12.0
                run = 0.29
                y = start_y + direction * step * run
                h = (step + 1) * rise
                cube(f"STAIR_{sx}_F{floor+1}_FL{flight+1}_STEP{step+1}",
                     (sx, y, start_z + h/2), (2.0, run+0.02, h), MAT_STEP, interior)
        cube(f"STAIR_{sx}_F{floor+1}_LANDING", (sx, 0.15, base+2.1), (2.2, 1.3, 0.18), MAT_STEP, interior)

# Label guides are non-rendering empties to document functional intent.
zone_specs = [
    ("F1_PUBLIC_LOBBY_RECEPTION", (-15,-11,1.3)),
    ("F1_BOOKING_INTAKE", (-5,-11,1.3)),
    ("F1_HOLDING_CELLS", (16,10,1.3)),
    ("F1_VEHICLE_GARAGE", (0,12,1.3)),
    ("F2_DISPATCH", (0,11,FLOOR_H+1.3)),
    ("F2_SWAT_BRIEFING", (14,10,FLOOR_H+1.3)),
    ("F2_EVIDENCE_ARMORY", (-15,10,FLOOR_H+1.3)),
    ("F3_DETECTIVE_BULLPEN", (0,10,2*FLOOR_H+1.3)),
    ("F3_INTERVIEW_ROOMS", (-15,10,2*FLOOR_H+1.3)),
    ("F3_ADMIN_CONFERENCE", (15,10,2*FLOOR_H+1.3)),
]
for name, loc in zone_specs:
    obj = bpy.data.objects.new(PREFIX + "ZONE_" + name, None)
    obj.empty_display_type = "CUBE"
    obj.empty_display_size = 0.8
    obj.location = loc
    guides.objects.link(obj)

print("Stage 3 interior pass created. Inspect door gaps, room circulation, and stair geometry before export.")
