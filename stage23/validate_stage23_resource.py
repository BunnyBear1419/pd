"""Stage 23: lightweight validator for an exported FiveM map resource folder.

Usage: python validate_stage23_resource.py PATH_TO_RESOURCE
This checks packaging structure only. It cannot validate GTA assets or MLO behavior.
"""
import argparse
import json
from pathlib import Path

EXPECTED_STREAM_EXTENSIONS = {".ymap", ".ytyp", ".ydr", ".ydd", ".ytd", ".ybn", ".ymf", ".yft"}
PLACEHOLDER_TOKENS = ("your_map", "replace_me", "todo", "placeholder", "example_map")


def inspect_resource(root: Path):
    issues = []
    warnings = []
    if not root.exists() or not root.is_dir():
        return {"resource": str(root), "valid_structure": False, "issues": ["Resource path does not exist or is not a directory."], "warnings": []}

    manifest = root / "fxmanifest.lua"
    stream = root / "stream"
    if not manifest.is_file():
        issues.append("Missing fxmanifest.lua at resource root.")
    if not stream.is_dir():
        issues.append("Missing stream/ directory.")
        files = []
    else:
        files = sorted(p for p in stream.rglob("*") if p.is_file())
        if not files:
            issues.append("stream/ contains no exported asset files.")

    asset_files = [p for p in files if p.suffix.lower() in EXPECTED_STREAM_EXTENSIONS]
    other_files = [p for p in files if p.suffix.lower() not in EXPECTED_STREAM_EXTENSIONS]
    if files and not asset_files:
        warnings.append("No recognized GTA map/model asset extensions found under stream/.")
    if not any(p.suffix.lower() == ".ytyp" for p in asset_files):
        warnings.append("No .ytyp found; verify whether this resource requires an archetype definition and DLC_ITYP_REQUEST entry.")
    if not any(p.suffix.lower() == ".ymap" for p in asset_files):
        warnings.append("No .ymap found; verify map placement and whether the exported resource should contain one.")
    if other_files:
        warnings.append("Unrecognized file types under stream/: " + ", ".join(str(p.relative_to(root)) for p in other_files[:30]))

    manifest_text = ""
    if manifest.is_file():
        try:
            manifest_text = manifest.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            issues.append("Could not read fxmanifest.lua: " + str(exc))
        lower = manifest_text.lower()
        if "fx_version" not in lower:
            issues.append("fxmanifest.lua does not declare fx_version.")
        if "game" not in lower:
            warnings.append("fxmanifest.lua does not visibly declare a game target; review the manifest.")
        if "this_is_a_map" not in lower and "'map'" not in lower and '"map"' not in lower:
            warnings.append("Manifest does not visibly mark this as a map; confirm the appropriate map-resource setup for the export.")
        placeholders = [token for token in PLACEHOLDER_TOKENS if token in lower]
        if placeholders:
            warnings.append("Manifest may still contain template placeholders: " + ", ".join(placeholders))
        ytyp_names = [p.name.lower() for p in asset_files if p.suffix.lower() == ".ytyp"]
        if ytyp_names and "dlc_ityp_request" not in lower:
            warnings.append("A .ytyp exists but DLC_ITYP_REQUEST was not found in fxmanifest.lua; verify registration syntax and paths.")

    return {
        "resource": str(root.resolve()),
        "valid_structure": not issues,
        "issues": issues,
        "warnings": warnings,
        "manifest_present": manifest.is_file(),
        "stream_directory_present": stream.is_dir(),
        "stream_file_count": len(files),
        "recognized_asset_files": [str(p.relative_to(root)) for p in asset_files],
        "other_stream_files": [str(p.relative_to(root)) for p in other_files],
        "limitations": [
            "This is a filesystem and text heuristic, not a Lua interpreter or FiveM asset validator.",
            "It does not validate YMAP/YTYP internals, Sollumz metadata, collision, portals, occlusion, LODs, textures, or coordinates.",
            "A structurally valid folder can still fail to load or render correctly in FiveM.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("resource_path", help="Path to the exported FiveM map resource directory")
    parser.add_argument("--json-out", help="Optional path to write the JSON report")
    args = parser.parse_args()
    report = inspect_resource(Path(args.resource_path).expanduser())
    output = json.dumps(report, indent=2)
    print(output)
    if args.json_out:
        Path(args.json_out).write_text(output + "\n", encoding="utf-8")
    if report.get("issues"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
