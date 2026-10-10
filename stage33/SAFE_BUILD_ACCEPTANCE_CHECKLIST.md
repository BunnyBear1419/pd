# Stage 33 — Safe Build Acceptance Checklist

- [ ] First run uses a new versioned output path.
- [ ] A second run targeting an existing output is refused without `--overwrite`.
- [ ] When `--overwrite` is supplied, the previous `.blend` remains available as a timestamped backup.
- [ ] Output and JSON report paths are different.
- [ ] Run from a clean, saved copy of the project; remember Stage 2 resets scene objects.
- [ ] Inspect the new scene in Blender and review the report before any GTA export.
- [ ] Keep the old scene and report until the new build is inspected.
- [ ] Never interpret GitHub syntax/package success as proof that Blender executed or that the MLO is valid.
