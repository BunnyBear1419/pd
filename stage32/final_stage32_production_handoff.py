#!/usr/bin/env python3
"""Stage 32: repository and production-handoff audit.

This is a filesystem/readiness inventory, not a Blender, Sollumz, CodeWalker,
or FiveM validator. Missing external-build outputs are reported as blockers
without making the audit itself fail.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

STAGE_FILES = {
    2: ["stage2/generate_stage2_blockout.py", "stage2/README.md"],
    3: ["stage3/generate_stage3_interior.py", "stage3/README.md"],
    4: ["stage4/generate_stage4_furnishing.py", "stage4/README.md"],
    5: ["stage5/audit_stage5_scene.py", "stage5/README.md"],
    6: ["stage6/validate_stage6_layout.py", "stage6/README.md"],
    7: ["stage7/generate_stage7_branding.py", "stage7/README.md"],
    8: ["stage8/generate_stage8_wayfinding.py", "stage8/README.md"],
    9: ["stage9/generate_stage9_emblems.py", "stage9/README.md"],
    10: ["stage10/generate_stage10_architectural_details.py", "stage10/README.md"],
    11: ["stage11/generate_stage11_interior_details.py", "stage11/README.md"],
    12: ["stage12/generate_stage12_doors_access.py", "stage12/README.md"],
    13: ["stage13/generate_stage13_garage_circulation.py", "stage13/README.md"],
    14: ["stage14/generate_stage14_exterior_access.py", "stage14/README.md"],
    15: ["stage15/generate_stage15_site_security.py", "stage15/README.md"],
    16: ["stage16/audit_stage16_structure.py", "stage16/README.md"],
    17: ["stage17/audit_stage17_room_circulation.py", "stage17/README.md"],
    18: ["stage18/generate_stage18_materials.py", "stage18/README.md"],
    19: ["stage19/audit_stage19_export_preflight.py", "stage19/README.md"],
    20: ["stage20/audit_stage20_lod_performance.py", "stage20/README.md"],
    21: ["stage21/audit_stage21_geometry_cleanup.py", "stage21/README.md"],
    22: ["stage22/audit_stage22_visibility_streaming.py", "stage22/README.md"],
    23: ["stage23/validate_stage23_resource.py", "stage23/fxmanifest.lua.template", "stage23/README.md"],
    24: ["stage24/audit_stage24_build_readiness.py", "stage24/README.md"],
    25: ["stage25/build_stage25_scene.py", "stage25/README.md"],
    26: ["stage26/reconcile_stage26_vertical_circulation.py", "stage26/README.md"],
    27: ["stage27/audit_stage27_room_circulation.py", "stage27/README.md"],
    28: ["stage28/audit_stage28_garage_secure_layout.py", "stage28/README.md"],
    29: ["stage29/audit_stage29_room_clearances.py", "stage29/README.md"],
    30: ["stage30/audit_stage30_exterior_helipad_clearance.py", "stage30/README.md"],
    31: ["stage31/audit_stage31_optimization_export_manifest.py", "stage31/README.md"],
    34: ["stage34/audit_stage34_architecture_geometry.py", "stage34/README.md", "stage34/ARCHITECTURE_GEOMETRY_ACCEPTANCE_CHECKLIST.md"],
    35: ["stage35/audit_stage35_floor_coordination.py", "stage35/README.md", "stage35/FLOOR_COORDINATION_ACCEPTANCE_CHECKLIST.md"],
    36: ["stage36/room_program_and_adjacency.json", "stage36/audit_stage36_room_program.py", "stage36/README.md", "stage36/ROOM_PROGRAM_ACCEPTANCE_CHECKLIST.md"],
    37: ["stage37/audit_stage37_floor_fit.py", "stage37/README.md", "stage37/FLOOR_FIT_ACCEPTANCE_CHECKLIST.md"],
}
REQUIRED_PROJECT_FILES = [
    ".github/workflows/stage2-package.yml",
    "stage24/BUILD_READINESS_AND_REMAINING_WORK.md",
    "stage25/BLENDER_BUILD_AND_ACCEPTANCE_CHECKLIST.md",
    "stage31/OPTIMIZATION_AND_EXPORT_MANIFEST_CHECKLIST.md",
    "stage32/README.md",
    "stage32/FINAL_PRODUCTION_HANDOFF_ACCEPTANCE_CHECKLIST.md",
    "stage34/ARCHITECTURE_GEOMETRY_ACCEPTANCE_CHECKLIST.md",
    "stage35/FLOOR_COORDINATION_ACCEPTANCE_CHECKLIST.md",
    "stage36/room_program_and_adjacency.json",
    "stage36/ROOM_PROGRAM_ACCEPTANCE_CHECKLIST.md",
    "stage37/FLOOR_FIT_ACCEPTANCE_CHECKLIST.md",
]

def inspect_path(root, relative):
    path = root / relative
    return {"path": relative, "exists": path.exists(), "kind": "directory" if path.is_dir() else "file"}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root (default: current directory)")
    parser.add_argument("--output", default="build/stage32_production_handoff.json", help="Report path, absolute or relative to root")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error("repository root is not a directory: " + str(root))

    stage_results = {}
    missing_source = []
    for stage, files in STAGE_FILES.items():
        entries = [inspect_path(root, item) for item in files]
        missing = [entry["path"] for entry in entries if not entry["exists"]]
        missing_source.extend(missing)
        stage_results[str(stage)] = {"status": "PRESENT" if not missing else "MISSING_FILES", "files": entries, "missing": missing}

    project_files = [inspect_path(root, item) for item in REQUIRED_PROJECT_FILES]
    missing_project = [item["path"] for item in project_files if not item["exists"]]
    expected_outputs = [
        "build/pdhq_stage35_blockout.blend",
        "build/pdhq_stage35_build_report.json",
        "resource/fxmanifest.lua",
        "resource/stream",
    ]
    output_inventory = [inspect_path(root, item) for item in expected_outputs]
    missing_outputs = [item["path"] for item in output_inventory if not item["exists"]]
    scene_exists = (root / "build/pdhq_stage35_blockout.blend").is_file()
    resource_exists = (root / "resource/fxmanifest.lua").is_file() and (root / "resource/stream").is_dir()

    if missing_source or missing_project:
        status = "BLOCKED_MISSING_PROJECT_FILES"
    elif not scene_exists:
        status = "BLOCKED_SCENE_NOT_BUILT"
    elif not resource_exists:
        status = "BLOCKED_GTA_RESOURCE_NOT_EXPORTED"
    else:
        status = "EXTERNAL_VALIDATION_REQUIRED"

    report = {
        "stage": 37,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "repository_root": str(root),
        "status": status,
        "production_ready": False,
        "summary": "This audit inventories files only. It does not certify geometry, GTA asset validity, MLO visibility, or in-game behavior.",
        "stage_inventory": stage_results,
        "required_project_files": project_files,
        "external_build_outputs": output_inventory,
        "missing_source_files": sorted(set(missing_source)),
        "missing_project_files": missing_project,
        "missing_expected_outputs": missing_outputs,
        "required_manual_gates": [
            "Generate and inspect a versioned Blender scene; review Stage 24-31 audit findings.",
            "Resolve geometry, room/door/furniture clearance, topology, transforms, UVs, materials, and guide/proxy cleanup.",
            "Use a compatible Sollumz workflow to author real GTA archetypes, collision, portals/occlusion, and LODs as appropriate.",
            "Export actual assets and inspect them in CodeWalker; verify the real fxmanifest.lua and stream paths.",
            "Run Stage 23 resource validation against the exported resource folder.",
            "Test on a FiveM development server with multiple clients, reconnect/restart/spawn scenarios, streaming, collisions, visibility, and measured performance.",
        ],
        "limitations": [
            "Presence of source files or a successful CI package is not proof that Blender executed.",
            "A .blend file alone is not a FiveM-ready MLO.",
            "A resource folder may exist and still be invalid; manual toolchain and in-game acceptance remains mandatory.",
        ],
    }
    output = Path(args.output).expanduser()
    if not output.is_absolute():
        output = root / output
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "report": str(output), "missing_source_files": len(report["missing_source_files"]), "missing_project_files": len(missing_project), "missing_expected_outputs": len(missing_outputs), "production_ready": False}, indent=2))

if __name__ == "__main__":
    main()
