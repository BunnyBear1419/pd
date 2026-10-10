#!/usr/bin/env python3
"""Stage 52: validate measured MLO performance-profile evidence.

This checks the shape and arithmetic of supplied measurements; it does not benchmark FiveM.
Usage:
  python stage52/validate_stage52_performance_profile.py --profile build/performance_profile.json
  python stage52/validate_stage52_performance_profile.py --self-test
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_NUMERIC = (
    "scene_object_count",
    "evaluated_triangle_count",
    "material_slot_count",
    "texture_file_count",
    "texture_total_bytes",
    "texture_largest_file_bytes",
    "baseline_frame_time_ms",
    "optimized_frame_time_ms",
    "baseline_memory_mb",
    "optimized_memory_mb",
)
DEFAULT_BUDGETS = {
    "scene_object_count": 12000,
    "evaluated_triangle_count": 500000,
    "material_slot_count": 4,
    "texture_largest_file_bytes": 16777216,
    "baseline_frame_time_ms": 0,
    "optimized_frame_time_ms": 0,
    "baseline_memory_mb": 0,
    "optimized_memory_mb": 0,
}


def validate_profile(data: object) -> dict:
    issues: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return {"stage": 52, "status": "BLOCKED_INVALID_PROFILE", "production_ready": False,
                "issues": ["Profile root must be a JSON object."], "warnings": []}
    if data.get("schema_version") != 1:
        issues.append("schema_version must be 1.")
    if not isinstance(data.get("capture"), dict):
        issues.append("Missing capture object; record build, tool versions, location, client count and test duration.")
    else:
        for key in ("captured_utc", "game_build", "tool_versions", "test_location", "client_count", "duration_seconds"):
            if key not in data["capture"] or data["capture"][key] in (None, "", {}):
                issues.append(f"capture.{key} is required.")
    metrics = data.get("metrics")
    if not isinstance(metrics, dict):
        issues.append("Missing metrics object.")
        metrics = {}
    values: dict[str, float] = {}
    for key in REQUIRED_NUMERIC:
        value = metrics.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            issues.append(f"metrics.{key} must be a non-negative number.")
        else:
            values[key] = float(value)
    if values.get("texture_largest_file_bytes", 0) > values.get("texture_total_bytes", float("inf")):
        issues.append("Largest texture file size cannot exceed total texture bytes.")
    if values.get("texture_file_count") == 0 and values.get("texture_total_bytes", 0) != 0:
        issues.append("Texture bytes are non-zero but texture_file_count is zero.")
    if values.get("baseline_frame_time_ms", 0) == 0 or values.get("baseline_memory_mb", 0) == 0:
        warnings.append("Baseline frame-time and memory measurements should be positive for a meaningful comparison.")
    if values.get("optimized_frame_time_ms", 0) == 0 or values.get("optimized_memory_mb", 0) == 0:
        warnings.append("Optimized frame-time and memory measurements should be positive for a meaningful comparison.")
    if values.get("optimized_frame_time_ms", 0) > values.get("baseline_frame_time_ms", 0) > 0:
        warnings.append("Optimized frame time is worse than baseline; investigate and document the regression.")
    if values.get("optimized_memory_mb", 0) > values.get("baseline_memory_mb", 0) > 0:
        warnings.append("Optimized memory is higher than baseline; investigate and document the regression.")
    budgets = data.get("budgets", DEFAULT_BUDGETS)
    if not isinstance(budgets, dict):
        issues.append("budgets must be an object when provided.")
        budgets = {}
    for key in ("scene_object_count", "evaluated_triangle_count", "material_slot_count", "texture_largest_file_bytes"):
        budget = budgets.get(key, DEFAULT_BUDGETS[key])
        observed = values.get(key)
        if isinstance(budget, bool) or not isinstance(budget, (int, float)) or budget <= 0:
            issues.append(f"budgets.{key} must be a positive number.")
        elif observed is not None and observed > budget:
            warnings.append(f"metrics.{key} exceeds review budget ({observed:g} > {budget:g}).")
    if not isinstance(data.get("evidence"), list) or not data.get("evidence"):
        warnings.append("Attach evidence references (screenshots, profiler exports, texture inventory and test notes).")
    if not isinstance(data.get("notes"), str) or not data.get("notes", "").strip():
        warnings.append("Add notes for test conditions, spikes, and visual/collision/streaming regression checks.")
    status = "BLOCKED_INVALID_PROFILE" if issues else ("REVIEW_REQUIRED" if warnings else "PROFILE_SCHEMA_VALID")
    return {
        "stage": 52,
        "status": status,
        "production_ready": False,
        "issues": issues,
        "warnings": warnings,
        "metrics_checked": sorted(values),
        "budget_review": {key: {"observed": values.get(key), "budget": budgets.get(key, DEFAULT_BUDGETS.get(key))}
                          for key in ("scene_object_count", "evaluated_triangle_count", "material_slot_count", "texture_largest_file_bytes")},
        "limitations": [
            "This validator checks supplied values only; it does not measure the Blender scene, GTA assets or FiveM runtime.",
            "Frame time and memory must be measured under repeatable baseline/optimized conditions on the target server/client.",
            "Budget exceedances are review flags, not automatic proof of failure; preserve collision, visibility and gameplay correctness.",
            "This report can never mark the MLO production-ready."
        ]
    }


def self_test() -> None:
    fixture = {
        "schema_version": 1,
        "capture": {
            "captured_utc": "synthetic-fixture-only",
            "game_build": "fixture",
            "tool_versions": {"blender": "fixture", "codewalker": "fixture"},
            "test_location": "fixture",
            "client_count": 1,
            "duration_seconds": 60
        },
        "metrics": {
            "scene_object_count": 100, "evaluated_triangle_count": 1000,
            "material_slot_count": 2, "texture_file_count": 1,
            "texture_total_bytes": 1000, "texture_largest_file_bytes": 1000,
            "baseline_frame_time_ms": 16.7, "optimized_frame_time_ms": 15.0,
            "baseline_memory_mb": 500, "optimized_memory_mb": 450
        },
        "budgets": {"scene_object_count": 12000, "evaluated_triangle_count": 500000,
                    "material_slot_count": 4, "texture_largest_file_bytes": 16777216},
        "evidence": ["synthetic fixture only"],
        "notes": "synthetic fixture only"
    }
    result = validate_profile(fixture)
    assert result["status"] == "PROFILE_SCHEMA_VALID", result
    fixture["metrics"]["optimized_frame_time_ms"] = -1
    result = validate_profile(fixture)
    assert result["status"] == "BLOCKED_INVALID_PROFILE", result
    print("Stage 52 performance profile validator self-test: PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", help="Path to measured performance_profile.json")
    parser.add_argument("--output", default="build/stage52_performance_profile_validation.json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.profile:
        parser.error("--profile is required unless --self-test is used")
    profile_path = Path(args.profile).expanduser()
    try:
        data = json.loads(profile_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"stage": 52, "status": "BLOCKED_INVALID_PROFILE", "production_ready": False,
                          "issues": [str(exc)], "warnings": []}, indent=2))
        return 1
    report = validate_profile(data)
    output = json.dumps(report, indent=2)
    print(output)
    out = Path(args.output).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(output + "\n", encoding="utf-8")
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
