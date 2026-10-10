#!/usr/bin/env python3
"""Stage 36: validate the room-program schedule before architectural modeling."""
import argparse
import json
from collections import Counter
from pathlib import Path

REQUIRED = {
    "public_entry", "public_wc", "booking", "processing", "cells", "interview",
    "evidence_intake", "evidence_vault", "armory", "patrol_support", "secure_transfer",
    "garage", "vertical_core", "dispatch", "command", "detectives", "briefing",
    "it_comms", "swat_briefing", "swat_gear", "locker", "showers", "fitness",
    "roof_access", "helipad",
}

def validate(data):
    errors, warnings = [], []
    rooms = data.get("rooms", [])
    ids = [r.get("id") for r in rooms]
    duplicates = [k for k, count in Counter(ids).items() if count > 1]
    if duplicates:
        errors.append("Duplicate room IDs: " + ", ".join(map(str, duplicates)))
    if not rooms:
        errors.append("No room records found.")
    known = set(ids)
    uses = set()
    for room in rooms:
        rid = room.get("id", "<missing-id>")
        dims = room.get("dimensions_m", [])
        if not isinstance(dims, list) or len(dims) != 2 or any(not isinstance(v, (int, float)) or v <= 0 for v in dims):
            errors.append(f"{rid}: dimensions_m must contain two positive numbers.")
        width = room.get("door_clear_width_m")
        if room.get("use") != "helipad" and (not isinstance(width, (int, float)) or width < data.get("door_width_screening_min_m", 0.8)):
            errors.append(f"{rid}: door clear width below screening minimum or missing.")
        uses.add(room.get("use"))
        for target in room.get("adjacent_to", []):
            if target not in known:
                errors.append(f"{rid}: adjacency references unknown room ID {target}.")
        if room.get("floor") not in (1, 2, 3, "roof"):
            errors.append(f"{rid}: floor must be 1, 2, 3, or 'roof'.")
    missing = sorted(REQUIRED - uses)
    if missing:
        errors.append("Required facility types missing: " + ", ".join(missing))
    for floor in (1, 2, 3):
        floor_rooms = [r for r in rooms if r.get("floor") == floor]
        gross = data.get("footprint_reference", {}).get("width", 0) * data.get("footprint_reference", {}).get("depth", 0)
        target_net = sum(r["dimensions_m"][0] * r["dimensions_m"][1] for r in floor_rooms if isinstance(r.get("dimensions_m"), list) and len(r["dimensions_m"]) == 2 and all(isinstance(v, (int, float)) and v > 0 for v in r["dimensions_m"]))
        if target_net > gross * 0.72:
            warnings.append(f"Floor {floor}: scheduled net room area {target_net:.1f} m² exceeds 72% of reference gross floor area; check fit and circulation.")
    if data.get("status") != "design_schedule_not_modeled_or_code_compliance_certified":
        warnings.append("Status label should make clear this is a design schedule, not a validated model.")
    return errors, warnings

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schedule", nargs="?", default="stage36/room_program_and_adjacency.json")
    args = parser.parse_args()
    path = Path(args.schedule)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(f"cannot read schedule: {exc}")
    errors, warnings = validate(data)
    result = {"stage": 36, "schedule": str(path), "room_count": len(data.get("rooms", [])), "errors": errors, "warnings": warnings, "valid": not errors, "production_ready": False}
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if errors else 0)

if __name__ == "__main__":
    main()
