# Stage 23 — FiveM resource packaging preflight

Stage 23 prepares a packaging checklist and a lightweight filesystem validator for the eventual exported map resource.

## Files

- `validate_stage23_resource.py` — checks a resource folder for `fxmanifest.lua`, `stream/`, expected asset extensions, and common manifest omissions.
- `fxmanifest.lua.template` — illustrative starter template; review and rename/copy it before use.
- `RESOURCE_PACKAGING_AND_INSTALL_CHECKLIST.md` — packaging and server-install review.

## Run the validator

Use standard Python against the actual exported resource folder, not the repository's Stage 23 folder:

```powershell
python validate_stage23_resource.py "C:\path\to\your\resource" --json-out "resource-preflight.json"
```

A non-zero exit code indicates structural issues such as a missing manifest or empty/missing stream folder. Warnings require human review. The template is not an install-ready resource until the actual exported files and correct paths are added.

## Limits

The validator does not parse Lua, validate YMAP/YTYP internals, export Sollumz assets, or launch FiveM. Successful structure checks are not proof that the MLO loads or behaves correctly in game.
