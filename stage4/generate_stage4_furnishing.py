"""Stage 4 furnishing and security-prop blockout for PDHQ.

Run Stage 2, then Stage 3, then this script in the SAME Blender scene.
All objects are schematic metre-scale proxies for layout/clearance review,
not production-ready props, collision, textures, or Sollumz-ready assets.
"""
import bpy

PREFIX = "PDHQ_"
FLOOR_H = 4.2
scene = bpy.context.scene

def get_collection(name):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        scene.collection.children.link(col)
    return col

def clear_collection(col):
    for obj in list(col.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

def material(name, color, metallic=0.0, roughness=0.65):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1)
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return mat

furn = get_collection("PDHQ_FURNITURE_BLOCKOUT")
clear_collection(furn)
guides = get_collection("PDHQ_GUIDES")
mat_dark = material("MAT_Stage4_Graphite", (0.10, 0.13, 0.15), 0.25)
mat_case = material("MAT_Stage4_Casework", (0.34, 0.39, 0.41))
mat_top = material("MAT_Stage4_Worktops", (0.57, 0.60, 0.60))
mat_secure = material("MAT_Stage4_SecureSteel", (0.22, 0.25, 0.27), 0.55)
mat_screen = material("MAT_Stage4_Display", (0.06, 0.19, 0.22), 0.12)
mat_label = material("MAT_Stage4_SafetyYellow", (0.95, 0.62, 0.10))

def cube(name, loc, dims, mat, bevel=0.025):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = PREFIX + name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    if bevel:
        mod = obj.modifiers.new("Blockout_Rounded_Edges", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    furn.objects.link(obj)
    return obj

def desk(name, x, y, z, width=1.8, depth=0.75, height=0.76, monitor=True):
    cube(name+"_TOP", (x,y,z+height), (width,depth,0.08), mat_top)
    cube(name+"_PEDESTAL", (x-width*0.30,y,z+height*0.48), (0.42,depth*0.72,height*0.9), mat_case)
    cube(name+"_LEG", (x+width*0.36,y,z+height*0.48), (0.08,depth*0.72,height*0.9), mat_dark, 0.01)
    if monitor:
        cube(name+"_MONITOR", (x,y+depth*0.20,z+height+0.28), (0.52,0.09,0.32), mat_screen, 0.015)
        cube(name+"_KEYBOARD", (x,y-depth*0.18,z+height+0.05), (0.38,0.16,0.025), mat_dark, 0.008)

def cabinet(name, x, y, z, width=0.9, depth=0.45, height=1.8, shelves=3, mat=mat_case):
    cube(name+"_BODY", (x,y,z+height/2), (width,depth,height), mat)
    for i in range(1,shelves+1):
        zz = z + height*i/(shelves+1)
        cube(name+"_SHELF_"+str(i), (x,y-depth*0.02,zz), (width*0.94,depth*1.02,0.035), mat_top, 0.008)

def bench(name, x, y, z, length=1.8):
    cube(name+"_SEAT", (x,y,z+0.48), (length,0.48,0.10), mat_secure)
    for dx in (-length*0.40, length*0.40):
        cube(name+"_SUPPORT", (x+dx,y,z+0.24), (0.08,0.42,0.48), mat_dark, 0.01)

# Ground floor: reception, booking intake, holding-cell bench proxies and
# garage workbench. Coordinates are aligned to the Stage 2/3 centre-origin plan.
desk("F1_RECEPTION_COUNTER", -15, -12, 0.15, 3.8, 0.95, 1.05, True)
for i, x in enumerate((-8.5,-5.5,-2.5)):
    desk("F1_BOOKING_INTAKE_"+str(i+1), x, -11, 0.15, 1.55, 0.72, 0.76, True)
for i, x in enumerate((12.5,16.5,20.5)):
    bench("F1_HOLDING_BENCH_"+str(i+1), x, 8.0, 0.15, 2.0)
    cabinet("F1_CELL_STORAGE_"+str(i+1), x, 11.5, 0.15, 0.55, 0.5, 1.4, 2, mat_secure)
desk("F1_GARAGE_WORKBENCH", 1.0, 14.0, 0.15, 3.2, 0.8, 0.9, False)
# Vehicle-size clearance boxes are guides only; remove/replace before final export.
for i, x in enumerate((-9.0, 0.0, 9.0)):
    cube("F1_GARAGE_VEHICLE_CLEARANCE_"+str(i+1), (x, 10.5, 0.95), (2.6, 5.8, 1.7), mat_label, 0.0)

# Level 2: dispatch console line, evidence storage and armory lockers.
z2 = FLOOR_H + 0.15
for i, x in enumerate((-7.0,-3.0,1.0,5.0,9.0)):
    desk("F2_DISPATCH_CONSOLE_"+str(i+1), x, 11.0, z2, 2.3, 0.85, 0.82, True)
for i, x in enumerate((-20.0,-16.0,-12.0)):
    cabinet("F2_EVIDENCE_CABINET_"+str(i+1), x, 11.0, z2, 1.1, 0.65, 2.0, 4, mat_secure)
for i, x in enumerate((-20.0,-17.5,-15.0,-12.5)):
    cabinet("F2_ARMORY_LOCKER_"+str(i+1), x, 7.0, z2, 0.72, 0.55, 2.0, 1, mat_secure)
desk("F2_SWAT_BRIEFING_TABLE", 15.0, 10.0, z2, 4.2, 1.5, 0.76, False)

# Level 3: detective workstations, interview tables, and conference table.
z3 = 2*FLOOR_H + 0.15
for i, (x,y) in enumerate(((-8,10),(-4,10),(0,10),(4,10),(8,10),(-8,15),(-4,15),(0,15),(4,15),(8,15))):
    desk("F3_DETECTIVE_DESK_"+str(i+1), x, y, z3, 1.5, 0.7, 0.76, True)
for i, x in enumerate((-18.0,-11.0)):
    cube("F3_INTERVIEW_TABLE_"+str(i+1), (x,10.0,z3+0.40), (1.6,0.85,0.08), mat_top)
    for side in (-1,1):
        bench("F3_INTERVIEW_SEAT_"+str(i+1)+"_"+str(side), x, 10.0+side*1.15, z3, 0.75)
cube("F3_CONFERENCE_TABLE", (16.0,11.0,z3+0.40), (4.0,1.5,0.08), mat_top)
for i, x in enumerate((14.5,16.0,17.5)):
    bench("F3_CONFERENCE_SEAT_"+str(i+1), x, 9.7, z3, 0.65)
for i, x in enumerate((12.0,15.0,18.0)):
    cabinet("F3_FILE_STORAGE_"+str(i+1), x, 15.0, z3, 0.8, 0.45, 1.8, 3)

# Guide labels are empties so teams can hide/show them separately from geometry.
for name, loc in [
    ("STAGE4_GARAGE_CLEARANCE_REVIEW", (0,10.5,1.0)),
    ("STAGE4_DISPATCH_CONSOLE_REVIEW", (1,11,FLOOR_H+1.4)),
    ("STAGE4_SECURE_STORAGE_REVIEW", (-16,10,FLOOR_H+1.3)),
    ("STAGE4_INTERVIEW_FURNITURE_REVIEW", (-14.5,10,2*FLOOR_H+1.3)),
]:
    obj = bpy.data.objects.new(PREFIX+"GUIDE_"+name, None)
    obj.empty_display_type = "SPHERE"
    obj.empty_display_size = 0.5
    obj.location = loc
    guides.objects.link(obj)

print("Stage 4 furniture/security blockout created. Review access paths, door swings, vehicle clearance, and stair circulation.")
