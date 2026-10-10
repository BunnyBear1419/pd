#!/usr/bin/env python3
"""Stage 37: deterministic rectangle-fit screening for the Stage 36 room schedule.

This is a schematic 2D packing exercise only. It is not a floor-plan drawing,
wall layout, egress/accessibility analysis, or a substitute for Blender review.
"""
import argparse
import json
from pathlib import Path

STEP = 0.5
MARGIN = 0.5
CORRIDOR_HALF_WIDTH = 1.2

def overlaps(a, b, eps=1e-8):
    return (a["x"] < b["x"] + b["width"] - eps and
            a["x"] + a["width"] > b["x"] + eps and
            a["y"] < b["y"] + b["depth"] - eps and
            a["y"] + a["depth"] > b["y"] + eps)

def positions(start, end, step=STEP):
    n = int(round((end - start) / step))
    return [round(start + i * step, 4) for i in range(max(0, n) + 1)]

def candidate_xs(width, half_width, footprint_half_width):
    xs = []
    xs.extend(positions(-footprint_half_width + MARGIN,
                        -CORRIDOR_HALF_WIDTH - width))
    xs.extend(positions(CORRIDOR_HALF_WIDTH,
                        footprint_half_width - MARGIN - width))
    return xs

def fit_floor(rooms, footprint):
    half_w = footprint["width"] / 2
    half_d = footprint["depth"] / 2
    min_y, max_y = -half_d + MARGIN, half_d - MARGIN
    placed, failures = [], []
    # Large rooms first; stable ID ordering makes the output repeatable.
    ordered = sorted(rooms, key=lambda r: (-(r["dimensions_m"][0] * r["dimensions_m"][1]), r["id"]))
    for room in ordered:
        base_w, base_d = room["dimensions_m"]
        options = [(base_w, base_d, False)]
        if base_w != base_d:
            options.append((base_d, base_w, True))
        found = None
        for width, depth, rotated in options:
            if width > (half_w - CORRIDOR_HALF_WIDTH - MARGIN) or depth > (max_y - min_y):
                continue
            xs = candidate_xs(width, half_w, half_w)
            ys = positions(min_y, max_y - depth)
            # Prefer front-to-back compact placement; test each side of the central corridor.
            for y in ys:
                for x in xs:
                    candidate = {"id": room["id"], "name": room["name"], "floor": room["floor"],
                                 "x": x, "y": y, "width": width, "depth": depth,
                                 "rotated_90_degrees": rotated, "use": room["use"], "zone": room["zone"]}
                    if any(overlaps(candidate, existing) for existing in placed):
                        continue
                    found = candidate
                    break
                if found:
                    break
            if found:
                break
        if found:
            placed.append(found)
        else:
            failures.append({"id": room["id"], "name": room["name"], "dimensions_m": room["dimensions_m"]})
    pair_overlaps = []
    for i, a in enumerate(placed):
        for b in placed[i+1:]:
            if overlaps(a, b):
                pair_overlaps.append([a["id"], b["id"]])
    return placed, failures, pair_overlaps

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schedule", nargs="?", default="stage36/room_program_and_adjacency.json")
    parser.add_argument("--output", default="", help="Optional JSON output path; otherwise print to stdout")
    args = parser.parse_args()
    schedule_path = Path(args.schedule)
    data = json.loads(schedule_path.read_text(encoding="utf-8"))
    footprint = data["footprint_reference"]
    floor_results = {}
    all_errors = []
    for floor in (1, 2, 3):
        rooms = [r for r in data["rooms"] if r["floor"] == floor]
        placed, failures, pair_overlaps = fit_floor(rooms, footprint)
        floor_results[str(floor)] = {
            "room_count": len(rooms), "placed_count": len(placed),
            "placements": sorted(placed, key=lambda r: r["id"]),
            "unplaced_rooms": failures, "overlap_pairs": pair_overlaps,
            "central_corridor_reserved_width_m": CORRIDOR_HALF_WIDTH * 2,
            "perimeter_margin_m": MARGIN,
            "fit_pass": not failures and not pair_overlaps,
        }
        if failures:
            all_errors.append(f"Floor {floor}: {len(failures)} room(s) could not be placed.")
        if pair_overlaps:
            all_errors.append(f"Floor {floor}: overlap pairs detected.")
    roof_rooms = [r for r in data["rooms"] if r["floor"] == "roof"]
    roof_results = []
    for room in roof_rooms:
        width, depth = room["dimensions_m"]
        fits = width <= footprint["width"] - 2*MARGIN and depth <= footprint["depth"] - 2*MARGIN
        roof_results.append({"id": room["id"], "dimensions_m": [width, depth],
                             "fits_nominal_footprint_with_margin": fits,
                             "centered_origin_xy_m": [0, 0]})
        if not fits:
            all_errors.append(f"Roof room {room['id']} exceeds nominal roof footprint.")
    result = {
        "stage": 37,
        "method": "0.5 m grid rectangle packing in two wings with a reserved 2.4 m central spine",
        "footprint_reference_m": [footprint["width"], footprint["depth"]],
        "floor_results": floor_results,
        "roof_envelopes": roof_results,
        "errors": all_errors,
        "fit_screen_pass": not all_errors,
        "production_ready": False,
        "limitations": [
            "Rectangles represent target room clear areas, not wall thickness or actual room polygons.",
            "Adjacency intentions are not guaranteed by this packing algorithm.",
            "Corridor spine is reserved but doors, door swings, stairs, elevator, columns, furniture, and egress paths are not geometrically modeled.",
            "A pass is only a coarse packing result; validate the proposed coordinates against the Blender scene and qualified design reviews."
        ]
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    raise SystemExit(1 if all_errors else 0)

if __name__ == "__main__":
    main()
