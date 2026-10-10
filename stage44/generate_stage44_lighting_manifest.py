#!/usr/bin/env python3
"""Stage 44: generate a conservative lighting placement manifest for Blender review."""
import argparse
import json
from pathlib import Path

ROOM_LIGHTS = {
    "public_entry": ("AREA", 1400.0, 5.0, "neutral_warm"),
    "public_wc": ("AREA", 500.0, 3.0, "neutral"),
    "booking": ("AREA", 900.0, 4.0, "neutral"),
    "processing": ("AREA", 850.0, 4.0, "neutral"),
    "cells": ("AREA", 450.0, 3.0, "neutral"),
    "interview": ("AREA", 500.0, 3.0, "neutral_warm"),
    "evidence_intake": ("AREA", 850.0, 4.0, "neutral"),
    "evidence_vault": ("AREA", 600.0, 3.0, "neutral"),
    "armory": ("AREA", 750.0, 3.0, "neutral"),
    "patrol_support": ("AREA", 650.0, 4.0, "neutral"),
    "garage": ("AREA", 1800.0, 7.0, "neutral"),
    "dispatch": ("AREA", 650.0, 3.0, "cool_neutral"),
    "operations": ("AREA", 700.0, 4.0, "neutral"),
    "command": ("AREA", 450.0, 3.0, "neutral_warm"),
    "detectives": ("AREA", 500.0, 3.0, "neutral"),
    "briefing": ("AREA", 650.0, 4.0, "neutral"),
    "it_comms": ("AREA", 500.0, 3.0, "neutral"),
    "swat_briefing": ("AREA", 700.0, 4.0, "neutral"),
    "swat_gear": ("AREA", 700.0, 3.0, "neutral"),
    "locker": ("AREA", 550.0, 3.0, "neutral"),
    "showers": ("AREA", 400.0, 3.0, "neutral"),
    "fitness": ("AREA", 550.0, 4.0, "neutral"),
    "staff_rest": ("AREA", 300.0, 3.0, "warm"),
    "tactical_command": ("AREA", 650.0, 3.0, "cool_neutral"),
}
COLOR_PRESETS = {
    "neutral": [1.0, 0.95, 0.88],
    "neutral_warm": [1.0, 0.82, 0.65],
    "cool_neutral": [0.78, 0.88, 1.0],
    "warm": [1.0, 0.72, 0.48],
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--spec", default="build/stage41_48_design_spec.json")
    p.add_argument("--fit-report", default="build/stage37_floor_fit.json")
    p.add_argument("--schedule", default="stage36/room_program_and_adjacency.json")
    p.add_argument("--output", default="build/stage44_lighting_manifest.json")
    args = p.parse_args()
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    fit = json.loads(Path(args.fit_report).read_text(encoding="utf-8"))
    schedule = json.loads(Path(args.schedule).read_text(encoding="utf-8"))
    placements = {}
    for floor_data in fit.get("floor_results", {}).values():
        for item in floor_data.get("placements", []):
            placements[item["id"]] = item
    floor_height = float(schedule["footprint_reference"]["floor_to_floor_height"])
    lights, skipped = [], []
    for room in spec.get("rooms", []):
        use, rid = room.get("use", "unknown"), room.get("room_id")
        placement = placements.get(rid)
        rule = ROOM_LIGHTS.get(use)
        if not placement or not rule:
            if use not in {"roof_access", "helipad", "vertical_core", "secure_transfer"}:
                skipped.append({"room_id": rid, "use": use, "reason": "no floor placement or no preset; manual lighting required"})
            continue
        x, y, w, d = (float(placement[k]) for k in ("x", "y", "width", "depth"))
        floor = int(placement["floor"])
        kind, power, radius, color_name = rule
        # One center fixture per room is a layout marker, not a photometric design.
        lights.append({
            "name": f"Light_{rid}_{use}", "room_id": rid, "floor": floor,
            "type": kind, "power_w": power, "size_m": min(2.5, max(0.8, min(w, d) * 0.35)),
            "radius_m": radius, "color_rgb": COLOR_PRESETS[color_name],
            "location_m": [round(x + w / 2, 3), round(y + d / 2, 3),
                           round((floor - 1) * floor_height + floor_height - 0.35, 3)],
            "role": "interior_review_light"
        })
    # Roof/exterior entries are deliberately separate markers for scene review.
    lights.extend([
        {"name": "Light_Exterior_Entry_Marker", "room_id": None, "floor": 0, "type": "AREA",
         "power_w": 1000.0, "size_m": 3.0, "radius_m": 8.0, "color_rgb": COLOR_PRESETS["neutral_warm"],
         "location_m": [0.0, -5.0, 4.0], "role": "exterior_review_light",
         "note": "Adjust to the actual site/front entrance origin in Blender."},
        {"name": "Light_Roof_Helipad_Marker", "room_id": "ROOF", "floor": 4, "type": "AREA",
         "power_w": 800.0, "size_m": 2.0, "radius_m": 10.0, "color_rgb": COLOR_PRESETS["neutral"],
         "location_m": [0.0, 0.0, 13.0], "role": "roof_review_light",
         "note": "Placeholder only; aviation marking/light requirements need independent review."}
    ])
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "stage": 44, "status": "lighting_manifest_generated_for_blender_review", "units": "metres",
        "lights": lights, "skipped_rooms": skipped,
        "counts": {"lights": len(lights), "skipped_rooms": len(skipped)},
        "production_ready": False,
        "limitations": [
            "Power, placement, radius and color are visual blockout defaults, not physically calibrated photometry.",
            "One fixture per room is not a final lighting layout; add fixtures after visual review and check shadows.",
            "Exterior and helipad locations are placeholders relative to an unverified site origin.",
            "Do not include review helpers in the GTA export collection without explicit conversion and validation."
        ]
    }
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out), "counts": report["counts"], "production_ready": False}, indent=2))


if __name__ == "__main__":
    main()
