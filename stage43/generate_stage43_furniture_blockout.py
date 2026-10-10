#!/usr/bin/env python3
"""Stage 43: generate review-only furniture/equipment blockout boxes from room placements."""
import argparse
import json
from pathlib import Path

# Localized low-poly placeholder kits. These are deliberately simple blockout masses,
# not detailed models or final collision geometry.
KITS = {
    "public_entry": [("reception_counter", 1.8, 0.65, 1.05)],
    "booking": [("booking_desk", 1.4, 0.7, 0.75), ("booking_seat", 0.5, 0.5, 0.9)],
    "processing": [("processing_bench", 1.6, 0.7, 0.9)],
    "cells": [("bunk_placeholder", 1.9, 0.75, 0.55), ("sanitary_fixture_placeholder", 0.5, 0.5, 0.45)],
    "interview": [("interview_table", 1.2, 0.75, 0.75), ("interview_seat_a", 0.45, 0.45, 0.9), ("interview_seat_b", 0.45, 0.45, 0.9)],
    "evidence_intake": [("evidence_counter", 1.6, 0.65, 1.0)],
    "evidence_vault": [("evidence_shelving", 0.45, 1.2, 2.0)],
    "armory": [("locked_storage_rack", 0.5, 1.4, 1.8)],
    "patrol_support": [("patrol_worktop", 1.5, 0.65, 0.9)],
    "garage": [("vehicle_bay_reference", 2.6, 5.2, 1.6)],
    "dispatch": [("dispatch_console", 1.8, 0.75, 1.0), ("display_wall_placeholder", 2.0, 0.18, 1.2)],
    "operations": [("incident_command_table", 1.8, 1.0, 0.75)],
    "command": [("office_desk", 1.4, 0.7, 0.75)],
    "detectives": [("detective_desk", 1.4, 0.7, 0.75), ("case_board_placeholder", 1.4, 0.12, 1.1)],
    "briefing": [("briefing_table", 2.0, 1.0, 0.75)],
    "it_comms": [("server_rack_placeholder", 0.7, 0.8, 2.0)],
    "swat_briefing": [("tactical_briefing_table", 1.8, 0.9, 0.75), ("map_wall_placeholder", 1.8, 0.15, 1.2)],
    "swat_gear": [("tactical_gear_rack", 0.5, 1.2, 1.8)],
    "locker": [("locker_bank", 0.45, 1.6, 1.8), ("changing_bench", 1.2, 0.45, 0.48)],
    "showers": [("shower_unit_placeholder", 0.9, 0.9, 2.1)],
    "fitness": [("fitness_equipment_placeholder", 0.8, 1.0, 1.5)],
    "staff_rest": [("staff_seating", 1.2, 0.65, 0.8)],
    "tactical_command": [("tactical_console", 1.6, 0.7, 1.0)],
    "public_wc": [("restroom_fixture_placeholder", 0.55, 0.7, 0.8)],
}
SKIP_USES = {"vertical_core", "roof_access", "helipad", "secure_transfer"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", default="build/stage41_48_design_spec.json")
    parser.add_argument("--fit-report", default="build/stage37_floor_fit.json")
    parser.add_argument("--output", default="build/stage43_furniture_blockout.json")
    args = parser.parse_args()
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    fit = json.loads(Path(args.fit_report).read_text(encoding="utf-8"))
    if spec.get("stage_range") != "41-48" or not isinstance(spec.get("rooms"), list):
        raise SystemExit("Expected Stage 41-48 room design specification.")
    placements = {}
    for floor_data in fit.get("floor_results", {}).values():
        for p in floor_data.get("placements", []):
            placements[p["id"]] = p
    floor_height = 3.6
    geometry, omitted = [], []
    for room in spec["rooms"]:
        rid, use = room.get("room_id"), room.get("use", "unknown")
        p = placements.get(rid)
        kit = KITS.get(use, [])
        if not p or not kit:
            if use not in SKIP_USES:
                omitted.append({"room_id": rid, "use": use, "reason": "no placement or no safe generic kit"})
            continue
        x, y, w, d = (float(p[k]) for k in ("x", "y", "width", "depth"))
        floor = int(p["floor"])
        # Place only one conservative item by default; keep all placeholder masses
        # near room center and omit items that cannot fit with a 0.25 m edge margin.
        for item_name, sx, sy, sz in kit:
            if sx > w - 0.5 or sy > d - 0.5:
                omitted.append({"room_id": rid, "use": use, "item": item_name, "reason": "item exceeds room clear footprint"})
                continue
            cx, cy = x + w / 2, y + d / 2
            cz = (floor - 1) * floor_height + sz / 2
            geometry.append({
                "role": "furniture_placeholder", "name": f"Furn_{rid}_{item_name}",
                "floor": floor, "center_m": [round(cx, 3), round(cy, 3), round(cz, 3)],
                "size_m": [sx, sy, sz], "room_id": rid, "use": use,
                "note": "Center-positioned schematic placeholder; relocate and clearance-check in Blender."
            })
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "stage": 43, "status": "furniture_equipment_blockout_generated", "units": "metres",
        "geometry": geometry, "omitted_items": omitted,
        "counts": {"geometry_boxes": len(geometry), "omitted_items": len(omitted)},
        "production_ready": False,
        "limitations": [
            "Items are schematic blockout boxes, not detailed furniture, final collision, materials, UVs or GTA assets.",
            "Items are centered in rooms as a starting point and may overlap each other, doors, or circulation; manually reposition and review.",
            "The fit report and room schedule are preliminary design inputs, not an approved architectural plan."
        ]
    }
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out), "counts": report["counts"], "production_ready": False}, indent=2))


if __name__ == "__main__":
    main()
