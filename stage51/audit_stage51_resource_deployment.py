#!/usr/bin/env python3
"""Stage 51 FiveM resource manifest and deployment preflight.

Checks resource packaging heuristically; it is not a Lua parser or FiveM runtime.
Usage:
  python stage51/audit_stage51_resource_deployment.py path/to/resource --json-out build/stage51_deployment_report.json
  python stage51/audit_stage51_resource_deployment.py --self-test
"""
from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path, PurePosixPath

ASSET_EXTENSIONS = {".ymap", ".ytyp", ".ydr", ".ydd", ".ytd", ".ybn", ".ymf", ".yft"}
PLACEHOLDERS = ("your_map", "replace_me", "todo", "placeholder", "example_map", "changeme")
QUOTED_PATH = re.compile(r"""['"]([^'"]+\.(?:ymap|ytyp|ydr|ydd|ytd|ybn|ymf|yft))['"]""", re.I)


def inspect_resource(root: Path, server_cfg: Path | None = None) -> dict:
    issues: list[str] = []
    warnings: list[str] = []
    root = root.expanduser().resolve()
    manifest = root / "fxmanifest.lua"
    stream = root / "stream"
    if not root.is_dir():
        return {"stage": 51, "status": "BLOCKED", "production_ready": False,
                "resource": str(root), "issues": ["Resource path is not a directory."],
                "warnings": [], "asset_count": 0}
    if not manifest.is_file():
        issues.append("Missing fxmanifest.lua at the resource root.")
        manifest_text = ""
    else:
        manifest_text = manifest.read_text(encoding="utf-8", errors="replace")
    lower = manifest_text.lower()
    if "fx_version" not in lower:
        issues.append("fxmanifest.lua does not declare fx_version.")
    if not re.search(r"""\bgame\s*\(?\s*['"]gta5['"]""", manifest_text, re.I):
        warnings.append("Could not confirm an explicit game 'gta5' declaration; inspect manifest syntax.")
    if not re.search(r"""this_is_a_map\s*\(?\s*['"]yes['"]""", manifest_text, re.I):
        warnings.append("Could not confirm this_is_a_map 'yes'; confirm the map resource setup for this export.")
    if any(token in lower for token in PLACEHOLDERS):
        warnings.append("Manifest contains a possible template placeholder token.")

    if not stream.is_dir():
        issues.append("Missing stream/ directory.")
        assets: list[Path] = []
    else:
        assets = sorted(p for p in stream.rglob("*") if p.is_file() and p.suffix.lower() in ASSET_EXTENSIONS)
        if not assets:
            issues.append("stream/ contains no recognized GTA/FiveM asset files.")

    relative_assets = {p.relative_to(root).as_posix() for p in assets}
    if assets and not any(p.suffix.lower() == ".ymap" for p in assets):
        warnings.append("No .ymap file found; confirm whether map placement is included in another resource.")
    ytyps = [p for p in assets if p.suffix.lower() == ".ytyp"]
    if ytyps:
        if "dlc_ityp_request" not in lower:
            warnings.append("A .ytyp exists but no DLC_ITYP_REQUEST declaration was detected.")
        for p in ytyps:
            rel = p.relative_to(root).as_posix()
            if rel not in manifest_text and p.name not in manifest_text:
                warnings.append(f"YTYP not visibly referenced by name in fxmanifest.lua: {rel}")

    for match in QUOTED_PATH.finditer(manifest_text):
        raw = match.group(1).replace("\\", "/")
        posix = PurePosixPath(raw)
        if posix.is_absolute() or ".." in posix.parts:
            issues.append(f"Manifest asset path is absolute or traverses directories: {raw}")
            continue
        if raw.startswith("stream/") and not (root / Path(*posix.parts)).is_file():
            issues.append(f"Manifest references a missing stream asset: {raw}")
        elif raw.startswith("stream/") and (root / Path(*posix.parts)).resolve().is_relative_to(stream.resolve()) is False:
            issues.append(f"Manifest path resolves outside stream/: {raw}")

    server_cfg_report = None
    if server_cfg is not None:
        cfg = server_cfg.expanduser().resolve()
        if not cfg.is_file():
            warnings.append(f"Optional server.cfg not found: {cfg}")
            server_cfg_report = {"path": str(cfg), "found": False, "start_reference_found": False}
        else:
            cfg_text = cfg.read_text(encoding="utf-8", errors="replace")
            resource_name = root.name.lower()
            start_re = re.compile(r"^\s*(?:ensure|start)\s+['"]?" + re.escape(resource_name) + r"['"]?\s*(?:#.*)?$", re.I | re.M)
            started = bool(start_re.search(cfg_text))
            if not started:
                warnings.append(f"server.cfg does not contain ensure/start {root.name}; add it after installing the resource.")
            server_cfg_report = {"path": str(cfg), "found": True, "start_reference_found": started}

    status = "BLOCKED" if issues else ("REVIEW_REQUIRED" if warnings else "STRUCTURE_CHECKED")
    return {
        "stage": 51,
        "status": status,
        "production_ready": False,
        "resource": str(root),
        "manifest_present": manifest.is_file(),
        "stream_present": stream.is_dir(),
        "asset_count": len(assets),
        "asset_files": sorted(relative_assets),
        "issues": issues,
        "warnings": warnings,
        "server_cfg": server_cfg_report,
        "manual_acceptance_checks": [
            "Install a backup copy on a staging server and verify the resource starts without console errors.",
            "Check map placement, YTYP registration, collisions, textures, portals and overlap with default world geometry in CodeWalker/FiveM.",
            "Test fresh join, respawn, reconnect and multiple clients.",
            "Document the exact resource folder name, server.cfg start line, dependencies, rollback folder and tested tool versions."
        ],
        "limitations": [
            "This checks filesystem and text patterns, not Lua semantics or actual FiveM startup.",
            "Asset presence does not prove that GTA binary formats or MLO metadata are valid.",
            "No result from this script can mark the MLO production-ready."
        ]
    }


def self_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "pdhq"
        stream = root / "stream"
        stream.mkdir(parents=True)
        (stream / "pdhq.ymap").write_bytes(b"fixture")
        (stream / "pdhq.ytyp").write_bytes(b"fixture")
        (root / "fxmanifest.lua").write_text(
            "fx_version 'cerulean'\ngame 'gta5'\nthis_is_a_map 'yes'\n"
            "data_file 'DLC_ITYP_REQUEST' 'stream/pdhq.ytyp'\n", encoding="utf-8")
        report = inspect_resource(root)
        assert report["status"] == "STRUCTURE_CHECKED", report
        (root / "fxmanifest.lua").write_text(
            "fx_version 'cerulean'\ngame 'gta5'\nthis_is_a_map 'yes'\n"
            "data_file 'DLC_ITYP_REQUEST' 'stream/../missing.ytyp'\n", encoding="utf-8")
        report = inspect_resource(root)
        assert report["status"] == "BLOCKED" and report["issues"], report
    print("Stage 51 resource deployment audit self-test: PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("resource", nargs="?", help="Path to the exported FiveM resource folder")
    parser.add_argument("--server-cfg", help="Optional server.cfg to check for ensure/start <resource-folder-name>")
    parser.add_argument("--json-out", help="Optional JSON report path")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.resource:
        parser.error("resource path is required unless --self-test is used")
    report = inspect_resource(Path(args.resource), Path(args.server_cfg) if args.server_cfg else None)
    output = json.dumps(report, indent=2)
    print(output)
    if args.json_out:
        out = Path(args.json_out).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(output + "\n", encoding="utf-8")
    return 1 if report["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
