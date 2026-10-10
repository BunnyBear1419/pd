"""Stage 2 blockout generator for a custom FiveM police HQ.

Run in Blender: Scripting workspace > Open > Run Script.
Designed as a dimensioned, organized blockout, not a finished game-ready MLO.
Units are metres. Building footprint is approximately 54 x 38 m.
"""
import bpy
import math
from mathutils import Vector

# ----------------------------- Configuration -----------------------------
PREFIX = "PDHQ_"
W = 54.0
D = 38.0
FLOOR_H = 4.2
SLAB = 0.28
WALL = 0.22
WALL_H = FLOOR_H - SLAB
FLOORS = 3
SITE_W = 92.0
SITE_D = 78.0

# ----------------------------- Scene setup -------------------------------
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.collections,):
    for c in list(datablocks):
        if c.name != "Collection":
            try:
                datablocks.remove(c)
            except Exception:
                pass
scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 1.0
scene.render.engine = "BLENDER_EEVEE_NEXT"

def collection(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        scene.collection.children.link(c)
    return c

COL_STRUCTURE = collection("PDHQ_STRUCTURE")
COL_INTERIOR = collection("PDHQ_INTERIOR_ZONES")
COL_ROOF = collection("PDHQ_ROOF_EQUIPMENT")
COL_EXTERIOR = collection("PDHQ_EXTERIOR_ASSETS")
COL_COLLISION = collection("PDHQ_COLLISION_PROXIES")
COL_GUIDES = collection("PDHQ_GUIDES")

def move_to(obj, col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)
    return obj

def material(name, color, roughness=0.72, metallic=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return m

MAT_CONCRETE = material("MAT_Blockout_Concrete", (0.38, 0.42, 0.45))
MAT_WALL = material("MAT_Blockout_Walls", (0.69, 0.72, 0.73))
MAT_GLASS = material("MAT_Blockout_GlassTint", (0.12, 0.28, 0.34), 0.22, 0.15)
MAT_DARK = material("MAT_Blockout_DarkMetal", (0.12, 0.15, 0.17), 0.45, 0.55)
MAT_ROOF = material("MAT_Blockout_Roof", (0.28, 0.31, 0.33))
MAT_MARK = material("MAT_Helipad_Marking", (0.92, 0.92, 0.86), 0.5)
MAT_ZONE = material("MAT_Interior_ZoneGuide", (0.25, 0.45, 0.56), 0.7)
MAT_SITE = material("MAT_Site_Apron", (0.24, 0.26, 0.27))

def box(name, loc, scale, mat, col, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = PREFIX + name
    o.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        o.data.materials.append(mat)
    if bevel:
        mod = o.modifiers.new("Small_Blockout_Edges", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    return move_to(o, col)

def wall_x(name, x1, x2, y, z, height=WALL_H, thickness=WALL, mat=MAT_WALL, col=COL_STRUCTURE):
    return box(name, ((x1+x2)/2, y, z+height/2), (abs(x2-x1), thickness, height), mat, col)

def wall_y(name, x, y1, y2, z, height=WALL_H, thickness=WALL, mat=MAT_WALL, col=COL_STRUCTURE):
    return box(name, (x, (y1+y2)/2, z+height/2), (thickness, abs(y2-y1), height), mat, col)

# Origin is centre of footprint; front/public entrance is negative Y.
box("SITE_APRON", (0, 0, -0.24), (SITE_W, SITE_D, 0.45), MAT_SITE, COL_EXTERIOR)
for floor in range(FLOORS):
    z = floor * FLOOR_H
    box(f"F{floor+1}_SLAB", (0, 0, z), (W, D, SLAB), MAT_CONCRETE, COL_STRUCTURE)
    # Outer perimeter walls. Front is split to create a generous entry opening.
    wall_x(f"F{floor+1}_REAR_WALL", -W/2, W/2, D/2, z)
    wall_y(f"F{floor+1}_LEFT_WALL", -W/2, -D/2, D/2, z)
    wall_y(f"F{floor+1}_RIGHT_WALL", W/2, -D/2, D/2, z)
    wall_x(f"F{floor+1}_FRONT_LEFT", -W/2, -7.5, -D/2, z)
    wall_x(f"F{floor+1}_FRONT_RIGHT", 7.5, W/2, -D/2, z)
    # Simple window-band blockout; separate glass panels help visualise facade rhythm.
    for i, x in enumerate(range(-23, 24, 6)):
        if abs(x) > 8:
            box(f"F{floor+1}_FRONT_GLAZING_{i+1}", (x, -D/2-0.025, z+2.25), (3.0, 0.06, 1.55), MAT_GLASS, COL_EXTERIOR)
    # Interior zoning walls: central corridor with cross partitions.
    wall_x(f"F{floor+1}_CORRIDOR_NORTH", -W/2+1, W/2-1, 2.8, z, height=2.8, thickness=0.12, mat=MAT_ZONE, col=COL_INTERIOR)
    wall_x(f"F{floor+1}_CORRIDOR_SOUTH", -W/2+1, W/2-1, -2.8, z, height=2.8, thickness=0.12, mat=MAT_ZONE, col=COL_INTERIOR)
    for j, x in enumerate([-16, -5, 6, 17]):
        wall_y(f"F{floor+1}_ROOM_DIVIDER_{j+1}", x, -D/2+1, -2.8, z, height=2.8, thickness=0.12, mat=MAT_ZONE, col=COL_INTERIOR)
        wall_y(f"F{floor+1}_ROOM_DIVIDER_REAR_{j+1}", x, 2.8, D/2-1, z, height=2.8, thickness=0.12, mat=MAT_ZONE, col=COL_INTERIOR)

# Front entrance canopy and support columns.
box("ENTRANCE_CANOPY", (0, -D/2-3.0, 4.0), (23, 6.0, 0.45), MAT_DARK, COL_EXTERIOR, 0.08)
for x in [-10, 10]:
    box(f"CANOPY_COLUMN_{x}", (x, -D/2-4.8, 1.95), (0.45, 0.45, 3.9), MAT_DARK, COL_EXTERIOR)

# Roof deck and perimeter parapet.
roof_z = FLOORS * FLOOR_H
box("ROOF_DECK", (0, 0, roof_z), (W, D, SLAB), MAT_ROOF, COL_STRUCTURE)
for x in [-W/2, W/2]:
    box(f"ROOF_PARAPET_SIDE_{x}", (x, 0, roof_z+0.65), (0.35, D, 1.3), MAT_CONCRETE, COL_STRUCTURE)
for y in [-D/2, D/2]:
    box(f"ROOF_PARAPET_END_{y}", (0, y, roof_z+0.65), (W, 0.35, 1.3), MAT_CONCRETE, COL_STRUCTURE)

# Helipad to the rear/right of roof; H and perimeter markings are simple blockout geometry.
pad_x, pad_y = 12.0, 5.0
box("HELIPAD_PLATFORM", (pad_x, pad_y, roof_z+0.18), (22, 20, 0.18), MAT_DARK, COL_ROOF)
mark_z = roof_z + 0.29
box("HELIPAD_MARK_H_BAR_TOP", (pad_x, pad_y+2.0, mark_z), (5.0, 0.45, 0.035), MAT_MARK, COL_ROOF)
box("HELIPAD_MARK_H_BAR_BOTTOM", (pad_x, pad_y-2.0, mark_z), (5.0, 0.45, 0.035), MAT_MARK, COL_ROOF)
box("HELIPAD_MARK_H_LEFT", (pad_x-2.0, pad_y, mark_z), (0.45, 4.0, 0.035), MAT_MARK, COL_ROOF)
box("HELIPAD_MARK_H_RIGHT", (pad_x+2.0, pad_y, mark_z), (0.45, 4.0, 0.035), MAT_MARK, COL_ROOF)
for x, y, sx, sy in [(pad_x, pad_y+9, 22, .22), (pad_x, pad_y-9, 22, .22),
                      (pad_x-10.9, pad_y, .22, 18), (pad_x+10.9, pad_y, .22, 18)]:
    box("HELIPAD_PERIMETER_MARK", (x, y, mark_z), (sx, sy, .035), MAT_MARK, COL_ROOF)

# HVAC equipment arranged in a service zone away from helipad approach.
for i, (x, y) in enumerate([(-19, 10), (-13, 10), (-19, 16), (-13, 16)]):
    box(f"HVAC_UNIT_{i+1}", (x, y, roof_z+1.0), (4.0, 3.0, 1.6), MAT_DARK, COL_ROOF, 0.08)
    box(f"HVAC_BASE_{i+1}", (x, y, roof_z+0.2), (4.4, 3.4, 0.25), MAT_CONCRETE, COL_ROOF)

# Stair cores / vertical circulation placeholders, aligned through all floors.
for sx in [-22.0, 22.0]:
    box(f"STAIR_CORE_MASS_{sx}", (sx, 0, roof_z/2), (5.0, 8.0, roof_z), MAT_ZONE, COL_INTERIOR)
# Elevator shaft placeholder.
box("ELEVATOR_SHAFT_MASS", (0, 0, roof_z/2), (3.2, 3.2, roof_z), MAT_DARK, COL_INTERIOR)

# Named zoning labels use empty objects, useful for later layout iteration.
zones = [
    ("GROUND_PUBLIC_LOBBY_BOOKING", (-14, -10, 1.2)),
    ("GROUND_CELLS_HOLDING", (16, 9, 1.2)),
    ("GROUND_VEHICLE_GARAGE", (0, 13, 1.2)),
    ("LEVEL2_DISPATCH_SWAT", (0, 10, FLOOR_H+1.2)),
    ("LEVEL2_EVIDENCE_ARMORY", (-16, 10, FLOOR_H+1.2)),
    ("LEVEL3_DETECTIVES_INTERVIEWS", (0, 10, 2*FLOOR_H+1.2)),
    ("ROOF_HELIPAD", (pad_x, pad_y, roof_z+1.0)),
]
for name, loc in zones:
    o = bpy.data.objects.new(PREFIX + "ZONE_" + name, None)
    o.empty_display_type = "CUBE"
    o.empty_display_size = 1.0
    o.location = loc
    COL_GUIDES.objects.link(o)

# Collision proxies: simplified, closed blockout volumes, not final GTA collision meshes.
box("COLLISION_BUILDING_ENVELOPE", (0, 0, roof_z/2), (W-0.3, D-0.3, roof_z), None, COL_COLLISION)
box("COLLISION_CANOPY", (0, -D/2-3.0, 4.0), (22.5, 5.5, 0.5), None, COL_COLLISION)
box("COLLISION_HELIPAD", (pad_x, pad_y, roof_z+0.2), (21.5, 19.5, 0.25), None, COL_COLLISION)

# Helpful scene defaults and camera.
bpy.ops.object.camera_add(location=(78, -96, 72))
camera = bpy.context.object
camera.name = PREFIX + "BLOCKOUT_CAMERA"
direction = Vector((0, 0, 12)) - camera.location
camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
camera.data.lens = 42
scene.camera = camera
move_to(camera, COL_GUIDES)

bpy.ops.object.light_add(type="AREA", location=(0, -35, 65))
light = bpy.context.object
light.name = PREFIX + "BLOCKOUT_KEY_LIGHT"
light.data.energy = 6500
light.data.shape = "DISK"
light.data.size = 45
move_to(light, COL_GUIDES)

# Select the overall envelope for easy inspection after generation.
bpy.ops.object.select_all(action="DESELECT")
envelope = bpy.data.objects.get(PREFIX + "COLLISION_BUILDING_ENVELOPE")
if envelope:
    envelope.select_set(True)
    bpy.context.view_layer.objects.active = envelope

print("PDHQ Stage 2 blockout generated. Review dimensions, circulation, and zoning before detailed modeling.")
