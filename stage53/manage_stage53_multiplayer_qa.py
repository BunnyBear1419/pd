#!/usr/bin/env python3
"""Stage 53: create and validate a FiveM police HQ multiplayer QA matrix.

This tool creates a test record template; it does not execute GTA/FiveM tests.
Usage:
  python stage53/manage_stage53_multiplayer_qa.py --init --output build/fivem_multiplayer_test.json
  python stage53/manage_stage53_multiplayer_qa.py --validate build/fivem_multiplayer_test.json
  python stage53/manage_stage53_multiplayer_qa.py --self-test
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

TESTS = [
    ("fresh_join_exterior", "Fresh join", "Exterior loads, no missing textures or default building overlap"),
    ("fresh_join_interior", "Fresh join interior", "MLO interior visible and accessible on first spawn"),
    ("reconnect", "Reconnect", "Leave and rejoin; interior and collision remain correct"),
    ("respawn", "Respawn", "Respawn at expected location; no streaming or visibility regression"),
    ("resource_restart", "Resource restart", "Restart map resource; no persistent overlap or missing assets"),
    ("floor_1_routes", "Floor 1 route", "Walk reception, booking, cells and public corridor routes"),
    ("floor_2_routes", "Floor 2 route", "Walk offices, interview, evidence/armory and staff routes"),
    ("floor_3_routes", "Floor 3 route", "Walk dispatch, SWAT, lockers/showers and stair/elevator routes"),
    ("garage_vehicle", "Garage vehicle test", "Drive representative vehicles through doors, bays and turning paths"),
    ("roof_helipad", "Roof and helipad", "Reach roof safely; check helipad clearance and edge collision"),
    ("doors_access", "Doors and access", "Test each door, locked boundary and access transition"),
    ("collision_walk", "Collision walk-through", "No falling through floors, invisible blockers or snagging on openings"),
    ("interior_exterior_visibility", "Visibility transitions", "Interior/exterior transitions work from multiple angles"),
    ("texture_materials", "Textures and materials", "No missing textures, flashing materials or unexpected shader fallback"),
    ("two_client_sync", "Two-client sync", "Two clients independently enter, exit and traverse the same areas"),
    ("multiple_client_streaming", "Multi-client streaming", "Test target server player count; compare each client after joining"),
    ("long_session", "Long-session check", "Remain in and around the station for at least 20 minutes"),
]

ALLOWED = {"not_run", "pass", "fail", "blocked", "not_applicable"}


def make_template() -> dict:
    return {
        "schema_version": 1,
        "status": "NOT_RUN",
        "production_ready": False,
        "capture": {
            "tested_utc": "",
            "server_artifact": "",
            "game_build": "",
            "resource_version_or_commit": "",
            "testers": [],
            "client_count": 0,
            "duration_minutes": 0,
            "test_location": "Police HQ MLO"
        },
        "tests": [
            {"id": tid, "name": name, "expected": expected, "result": "not_run",
             "evidence": [], "notes": "", "defect_id": ""}
            for tid, name, expected in TESTS
        ],
        "defects": [],
        "limitations": [
            "This is a record template, not an automated in-game test.",
            "Use screenshots/video, client F8/server console logs, and repeatable steps as evidence.",
            "A passing result is only as reliable as the recorded real test and evidence.",
            "production_ready must remain false until export, CodeWalker, performance and multiplayer reviews are accepted."
        ]
    }


def validate(report: object) -> dict:
    issues: list[str] = []
    warnings: list[str] = []
    if not isinstance(report, dict):
        return {"stage": 53, "status": "BLOCKED_INVALID_REPORT", "production_ready": False,
                "issues": ["Report root must be a JSON object."], "warnings": []}
    if report.get("schema_version") != 1:
        issues.append("schema_version must be 1.")
    capture = report.get("capture")
    if not isinstance(capture, dict):
        issues.append("Missing capture metadata.")
        capture = {}
    for key in ("tested_utc", "server_artifact", "game_build", "resource_version_or_commit"):
        if not isinstance(capture.get(key), str) or not capture.get(key, "").strip():
            warnings.append(f"capture.{key} has not been recorded.")
    if not isinstance(capture.get("testers"), list) or not capture.get("testers"):
        warnings.append("Record at least one tester.")
    if not isinstance(capture.get("client_count"), int) or capture.get("client_count", 0) < 1:
        warnings.append("Record a client count of at least 1.")
    tests = report.get("tests")
    if not isinstance(tests, list):
        issues.append("tests must be a list.")
        tests = []
    seen: set[str] = set()
    passed = failed = blocked = not_run = 0
    expected_ids = {item[0] for item in TESTS}
    for item in tests:
        if not isinstance(item, dict):
            issues.append("Each test entry must be an object.")
            continue
        tid = item.get("id")
        if not isinstance(tid, str) or not tid:
            issues.append("A test entry is missing its id.")
            continue
        if tid in seen:
            issues.append(f"Duplicate test id: {tid}")
        seen.add(tid)
        result = item.get("result")
        if result not in ALLOWED:
            issues.append(f"{tid}: invalid result {result!r}.")
            continue
        if result == "pass":
            passed += 1
            if not isinstance(item.get("evidence"), list) or not item.get("evidence"):
                warnings.append(f"{tid}: marked pass without evidence references.")
        elif result == "fail":
            failed += 1
            if not str(item.get("notes", "")).strip() and not str(item.get("defect_id", "")).strip():
                warnings.append(f"{tid}: failure needs notes or a defect_id.")
        elif result == "blocked":
            blocked += 1
        elif result == "not_run":
            not_run += 1
    missing = sorted(expected_ids - seen)
    extra = sorted(seen - expected_ids)
    if missing:
        warnings.append("Missing required test cases: " + ", ".join(missing))
    if extra:
        warnings.append("Unrecognized test case ids: " + ", ".join(extra))
    if failed:
        warnings.append(f"{failed} test(s) failed; resolve and retest before acceptance.")
    if blocked:
        warnings.append(f"{blocked} test(s) blocked; explain the blocker and retest.")
    if not_run:
        warnings.append(f"{not_run} test(s) have not been run.")
    if not tests:
        warnings.append("No test results recorded.")
    defects = report.get("defects", [])
    if not isinstance(defects, list):
        issues.append("defects must be a list.")
    status = "BLOCKED_INVALID_REPORT" if issues else ("REVIEW_REQUIRED" if warnings else "MATRIX_COMPLETE_REQUIRES_HUMAN_SIGNOFF")
    return {
        "stage": 53,
        "status": status,
        "production_ready": False,
        "summary": {"test_cases": len(tests), "passed": passed, "failed": failed, "blocked": blocked, "not_run": not_run},
        "issues": issues,
        "warnings": warnings,
        "manual_signoff_required": True,
        "limitations": [
            "The tool does not launch FiveM, drive a client, inspect screenshots, or verify log evidence.",
            "Do not mark a test pass unless it was actually performed against the target build.",
            "Fresh join, reconnect, resource restart and multi-client streaming are mandatory real-world checks."
        ]
    }


def self_test() -> None:
    template = make_template()
    result = validate(template)
    assert result["status"] == "REVIEW_REQUIRED", result
    template["schema_version"] = 999
    result = validate(template)
    assert result["status"] == "BLOCKED_INVALID_REPORT", result
    print("Stage 53 multiplayer QA matrix self-test: PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--init", action="store_true", help="Write an empty QA template")
    group.add_argument("--validate", metavar="REPORT", help="Validate a filled QA report")
    group.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", default="build/fivem_multiplayer_test.json")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.init:
        output = Path(args.output).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(make_template(), indent=2) + "\n", encoding="utf-8")
        print(f"Wrote uncompleted QA template: {output}")
        print("No in-game tests were run; production_ready remains false.")
        return 0
    path = Path(args.validate).expanduser()
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"stage": 53, "status": "BLOCKED_INVALID_REPORT", "production_ready": False,
                          "issues": [str(exc)], "warnings": []}, indent=2))
        return 1
    result = validate(report)
    output = json.dumps(result, indent=2)
    print(output)
    out = Path(args.output).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(output + "\n", encoding="utf-8")
    return 1 if result["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
