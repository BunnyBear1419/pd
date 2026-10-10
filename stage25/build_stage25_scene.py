"""Stage 25: repeatable Blender scene build and audit orchestration.

Run from the repository root:
  blender -b --python stage25/build_stage25_scene.py -- --output build/pdhq_stage29_blockout.blend

This generates a schematic Blender blockout and runs non-destructive audits.
It is not a GTA/Sollumz exporter and does not certify a production MLO.
"""
import argparse
import json
import runpy
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATION_STEPS = [
    ("Stage 2 blockout", "stage2/generate_stage2_blockout.py"),
    ("Stage 26 vertical-circulation reconciliation", "stage26/reconcile_stage26_vertical_circulation.py"),
    ("Stage 3 interior partitions", "stage3/generate_stage3_interior.py"),
    ("Stage 4 furniture proxies", "stage4/generate_stage4_furnishing.py"),
    ("Stage 7 branding", "stage7/generate_stage7_branding.py"),
    ("Stage 8 wayfinding", "stage8/generate_stage8_wayfinding.py"),
    ("Stage 9 emblems", "stage9/generate_stage9_emblems.py"),
    ("Stage 10 exterior details", "stage10/generate_stage10_architectural_details.py"),
    ("Stage 11 interior details", "stage11/generate_stage11_interior_details.py"),
    ("Stage 12 door/access proxies", "stage12/generate_stage12_doors_access.py"),
    ("Stage 13 garage circulation guides", "stage13/generate_stage13_garage_circulation.py"),
    ("Stage 14 exterior access guides", "stage14/generate_stage14_exterior_access.py"),
    ("Stage 15 site/security guides", "stage15/generate_stage15_site_security.py"),
]
AUDIT_STEPS_BEFORE_MATERIALS = [
    ("Stage 5 scene audit", "stage5/audit_stage5_scene.py"),
    ("Stage 6 layout validation", "stage6/validate_stage6_layout.py"),
    ("Stage 16 structural/circulation audit", "stage16/audit_stage16_structure.py"),
    ("Stage 17 room/circulation audit", "stage17/audit_stage17_room_circulation.py"),
    ("Stage 27 room layout/circulation review", "stage27/audit_stage27_room_circulation.py"),
    ("Stage 28 garage/secure ground-floor review", "stage28/audit_stage28_garage_secure_layout.py"),
    ("Stage 29 room/door/furniture clearance review", "stage29/audit_stage29_room_clearances.py"),
]
AUDIT_STEPS_AFTER_MATERIALS = [
    ("Stage 19 export preflight", "stage19/audit_stage19_export_preflight.py"),
    ("Stage 20 LOD/performance review", "stage20/audit_stage20_lod_performance.py"),
    ("Stage 21 geometry cleanup review", "stage21/audit_stage21_geometry_cleanup.py"),
    ("Stage 22 visibility/streaming review", "stage22/audit_stage22_visibility_streaming.py"),
]


def parse_args():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="build/pdhq_stage29_blockout.blend", help="Output .blend path")
    parser.add_argument("--log", default="build/pdhq_stage29_build_report.json", help="Build report JSON path")
    parser.add_argument("--skip-audits", action="store_true", help="Skip audit scripts; generators still run")
    return parser.parse_args(argv)


def write_report(path, report):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def main():
    import bpy

    args = parse_args()
    output = Path(args.output).expanduser()
    if not output.is_absolute():
        output = (Path.cwd() / output).resolve()
    log_path = Path(args.log).expanduser()
    if not log_path.is_absolute():
        log_path = (Path.cwd() / log_path).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    plan = list(GENERATION_STEPS)
    if not args.skip_audits:
        plan.extend(AUDIT_STEPS_BEFORE_MATERIALS)
    plan.append(("Stage 18 reusable materials", "stage18/generate_stage18_materials.py"))
    if not args.skip_audits:
        plan.extend(AUDIT_STEPS_AFTER_MATERIALS)

    report = {
        "stage": 29,
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "repository_root": str(ROOT),
        "output_blend": str(output),
        "mode": "generation_only" if args.skip_audits else "generation_plus_non_destructive_audits",
        "steps": [],
        "status": "RUNNING",
        "production_readiness": "NOT_CERTIFIED",
        "limitations": [
            "Must be executed by Blender; repository CI only checks Python syntax and packaging.",
            "Generators produce schematic blockout/proxy geometry and planning guides, not a finished architectural model.",
            "Does not export GTA assets or create/validate Sollumz archetypes, portals, occlusion, collision, or LODs.",
            "A saved .blend file is not evidence that the MLO works in FiveM; manual Blender, CodeWalker, and in-game checks remain required.",
        ],
    }

    try:
        for label, relative in plan:
            script = ROOT / relative
            if not script.is_file():
                raise FileNotFoundError("Required build script is missing: " + str(script))
            print("\n[PDHQ Build] Running: " + label + " (" + relative + ")", flush=True)
            started = datetime.now(timezone.utc).isoformat()
            runpy.run_path(str(script), run_name="__main__")
            report["steps"].append({"label": label, "script": relative, "status": "SUCCESS", "finished_utc": datetime.now(timezone.utc).isoformat()})
            report["last_step_started_utc"] = started

        report["status"] = "BUILD_COMPLETED_REQUIRES_MANUAL_REVIEW"
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        block_name = "PDHQ_STAGE29_BUILD_REPORT"
        block = bpy.data.texts.get(block_name) or bpy.data.texts.new(block_name)
        block.clear()
        block.write(json.dumps(report, indent=2))
        bpy.ops.wm.save_as_mainfile(filepath=str(output))
        write_report(log_path, report)
        print("\n[PDHQ Build] Saved Blender project: " + str(output), flush=True)
        print("[PDHQ Stage 25] Saved build report: " + str(log_path), flush=True)
        print("[PDHQ Stage 25] Build scripts completed; inspect the scene and audit findings before export.", flush=True)
    except Exception as exc:
        report["status"] = "FAILED"
        report["error"] = str(exc)
        report["traceback"] = traceback.format_exc()
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        write_report(log_path, report)
        print("\n[PDHQ Stage 25] BUILD FAILED: " + str(exc), file=sys.stderr, flush=True)
        traceback.print_exc()
        try:
            partial = output.with_name(output.stem + ".partial.blend")
            bpy.ops.wm.save_as_mainfile(filepath=str(partial))
            print("[PDHQ Stage 25] Saved partial scene for debugging: " + str(partial), file=sys.stderr, flush=True)
        except Exception:
            pass
        raise


if __name__ == "__main__":
    main()
