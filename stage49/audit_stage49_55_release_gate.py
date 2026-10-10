#!/usr/bin/env python3
"""Stage 49–55: audit external production evidence without pretending to create it."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = [
    ("blender_scene", "build/pdhq_final.blend", "Reviewed final Blender scene"),
    ("export_manifest", "build/export_manifest.json", "Asset counts, export versions and hashes"),
    ("resource_manifest", "resource/fxmanifest.lua", "Actual FiveM resource manifest"),
    ("stream_directory", "resource/stream", "Exported GTA stream assets"),
    ("codewalker_review", "build/codewalker_review.json", "CodeWalker export and visibility review record"),
    ("performance_profile", "build/performance_profile.json", "Measured performance and geometry/texture budgets"),
    ("multiplayer_qa", "build/fivem_multiplayer_test.json", "In-game multiplayer, spawn, reconnect and streaming QA"),
    ("release_notes", "build/release_notes.md", "Install, configuration, known limitations and rollback instructions"),
]

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", default=".")
    p.add_argument("--output", default="build/stage49_55_release_gate.json")
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()
    evidence = []
    for key, rel, meaning in REQUIRED:
        path = root / rel
        exists = path.is_file() if key != "stream_directory" else path.is_dir()
        evidence.append({"key": key, "path": rel, "purpose": meaning, "present": exists})
    missing = [e for e in evidence if not e["present"]]
    report = {
        "stage_range": "49-55",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "BLOCKED_MISSING_EXTERNAL_EVIDENCE" if missing else "EVIDENCE_PRESENT_REQUIRES_HUMAN_REVIEW",
        "production_ready": False,
        "required_evidence": evidence,
        "missing_evidence": [e["path"] for e in missing],
        "acceptance_gates": [
            "Confirm Blender scene opens cleanly in the chosen supported Blender/Sollumz versions.",
            "Inspect actual exported assets and MLO archetype/portal/occlusion/collision in CodeWalker.",
            "Validate manifest and streamed files against the target FiveM artifact/runtime.",
            "Test interior/exterior visibility, collisions, stairs/elevator, door access, vehicle garage and roof transitions.",
            "Run multi-client join, respawn, reconnect, resource restart and long-session tests.",
            "Measure and record performance on representative hardware and network conditions.",
            "Package installation and rollback instructions only after evidence is reviewed."
        ],
        "limitations": ["File presence is not proof that the evidence is correct.",
                        "This audit cannot run Blender, Sollumz, CodeWalker, or a FiveM server in CI.",
                        "production_ready remains false until a human reviews the evidence and the actual in-game result."]
    }
    out = Path(args.output)
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "output": str(out), "missing_evidence": len(missing),
                      "production_ready": False}, indent=2))

if __name__ == "__main__":
    main()
