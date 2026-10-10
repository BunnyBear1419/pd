# Resource packaging and install checklist

## Exported resource folder

- [ ] Create a resource directory with a valid `fxmanifest.lua` at its root.
- [ ] Put the actual exported assets in `stream/`; do not ship empty folders or placeholder assets.
- [ ] Register each required `.ytyp` using the correct `DLC_ITYP_REQUEST` data-file entry and exact relative path.
- [ ] Confirm `.ymap`, `.ydr`, `.ydd`, `.ytd`, `.ybn`, and other files match the actual export and resource design.
- [ ] Remove temporary guides, audit reports, source `.blend` files, and unrelated working files from the runtime resource unless intentionally needed.
- [ ] Run `validate_stage23_resource.py` against the exported resource and resolve issues; review every warning.
- [ ] Verify file names and paths match case and spelling used by the manifest.

## Server installation

- [ ] Install the resource folder in the server's resources directory.
- [ ] Add the correct `ensure resource_name` entry to server configuration.
- [ ] Confirm map coordinates and avoid conflicts with other streamed map resources.
- [ ] Restart the server or resource using the normal development procedure and inspect server/client logs.
- [ ] Test fresh join, spawn, reconnect, entering and exiting the building, and changing camera positions.
- [ ] Test collision and player movement separately from visual streaming.
- [ ] Test with the server's full resource set and a second client.
- [ ] Keep a known-good version and record the exact tested commit/resource version.

## Acceptance gate

- [ ] No missing asset/path errors in logs.
- [ ] The custom map appears at the intended coordinates with no unintended base-game building overlap.
- [ ] Interior visibility, textures, collision, portals/occlusion, and LOD behavior are tested in-game.
- [ ] Resource starts cleanly after a fresh server restart.

The repository currently contains planning/generator/audit stages. Do not treat the template as a completed MLO resource until actual exported assets have been added and tested.
