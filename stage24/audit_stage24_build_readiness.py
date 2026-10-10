"""Stage 24: repository build-readiness audit for the police HQ project.

Run with standard Python from the repository root:
  python stage24/audit_stage24_build_readiness.py --root . --json-out build-readiness.json
This audits expected project files and simple repository structure only. It does not
open Blender scenes or prove that any GTA/FiveM assets work in game.
"""
import argparse
import json
from pathlib import Path

REQUIRED_FILES = {
    "Stage 2 blockout generator": "stage2/generate_stage2_blockout.py",
    "Stage 3 interior generator": "stage3/generate_stage3_interior.py",
    "Stage 4 furnishing generator": "stage4/generate_stage4_furnishing.py",
    "Stage 5 scene audit": "stage5/audit_stage5_scene.py",
    "Stage 6 layout validator": "stage6/validate_stage6_layout.py",
    "Stage 7 branding generator": "stage7/generate_stage7_branding.py",
    "Stage 8 wayfinding generator": "stage8/generate_stage8_wayfinding.py",
    "Stage 9 emblem generator": "stage9/generate_stage9_emblems.py",
    "Stage 10 exterior detail generator": "stage10/generate_stage10_architectural_details.py",
    "Stage 11 interior detail generator": "stage11/generate_stage11_interior_details.py",
    "Stage 12 doors/access generator": "stage12/generate_stage12_doors_access.py",
    "Stage 13 garage circulation generator": "stage13/generate_stage13_garage_circulation.py",
    "Stage 14 exterior access generator": "stage14/generate_stage14_exterior_access.py",
    "Stage 15 site security generator": "stage15/generate_stage15_site_security.py",
    "Stage 16 structural audit": "stage16/audit_stage16_structure.py",
    "Stage 17 room/circulation audit": "stage17/audit_stage17_room_circulation.py",
    "Stage 18 material generator": "stage18/generate_stage18_materials.py",
    "Stage 19 export preflight audit": "stage19/audit_stage19_export_preflight.py",
    "Stage 20 LOD/performance audit": "stage20/audit_stage20_lod_performance.py",
    "Stage 21 geometry cleanup audit": "stage21/audit_stage21_geometry_cleanup.py",
    "Stage 22 visibility/streaming audit": "stage22/audit_stage22_visibility_streaming.py",
    "Stage 23 resource validator": "stage23/validate_stage23_resource.py",
    "Stage 23 manifest template": "stage23/fxmanifest.lua.template",
    "Stage 26 vertical-circulation reconciliation": "stage26/reconcile_stage26_vertical_circulation.py",
    "Stage 27 room circulation audit": "stage27/audit_stage27_room_circulation.py",
    "Packaging workflow": ".github/workflows/stage2-package.yml",
}
REQUIRED_DOCS = {
    "Stage 2 scope": "stage2/STAGE2_SCOPE.md",
    "Stage 3 room/door schedule": "stage3/ROOM_LAYOUT_AND_DOOR_SCHEDULE.md",
    "Stage 4 furniture/equipment plan": "stage4/FURNITURE_AND_EQUIPMENT_PLAN.md",
    "Stage 19 collision/export checklist": "stage19/COLLISION_AND_EXPORT_PREFLIGHT_CHECKLIST.md",
    "Stage 20 LOD/performance checklist": "stage20/LOD_AND_PERFORMANCE_CHECKLIST.md",
    "Stage 21 geometry cleanup checklist": "stage21/GEOMETRY_CLEANUP_AND_EXPORT_CHECKLIST.md",
    "Stage 22 visibility/streaming checklist": "stage22/VISIBILITY_STREAMING_AND_MLO_CHECKLIST.md",
    "Stage 23 resource packaging checklist": "stage23/RESOURCE_PACKAGING_AND_INSTALL_CHECKLIST.md",
    "Stage 26 circulation acceptance checklist": "stage26/VERTICAL_CIRCULATION_ACCEPTANCE_CHECKLIST.md",
    "Stage 27 circulation acceptance checklist": "stage27/ROOM_CIRCULATION_ACCEPTANCE_CHECKLIST.md",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root directory")
    parser.add_argument("--json-out", help="Optional output JSON report path")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    missing_files = [{"label": label, "path": path} for label, path in REQUIRED_FILES.items() if not (root / path).is_file()]
    missing_docs = [{"label": label, "path": path} for label, path in REQUIRED_DOCS.items() if not (root / path).is_file()]
    stage_dirs = [f"stage{i}" for i in range(2, 28)]
    present_stages = [name for name in stage_dirs if (root / name).is_dir()]
    absent_stages = [name for name in stage_dirs if not (root / name).is_dir()]
    workflow_text = ""
    workflow_path = root / ".github/workflows/stage2-package.yml"
    if workflow_path.is_file():
        workflow_text = workflow_path.read_text(encoding="utf-8", errors="replace")
    workflow_checks = {
        "mentions_stage23": "stage23/" in workflow_text,
        "includes_stage23_in_zip": "stage23\n" in workflow_text or "stage23" in workflow_text.split("- name: Create ZIP", 1)[-1],
        "artifact_upload_step_present": "actions/upload-artifact@v4" in workflow_text,
    }
    production_gates = [
        {"gate": "Blender scene generated and visually inspected", "status": "NOT_VERIFIED_BY_REPOSITORY_AUDIT"},
        {"gate": "Room dimensions, Stage 26 slab openings, stairs, elevator, doors, and access reviewed", "status": "MANUAL_REVIEW_REQUIRED"},
        {"gate": "Temporary guide/proxy geometry separated from production assets", "status": "MANUAL_REVIEW_REQUIRED"},
        {"gate": "Sollumz export metadata, archetypes, portals, occlusion, collision, and LODs verified", "status": "EXTERNAL_TOOL_VALIDATION_REQUIRED"},
        {"gate": "CodeWalker inspection completed", "status": "EXTERNAL_TOOL_VALIDATION_REQUIRED"},
        {"gate": "Actual exported resource tested in FiveM with clean join/reconnect and multiple clients", "status": "IN_GAME_TEST_REQUIRED"},
    ]
    report = {
        "stage": 24,
        "repository_root": str(root),
        "present_stage_directories": present_stages,
        "absent_stage_directories": absent_stages,
        "missing_required_files": missing_files,
        "missing_required_docs": missing_docs,
        "workflow_checks": workflow_checks,
        "repository_structure_ready": not missing_files and not missing_docs and not absent_stages and all(workflow_checks.values()),
        "production_readiness": "NOT_ESTABLISHED_BY_THIS_AUDIT",
        "production_gates": production_gates,
        "limitations": [
            "Checks repository file presence and basic workflow text only; does not run Blender or parse the workflow as GitHub Actions would.",
            "Does not inspect generated scene geometry or actual exported asset files.",
            "Does not establish that the MLO is complete, optimized, installable, or functional in FiveM.",
        ],
    }
    output = json.dumps(report, indent=2)
    print(output)
    if args.json_out:
        Path(args.json_out).expanduser().write_text(output + "\n", encoding="utf-8")
    if not report["repository_structure_ready"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
