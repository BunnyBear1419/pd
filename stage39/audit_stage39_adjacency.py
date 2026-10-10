#!/usr/bin/env python3
"""Stage 39: audit intended room adjacency against Stage 37 schematic placements.

Reports proximity and same-floor edge contact. It never moves geometry and does
not treat geometric proximity as proof of a usable door or compliant route.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEDULE = ROOT / "stage36/room_program_and_adjacency.json"

def rect_gap(a, b):
    """Euclidean separation between two axis-aligned rectangles; zero if touching/overlapping."""
    dx = max(a["x"] - (b["x"] + b["width"]),
             b["x"] - (a["x"] + a["width"]), 0.0)
    dy = max(a["y"] - (b["y"] + b["depth"]),
             b["y"] - (a["y"] + a["depth"]), 0.0)
    return (dx * dx + dy * dy) ** 0.5

def shared_edge_length(a, b, eps=0.05):
    """Length of a shared boundary segment, if rectangles nearly touch."""
    ax1, ax2 = a["x"], a["x"] + a["width"]
    ay1, ay2 = a["y"], a["y"] + a["depth"]
    bx1, bx2 = b["x"], b["x"] + b["width"]
    by1, by2 = b["y"], b["y"] + b["depth"]
    vertical = min(abs(ax2 - bx1), abs(bx2 - ax1)) <= eps
    horizontal = min(abs(ay2 - by1), abs(by2 - ay1)) <= eps
    if vertical:
        return max(0.0, min(ay2, by2) - max(ay1, by1))
    if horizontal:
        return max(0.0, min(ax2, bx2) - max(ax1, bx1))
    return 0.0

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schedule", default=str(DEFAULT_SCHEDULE))
    parser.add_argument("--output", default="build/stage39_adjacency_report.json")
    parser.add_argument("--near-threshold-m", type=float, default=1.5,
                        help="Distance within which an adjacency is flagged as near, not proven")
    args = parser.parse_args()
    schedule_path = Path(args.schedule).resolve()
    schedule = json.loads(schedule_path.read_text(encoding="utf-8"))
    if args.near_threshold_m < 0:
        parser.error("--near-threshold-m must be non-negative")

    with tempfile.TemporaryDirectory(prefix="pdhq_stage39_") as td:
        fit_path = Path(td) / "stage37_fit.json"
        proc = subprocess.run(
            [sys.executable, str(ROOT / "stage37/audit_stage37_floor_fit.py"),
             str(schedule_path), "--output", str(fit_path)],
            capture_output=True, text=True, cwd=ROOT)
        if not fit_path.exists():
            raise RuntimeError("Stage 37 failed to produce a fit report: " + proc.stderr)
        fit = json.loads(fit_path.read_text(encoding="utf-8"))

    rooms = {room["id"]: room for room in schedule["rooms"]}
    placements = {}
    for floor_data in fit["floor_results"].values():
        for placement in floor_data.get("placements", []):
            placements[placement["id"]] = placement

    adjacency_checks = []
    missing_refs = []
    seen_pairs = set()
    for room in schedule["rooms"]:
        for target_id in room.get("adjacent_to", []):
            pair = tuple(sorted((room["id"], target_id)))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            target = rooms.get(target_id)
            if target is None:
                missing_refs.append({"from": room["id"], "to": target_id})
                adjacency_checks.append({"from": room["id"], "to": target_id,
                                         "status": "INVALID_REFERENCE"})
                continue
            a, b = placements.get(room["id"]), placements.get(target_id)
            if a is None or b is None:
                status = "UNPLACED"
                gap = None
                edge = 0.0
            elif room["floor"] != target["floor"]:
                status = "CROSS_FLOOR_REQUIRES_VERTICAL_ROUTE_REVIEW"
                gap = None
                edge = 0.0
            else:
                gap = round(rect_gap(a, b), 3)
                edge = round(shared_edge_length(a, b), 3)
                if edge > 0:
                    status = "SHARED_EDGE_CANDIDATE"
                elif gap <= args.near_threshold_m:
                    status = "NEAR_NOT_ADJACENT"
                else:
                    status = "NOT_ADJACENT_IN_PACKING"
            adjacency_checks.append({
                "from": room["id"], "to": target_id,
                "from_name": room["name"], "to_name": target["name"],
                "floor_from": room["floor"], "floor_to": target["floor"],
                "status": status, "rectangle_gap_m": gap,
                "shared_edge_length_m": edge,
                "note": "Candidate only; door, wall opening, access control and route usability require Blender review."
            })

    counts = {}
    for item in adjacency_checks:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    report = {
        "stage": 39,
        "method": "Compare Stage 36 adjacency intentions with Stage 37 rectangle placement",
        "near_threshold_m": args.near_threshold_m,
        "adjacency_pair_count": len(adjacency_checks),
        "status_counts": counts,
        "checks": adjacency_checks,
        "missing_room_references": missing_refs,
        "fit_screen_pass": fit.get("fit_screen_pass", False),
        "design_review_required": True,
        "production_ready": False,
        "limitations": [
            "Stage 37 is a coarse rectangle packing algorithm and does not optimize adjacency.",
            "Shared rectangle edges do not prove a wall opening, door, or passable connection exists.",
            "Cross-floor references require actual stairs/elevator and secure-route review.",
            "This report is advisory; no rooms or geometry are moved or modified."
        ]
    }
    out = Path(args.output)
    if not out.is_absolute():
        out = (ROOT / out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"stage": 39, "report": str(out),
                      "adjacency_pair_count": len(adjacency_checks),
                      "status_counts": counts, "production_ready": False}, indent=2))
    # Structural errors are fatal; layout mismatches are deliberately advisory.
    if missing_refs:
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
