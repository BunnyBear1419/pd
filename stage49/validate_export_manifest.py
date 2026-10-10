#!/usr/bin/env python3
"""Validate a real FiveM stream export manifest against files on disk.

Expected JSON shape:
{
  "schema_version": 1,
  "assets": [
    {"path": "resource/stream/example.ydr", "size_bytes": 123,
     "sha256": "<64 lowercase or uppercase hex chars>", "kind": "model"}
  ]
}
Paths are project-root-relative and must remain inside resource/stream.
This tool validates inventory integrity; it does not validate GTA formats.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
from pathlib import Path, PurePosixPath


SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def validate_manifest(root: Path, manifest_path: Path) -> dict:
    root = root.resolve()
    manifest_path = manifest_path.resolve()
    errors: list[str] = []
    checked: list[dict] = []
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {"status": "INVALID", "production_ready": False,
                "errors": [f"Cannot read valid JSON manifest: {exc}"], "assets_checked": 0}

    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return {"status": "INVALID", "production_ready": False,
                "errors": ["Manifest must be an object with schema_version: 1."],
                "assets_checked": 0}
    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        errors.append("'assets' must be a non-empty list.")

    seen: set[str] = set()
    for index, asset in enumerate(assets if isinstance(assets, list) else []):
        prefix = f"assets[{index}]"
        if not isinstance(asset, dict):
            errors.append(f"{prefix} must be an object.")
            continue
        rel = asset.get("path")
        if not isinstance(rel, str) or not rel.strip():
            errors.append(f"{prefix}.path must be a non-empty relative path.")
            continue
        posix = PurePosixPath(rel.replace("\\", "/"))
        if posix.is_absolute() or ".." in posix.parts or not posix.parts:
            errors.append(f"{prefix}.path is absolute or contains traversal: {rel!r}")
            continue
        normalized = posix.as_posix()
        if not normalized.startswith("resource/stream/") or normalized == "resource/stream/":
            errors.append(f"{prefix}.path must point inside resource/stream/: {rel!r}")
            continue
        if normalized in seen:
            errors.append(f"Duplicate asset path: {normalized}")
            continue
        seen.add(normalized)
        target = (root / Path(*posix.parts)).resolve()
        stream_root = (root / "resource" / "stream").resolve()
        try:
            target.relative_to(stream_root)
        except ValueError:
            errors.append(f"{prefix}.path resolves outside resource/stream/: {rel!r}")
            continue
        if not target.is_file():
            errors.append(f"Missing asset file: {normalized}")
            continue
        size = asset.get("size_bytes")
        digest = asset.get("sha256")
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            errors.append(f"{prefix}.size_bytes must be a non-negative integer.")
            continue
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            errors.append(f"{prefix}.sha256 must be a 64-character hexadecimal digest.")
            continue
        actual_size = target.stat().st_size
        actual_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        item_errors = []
        if size != actual_size:
            item_errors.append(f"size mismatch (manifest {size}, actual {actual_size})")
        if digest.lower() != actual_hash:
            item_errors.append("SHA-256 mismatch")
        if item_errors:
            errors.append(f"{normalized}: " + "; ".join(item_errors))
        else:
            checked.append({"path": normalized, "size_bytes": actual_size, "sha256": actual_hash})

    status = "VALID_INVENTORY" if not errors else "INVALID"
    return {
        "status": status,
        "production_ready": False,
        "manifest": str(manifest_path),
        "assets_declared": len(assets) if isinstance(assets, list) else 0,
        "assets_checked": len(checked),
        "total_bytes_checked": sum(item["size_bytes"] for item in checked),
        "verified_assets": checked,
        "errors": errors,
        "limitations": [
            "A valid hash inventory does not prove that files are valid GTA/FiveM assets.",
            "Use CodeWalker and a real FiveM server for format, archetype, collision, visibility and multiplayer validation.",
            "This report never marks the MLO production-ready."
        ]
    }


def self_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        stream = root / "resource" / "stream"
        stream.mkdir(parents=True)
        asset = stream / "fixture.ydr"
        payload = b"stage49-test-fixture"
        asset.write_bytes(payload)
        manifest = root / "build" / "export_manifest.json"
        manifest.parent.mkdir()
        base = {"schema_version": 1, "assets": [{
            "path": "resource/stream/fixture.ydr",
            "size_bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "kind": "model"
        }]}
        manifest.write_text(json.dumps(base), encoding="utf-8")
        assert validate_manifest(root, manifest)["status"] == "VALID_INVENTORY"
        base["assets"][0]["path"] = "resource/stream/../../outside.ydr"
        manifest.write_text(json.dumps(base), encoding="utf-8")
        assert validate_manifest(root, manifest)["status"] == "INVALID"
        base["assets"][0]["path"] = "resource/stream/fixture.ydr"
        base["assets"][0]["sha256"] = "0" * 64
        manifest.write_text(json.dumps(base), encoding="utf-8")
        assert validate_manifest(root, manifest)["status"] == "INVALID"
    print("Stage 49 export-manifest validator self-test: PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="project root")
    parser.add_argument("--manifest", default="build/export_manifest.json")
    parser.add_argument("--output", default="build/stage49_export_manifest_validation.json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    root = Path(args.root).expanduser().resolve()
    manifest = Path(args.manifest)
    if not manifest.is_absolute():
        manifest = root / manifest
    report = validate_manifest(root, manifest)
    output = Path(args.output)
    if not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "assets_checked": report["assets_checked"],
                      "errors": len(report["errors"]), "production_ready": False}, indent=2))
    return 0 if report["status"] == "VALID_INVENTORY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
