#!/usr/bin/env python3
"""Stage 40: derive a review-only wall and door coordination schedule.

Uses Stage 36 room intent and Stage 37 rectangle placements. Output is a
schematic coordination aid, not a construction drawing or code-compliance check.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

EPS = 0.05
EDGE_MARGIN = 0.15


def shared_edge(a, b, eps=EPS):
    ax0, ay0, ax1, ay1 = a["x"], a["y"], a["x"] + a["width"], a["y"] + a["depth"]
    bx0, by0, bx1, by1 = b["x"], b["y"], b["x"] + b["width"], b["y"] + b["depth"]
    if abs(ax1 - bx0) <= eps or abs(bx1 - ax0) <= eps:
        lo, hi = max(ay0, by0), min(ay1, by1)
        if hi - lo > EPS:
            return {"orientation": "vertical", "coordinate_m": round((ax1 + bx0) / 2 if abs(ax1 - bx0) <= eps else (bx1 + ax0) / 2, 3),
                    "start_m": round(lo, 3), "end_m": round(hi, 3), "length_m": round(hi - lo, 3)}
    if abs(ay1 - by0) <= eps or abs(by1 - ay0) <= eps:
        lo, hi = max(ax0, bx0), min(ax1, bx1)
        if hi - lo > EPS:
            return {"orientation": "horizontal", "coordinate_m": round((ay1 + by0) / 2 if abs(ay1 - by0) <= eps else (by1 + ay0) / 2, 3),
                    "start_m": round(lo, 3), "end_m": round(hi, 3), "length_m": round(hi - lo, 3)}
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--schedule", default="stage36/room_program_and_adjacency.json")
    p.add_argument("--output", default="build/stage40_wall_door_schedule.json")
    p.add_argument("--fit-report", default="", help="Optional existing Stage 37 JSON; otherwise run Stage 37")
    args = p.parse_args()
    root = Path.cwd()
    schedule_path = Path(args.schedule)
    schedule = json.loads(schedule_path.read_text(encoding="utf-8"))
    if args.fit_report:
        fit = json.loads(Path(args.fit_report).read_text(encoding="utf-8"))
    else:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            temp_path = Path(tmp.name)
        try:
            proc = subprocess.run([sys.executable, "stage37/audit_stage37_floor_fit.py", str(schedule_path), "--output", str(temp_path)],
                                  capture_output=True, text=True)
            if proc.returncode:
                raise SystemExit("Stage 37 fit audit failed: " + proc.stderr[-1500:])
            fit = json.loads(temp_path.read_text(encoding="utf-8"))
        finally:
            temp_path.unlink(missing_ok=True)

    room_by_id = {r["id"]: r for r in schedule["rooms"]}
    placements = []
    for floor_key, result in fit.get("floor_results", {}).items():
        placements.extend(result.get("placements", []))
    place_by_id = {r["id"]: r for r in placements}
    intended = set()
    invalid_refs = []
    for room in schedule["rooms"]:
        for other_id in room.get("adjacent_to", []):
            pair = tuple(sorted((room["id"], other_id)))
            intended.add(pair)
            if other_id not in room_by_id:
                invalid_refs.append({"pair": list(pair), "issue": "referenced room ID does not exist"})

    shared_pairs = {}
    for i, a in enumerate(placements):
        for b in placements[i + 1:]:
            if a.get("floor") != b.get("floor"):
                continue
            edge = shared_edge(a, b)
            if edge:
                shared_pairs[tuple(sorted((a["id"], b["id"])))] = edge

    door_candidates, review_items = [], []
    for pair in sorted(intended):
        a_id, b_id = pair
        if a_id not in room_by_id or b_id not in room_by_id:
            continue
        ra, rb = room_by_id[a_id], room_by_id[b_id]
        pa, pb = place_by_id.get(a_id), place_by_id.get(b_id)
        if pa is None or pb is None:
            review_items.append({"rooms": list(pair), "issue": "one or both rooms unplaced; wall and door cannot be coordinated"})
            continue
        if ra["floor"] != rb["floor"]:
            review_items.append({"rooms": list(pair), "issue": "cross-floor adjacency requires a verified stair/elevator/route, not a direct door"})
            continue
        edge = shared_pairs.get(pair)
        if not edge:
            review_items.append({"rooms": list(pair), "issue": "intended adjacency has no shared rectangle edge; redesign placement or document a corridor connection"})
            continue
        width_a = float(ra.get("door_clear_width_m", 0))
        width_b = float(rb.get("door_clear_width_m", 0))
        clear_width = min(width_a, width_b, max(0, edge["length_m"] - 2 * EDGE_MARGIN))
        if clear_width <= 0:
            review_items.append({"rooms": list(pair), "issue": "shared edge too short for a positive candidate opening"})
            continue
        door_candidates.append({
            "door_id": "D-" + "-".join(pair),
            "rooms": list(pair),
            "floor": ra["floor"],
            "edge": edge,
            "candidate_clear_width_m": round(clear_width, 2),
            "opening_center_m": round((edge["start_m"] + edge["end_m"]) / 2, 3),
            "status": "candidate_requires_human_review",
            "zone_pair": [ra.get("zone", "unspecified"), rb.get("zone", "unspecified")],
            "security_review_required": ra.get("zone") != rb.get("zone"),
            "swing_and_accessibility_review_required": True
        })

    external_edges = []
    for placement in placements:
        x, y, w, d = (placement[k] for k in ("x", "y", "width", "depth"))
        sides = {
            "west": {"orientation": "vertical", "coordinate_m": x, "start_m": y, "end_m": y+d},
            "east": {"orientation": "vertical", "coordinate_m": x+w, "start_m": y, "end_m": y+d},
            "south": {"orientation": "horizontal", "coordinate_m": y, "start_m": x, "end_m": x+w},
            "north": {"orientation": "horizontal", "coordinate_m": y+d, "start_m": x, "end_m": x+w},
        }
        for side, edge in sides.items():
            neighbors = []
            for other in placements:
                if other["id"] == placement["id"] or other.get("floor") != placement.get("floor"):
                    continue
                shared = shared_edge(placement, other)
                if shared and shared["orientation"] == edge["orientation"] and abs(shared["coordinate_m"] - edge["coordinate_m"]) <= EPS:
                    overlap = max(0, min(edge["end_m"], shared["end_m"]) - max(edge["start_m"], shared["start_m"]))
                    if overlap > EPS:
                        neighbors.append(other["id"])
            if not neighbors:
                external_edges.append({"room_id": placement["id"], "floor": placement["floor"], "side": side,
                                       **{k: round(v, 3) if isinstance(v, (int, float)) else v for k, v in edge.items()},
                                       "status": "perimeter_candidate_check_facade_and_actual_wall_geometry"})

    report = {
        "stage": 40,
        "source_schedule": str(schedule_path),
        "method": "rectangle edge analysis using Stage 37 schematic placements",
        "room_count": len(room_by_id),
        "placed_room_count": len(place_by_id),
        "intended_adjacency_pair_count": len(intended),
        "door_opening_candidates": door_candidates,
        "perimeter_wall_candidates": external_edges,
        "review_items": review_items,
        "invalid_adjacency_references": invalid_refs,
        "production_ready": False,
        "limitations": [
            "This is a schematic rectangle-based schedule, not real wall geometry or a construction drawing.",
            "It does not determine wall thickness, structural openings, fire ratings, code compliance, door swing, accessibility, egress, or security-system requirements.",
            "Door candidates are only suggested where intended rooms share a rectangle edge; routes through corridors and cross-floor links need separate design.",
            "Validate all openings in the actual Blender scene and with appropriate qualified review before export."
        ]
    }
    out = Path(args.output)
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"stage": 40, "output": str(out), "door_candidates": len(door_candidates),
                      "perimeter_candidates": len(external_edges), "review_items": len(review_items),
                      "production_ready": False}, indent=2))


if __name__ == "__main__":
    main()
