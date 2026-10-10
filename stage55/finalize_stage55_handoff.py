#!/usr/bin/env python3
"""Stage 55 final acceptance handoff report for the custom FiveM police HQ MLO.

Aggregates evidence files and reports blockers. It never marks the MLO production-ready.
"""
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

EVIDENCE = [
    ("final_blender_scene", "build/pdhq_final.blend", "Final editable Blender scene"),
    ("export_manifest", "build/export_manifest.json", "Hashed inventory of exported stream assets"),
    ("five_m_resource_manifest", "resource/fxmanifest.lua", "FiveM resource manifest"),
    ("stream_assets", "resource/stream", "Actual exported GTA assets"),
    ("codewalker_review", "build/codewalker_review.json", "Human-reviewed CodeWalker report"),
    ("performance_profile", "build/performance_profile.json", "Measured runtime performance"),
    ("multiplayer_qa", "build/fivem_multiplayer_test.json", "Completed real FiveM QA matrix"),
    ("release_notes", "build/release_notes.md", "Install, configuration, limitations and rollback notes"),
    ("stage48_pre_export", "build/stage48_pre_export_report.json", "Integrated pre-export review"),
    ("stage49_export_validation", "build/stage49_export_manifest_validation.json", "Export manifest hash/path validation"),
    ("stage50_collision_visibility", "build/stage50_collision_visibility.json", "Blender collision/visibility audit"),
    ("stage52_performance_validation", "build/stage52_performance_profile_validation.json", "Measured performance profile validation"),
    ("stage54_release_candidate", "build/stage54_release_candidate_report.json", "Release candidate gate report"),
]

def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

def build_report(root: Path) -> dict:
    items = []
    for key, rel, purpose in EVIDENCE:
        p = root / rel
        if key == "stream_assets":
            files = [x for x in p.rglob("*") if x.is_file()] if p.is_dir() else []
            present = bool(files)
            detail = {"file_count": len(files)}
        else:
            present = p.is_file() and p.stat().st_size > 0
            detail = {}
        entry = {"key": key, "path": rel, "purpose": purpose, "present": present, **detail}
        if present and p.suffix.lower() == ".json":
            doc = read_json(p)
            if doc is None:
                entry["valid_json"] = False
            else:
                entry["valid_json"] = True
                if "production_ready" in doc:
                    entry["source_production_ready"] = bool(doc.get("production_ready"))
                if "status" in doc:
                    entry["source_status"] = doc.get("status")
        items.append(entry)
    missing = [x["path"] for x in items if not x["present"]]
    malformed = [x["path"] for x in items if x.get("valid_json") is False]
    caution = [
        "Presence of evidence files does not establish that the evidence is accurate or acceptable.",
        "Review each source report and close every critical/high-severity defect before release.",
        "Inspect the real export in CodeWalker, including MLO archetype, portals, occlusion, collisions and map suppression.",
        "Test fresh join, reconnect, respawn, resource restart, interior/exterior transitions and multiple clients in FiveM.",
        "Record measured baseline and optimized performance on representative hardware.",
        "Back up the live resource and configuration; stage the candidate first and preserve a tested rollback copy."
    ]
    status = "BLOCKED_MISSING_EVIDENCE" if missing else ("BLOCKED_INVALID_EVIDENCE" if malformed else "EVIDENCE_PRESENT_REQUIRES_HUMAN_SIGNOFF")
    return {
        "stage": 55,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "production_ready": False,
        "summary": {"required_evidence_items": len(items),
                    "present": sum(1 for x in items if x["present"]),
                    "missing": len(missing), "invalid_json": len(malformed)},
        "evidence": items,
        "missing_evidence": missing,
        "invalid_evidence": malformed,
        "final_handoff_checklist": [
            "Final Blender scene opens without missing linked assets.",
            "All schematic/proxy placeholders are removed or explicitly accepted.",
            "Exported resource inventory and SHA-256 manifest validate.",
            "CodeWalker review is signed off with no unresolved critical defects.",
            "Collision, door access, floor transitions, garage clearance and roof access pass.",
            "Performance measurements are within the agreed budgets.",
            "Multiplayer QA matrix is complete with evidence and defects resolved/retested.",
            "Installation and rollback instructions match the exact release package.",
            "Reviewer, date, tool versions, release version and known limitations are recorded."
        ],
        "next_actions": (["Collect missing external evidence: " + ", ".join(missing)] if missing else []) +
                       (["Repair malformed JSON evidence: " + ", ".join(malformed)] if malformed else []) +
                       ["Have a human reviewer inspect the actual assets and evidence, then repeat the in-game tests."],
        "limitations": caution
    }

def self_test():
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as tmp:
        result = build_report(Path(tmp))
        assert result["status"] == "BLOCKED_MISSING_EVIDENCE"
        assert result["production_ready"] is False
        assert result["summary"]["missing"] == len(EVIDENCE)
    print("Stage 55 final handoff self-test: PASS")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", default=".", help="Project root")
    p.add_argument("--output", default="build/stage55_final_handoff.json")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0
    root = Path(args.root).expanduser().resolve()
    result = build_report(root)
    output = Path(args.output).expanduser()
    if not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "production_ready": False,
                      "summary": result["summary"], "report": str(output)}, indent=2))
    return 0 if result["status"] == "EVIDENCE_PRESENT_REQUIRES_HUMAN_SIGNOFF" else 1

if __name__ == "__main__":
    raise SystemExit(main())
