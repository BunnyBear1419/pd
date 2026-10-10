#!/usr/bin/env python3
"""Stage 54 release-candidate gate for a FiveM MLO; never fabricates assets."""
from __future__ import annotations
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_FILES = {
    "final_blender_scene": ("build/pdhq_final.blend", "Reviewed final Blender scene"),
    "export_manifest": ("build/export_manifest.json", "Asset hashes and export metadata"),
    "codewalker_review": ("build/codewalker_review.json", "Human-reviewed CodeWalker evidence"),
    "performance_profile": ("build/performance_profile.json", "Measured performance profile"),
    "multiplayer_test": ("build/fivem_multiplayer_test.json", "Completed multiplayer QA matrix"),
    "release_notes": ("build/release_notes.md", "Install, configuration, known issues and rollback notes"),
    "resource_manifest": ("resource/fxmanifest.lua", "FiveM resource manifest"),
}
REQUIRED_DIRS = {"stream_assets": ("resource/stream", "Exported runtime assets")}

def audit(root: Path) -> dict:
    evidence = []
    for key, (rel, purpose) in REQUIRED_FILES.items():
        p = root / rel
        present = p.is_file() and p.stat().st_size > 0
        evidence.append({"key": key, "path": rel, "purpose": purpose, "present": present})
    for key, (rel, purpose) in REQUIRED_DIRS.items():
        p = root / rel
        files = [x for x in p.rglob("*") if x.is_file()] if p.is_dir() else []
        evidence.append({"key": key, "path": rel, "purpose": purpose,
                         "present": bool(files), "file_count": len(files)})
    notes_path = root / "build/release_notes.md"
    notes = notes_path.read_text(encoding="utf-8", errors="replace") if notes_path.is_file() else ""
    rollback_terms = ("rollback", "backup")
    missing_rollback = [term for term in rollback_terms if term not in notes.lower()]
    if missing_rollback:
        evidence.append({"key": "rollback_instructions", "path": "build/release_notes.md",
                         "purpose": "Explicit backup and rollback instructions",
                         "present": False, "missing_terms": missing_rollback})
    else:
        evidence.append({"key": "rollback_instructions", "path": "build/release_notes.md",
                         "purpose": "Explicit backup and rollback instructions", "present": True})
    manifest_path = root / "resource/fxmanifest.lua"
    manifest_text = manifest_path.read_text(encoding="utf-8", errors="replace") if manifest_path.is_file() else ""
    evidence.append({"key": "resource_manifest_basics", "path": "resource/fxmanifest.lua",
                     "purpose": "Manifest has fx_version and game declarations",
                     "present": bool(re.search(r"fx_version\\s*['\"]", manifest_text)
                                     and re.search(r"game\\s*['\"]", manifest_text))})
    missing = [x["path"] for x in evidence if not x["present"]]
    return {
        "stage": 54,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "BLOCKED_MISSING_RELEASE_EVIDENCE" if missing else "EVIDENCE_PRESENT_REQUIRES_HUMAN_SIGNOFF",
        "production_ready": False,
        "evidence": evidence,
        "missing_or_incomplete": missing,
        "release_safeguards": [
            "Do not overwrite a live resource before backing up its entire current folder and server configuration.",
            "Install the candidate under a staging resource name and test it before switching production.",
            "Preserve the previous known-good resource and document the exact rollback command.",
            "Only include actual exported runtime assets in resource/stream; keep build reports and Blender review helpers out of the runtime resource.",
            "Validate asset paths, file hashes, YTYP registration, collisions, portals and map suppression in the real toolchain.",
            "Compare measured performance and complete multiplayer QA before release."
        ],
        "limitations": [
            "This script checks file presence and a few textual markers; it does not prove the files are valid.",
            "It does not export Blender scenes, create GTA assets, launch FiveM, or produce a release ZIP.",
            "production_ready is deliberately false and requires human review."
        ]
    }

def self_test() -> None:
    with __import__("tempfile").TemporaryDirectory() as td:
        root = Path(td)
        result = audit(root)
        assert result["status"] == "BLOCKED_MISSING_RELEASE_EVIDENCE"
        assert result["production_ready"] is False
    print("Stage 54 release-candidate gate self-test: PASS")

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", default=".", help="Project root")
    p.add_argument("--output", default="build/stage54_release_candidate_report.json")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0
    root = Path(args.root).expanduser().resolve()
    result = audit(root)
    out = Path(args.output).expanduser()
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "production_ready": False,
                      "missing_or_incomplete": result["missing_or_incomplete"],
                      "report": str(out)}, indent=2))
    return 0 if result["status"] != "BLOCKED_MISSING_RELEASE_EVIDENCE" else 1

if __name__ == "__main__":
    raise SystemExit(main())
