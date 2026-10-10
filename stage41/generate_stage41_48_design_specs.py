#!/usr/bin/env python3
"""Stage 41–48: generate a structured design/optimization brief from the room program.

This creates auditable specifications and review prompts; it does not create
Blender geometry, GTA assets, or a certified building design.
"""
import argparse
import json
from pathlib import Path

ROOM_RULES = {
    "public_entry": {"kit": "public_lobby", "lighting": "bright_public", "collision": "public_walkable", "priority": "high"},
    "public_wc": {"kit": "restroom", "lighting": "uniform_task", "collision": "wet_area_walkable", "priority": "medium"},
    "booking": {"kit": "secure_booking", "lighting": "bright_task", "collision": "secure_walkable", "priority": "high"},
    "processing": {"kit": "processing_bench", "lighting": "bright_task", "collision": "secure_walkable", "priority": "high"},
    "cells": {"kit": "cell_bunks_and_sanitary", "lighting": "durable_uniform", "collision": "high_security_walkable", "priority": "high"},
    "interview": {"kit": "interview_table_chairs_camera", "lighting": "controlled_soft_task", "collision": "walkable_clearance", "priority": "high"},
    "evidence_intake": {"kit": "evidence_counter_and_scanner", "lighting": "bright_task", "collision": "secure_walkable", "priority": "high"},
    "evidence_vault": {"kit": "modular_evidence_shelving", "lighting": "uniform_secure", "collision": "high_security_walkable", "priority": "high"},
    "armory": {"kit": "locked_weapon_and_gear_storage", "lighting": "bright_task", "collision": "high_security_walkable", "priority": "high"},
    "patrol_support": {"kit": "patrol_lockers_and_worktop", "lighting": "uniform_task", "collision": "staff_walkable", "priority": "medium"},
    "secure_transfer": {"kit": "controlled_transfer_corridor", "lighting": "continuous_uniform", "collision": "unobstructed_route", "priority": "high"},
    "garage": {"kit": "vehicle_bays_and_pedestrian_edge", "lighting": "high_bay", "collision": "vehicle_and_pedestrian_separation", "priority": "high"},
    "vertical_core": {"kit": "stair_elevator_core", "lighting": "continuous_route", "collision": "stair_landing_and_lift_clearance", "priority": "high"},
    "dispatch": {"kit": "console_rows_and_display_wall", "lighting": "low_glare_control_room", "collision": "staff_walkable", "priority": "high"},
    "operations": {"kit": "incident_command_table_and_screens", "lighting": "meeting_task", "collision": "staff_walkable", "priority": "medium"},
    "command": {"kit": "command_office", "lighting": "office_task", "collision": "staff_walkable", "priority": "medium"},
    "detectives": {"kit": "case_desks_and_evidence_boards", "lighting": "office_task", "collision": "staff_walkable", "priority": "medium"},
    "briefing": {"kit": "briefing_table_and_display", "lighting": "meeting_task", "collision": "staff_walkable", "priority": "medium"},
    "it_comms": {"kit": "rack_cabinets_and_service_clearance", "lighting": "service_task", "collision": "restricted_walkable", "priority": "high"},
    "swat_briefing": {"kit": "tactical_briefing_table_and_map_wall", "lighting": "briefing_task", "collision": "restricted_walkable", "priority": "high"},
    "swat_gear": {"kit": "tactical_racks_and_kit_benches", "lighting": "bright_task", "collision": "high_security_walkable", "priority": "high"},
    "locker": {"kit": "individual_lockers_and_benches", "lighting": "uniform_task", "collision": "staff_walkable", "priority": "medium"},
    "showers": {"kit": "showers_and_dry_change_zone", "lighting": "uniform_wet_area", "collision": "wet_area_walkable", "priority": "medium"},
    "fitness": {"kit": "fitness_equipment_with_clearance", "lighting": "bright_even", "collision": "equipment_clearance", "priority": "medium"},
    "staff_rest": {"kit": "quiet_seating", "lighting": "warm_low_glare", "collision": "staff_walkable", "priority": "low"},
    "roof_access": {"kit": "protected_roof_access_and_signage", "lighting": "route_and_warning", "collision": "edge_safe_route", "priority": "high"},
    "tactical_command": {"kit": "tactical_monitoring_and_safety_controls", "lighting": "controlled_task", "collision": "restricted_walkable", "priority": "high"},
    "helipad": {"kit": "marked_landing_zone_and_safety_buffer", "lighting": "aviation_review_required", "collision": "roof_surface_and_obstacle_clearance", "priority": "high"},
}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--schedule", default="stage36/room_program_and_adjacency.json")
    p.add_argument("--fit-report", default="build/stage37_floor_fit.json")
    p.add_argument("--output", default="build/stage41_48_design_spec.json")
    args = p.parse_args()
    data = json.loads(Path(args.schedule).read_text(encoding="utf-8"))
    fit_path = Path(args.fit_report)
    fit = json.loads(fit_path.read_text(encoding="utf-8")) if fit_path.exists() else None
    placements = {}
    if fit:
        for result in fit.get("floor_results", {}).values():
            for item in result.get("placements", []):
                placements[item["id"]] = item
    rooms = []
    unknown_uses = []
    for room in data.get("rooms", []):
        use = room.get("use", "unknown")
        rule = ROOM_RULES.get(use)
        if not rule:
            unknown_uses.append({"id": room.get("id"), "use": use})
            rule = {"kit": "manual_room_specific_kit_required", "lighting": "manual_lighting_design_required",
                    "collision": "manual_collision_review_required", "priority": "review"}
        dims = room.get("dimensions_m", [0, 0])
        place = placements.get(room.get("id"))
        rooms.append({
            "room_id": room.get("id"), "name": room.get("name"), "floor": room.get("floor"),
            "use": use, "zone": room.get("zone"), "target_dimensions_m": dims,
            "target_area_m2": round(float(dims[0]) * float(dims[1]), 2),
            "placement_available": place is not None,
            "placement_xywh_m": ({k: place[k] for k in ("x", "y", "width", "depth")} if place else None),
            "interior_kit": rule["kit"], "lighting_intent": rule["lighting"],
            "collision_profile": rule["collision"], "implementation_priority": rule["priority"],
            "door_clear_width_target_m": room.get("door_clear_width_m"),
            "manual_checks": ["furniture does not intersect door swings or circulation",
                              "collision meshes match visible geometry and player-scale use",
                              "materials use shared atlases where appropriate; avoid unnecessary unique materials",
                              "check LOD and occlusion from actual player sightlines"]
        })
    spec = {
        "stage_range": "41-48",
        "status": "generated_design_spec_not_modeled",
        "units": "metres",
        "design_intent": {
            "style": "modern custom police headquarters",
            "front": "negative Y",
            "footprint_reference_m": [data["footprint_reference"]["width"], data["footprint_reference"]["depth"]],
            "floors": data["footprint_reference"]["floors"],
            "facade": ["clear front entry canopy and legible reception", "modular cladding and glazing",
                       "secure service frontage", "garage doors aligned to vehicle approach", "roof edge and helipad safety buffer"],
            "interior": ["consistent door and trim family", "room-specific police furniture kits", "clear public-to-secure transitions",
                         "wayfinding at decision points", "maintainable service access"],
            "lighting": {"principle": "use shared fixture families and deliberate lighting zones",
                         "checks": ["no black navigation pockets", "no excessive emissive surfaces", "avoid needless overlapping lights",
                                    "test at daytime, night, and interior/exterior transitions"]},
            "materials": {"principle": "small reusable PBR material library and texture atlases where sensible",
                          "checks": ["consistent scale and texel density", "applied transforms", "correct normals", "no missing texture paths",
                                     "avoid per-object duplicate materials"]},
            "geometry_budget": {"principle": "modular repeatable assets; remove hidden/internal faces where safe",
                               "checks": ["record triangle counts by room and asset family", "LOD test at real viewing distances",
                                          "keep collision simpler than render mesh", "no destructive decimation without visual QA"]},
            "streaming": {"principle": "validate room visibility and MLO boundaries in the real GTA toolchain",
                          "checks": ["test entry/exit and floor transitions", "verify portals/occlusion where used",
                                     "avoid accidental exterior leakage", "test with multiple clients and reconnects"]},
        },
        "rooms": rooms,
        "unknown_room_uses": unknown_uses,
        "external_toolchain_gates": ["Blender scene build and visual review", "Sollumz archetype/collision/LOD authoring",
                                     "CodeWalker export and visibility review", "FiveM multiplayer streaming/performance test"],
        "production_ready": False,
        "limitations": ["This is a structured design brief, not generated geometry or a valid GTA export.",
                        "All dimensions, safety clearances, aviation details, accessibility, and security boundaries need real-scene review."]
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"stage_range": "41-48", "output": str(out), "rooms": len(rooms),
                      "rooms_with_placement": sum(r["placement_available"] for r in rooms),
                      "unknown_uses": len(unknown_uses), "production_ready": False}, indent=2))

if __name__ == "__main__":
    main()
