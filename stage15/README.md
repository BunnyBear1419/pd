# Stage 15 — Site Perimeter, Security, Landscaping and Lighting

## Purpose
Adds a separate planning layer for perimeter fence guides, provisional gate zones, exterior lighting locations, landscape beds, and drainage/grading review lines.

## Run
1. Open the current project in Blender.
2. Go to Scripting and load `stage15/generate_stage15_site_security.py`.
3. Run the script.
4. Inspect `PDHQ_SITE_SECURITY_LANDSCAPE_GUIDES` from top, street/frontage, and building-height views.

Reruns clear and rebuild only this collection. Previous stages are not modified.

## Configuration
The CONFIG dictionary at the top controls the approximate site bounds, fence dimensions, gate positions and widths, lighting spacing, landscape beds, drainage guide count, and guide visibility toggles.

All site bounds and gates are **provisional**. Check the actual site apron and approach before accepting them. The fence generator leaves an opening on the front boundary for the main gate; the service-gate zone is a planning marker only and does not create a second opening automatically.

## Limitations
These are visual blockout guides, not a final perimeter design, functional gate, light fixture photometry, engineered drainage solution, landscaping asset set, production collision, or Sollumz-ready export. Drainage lines do not represent surveyed elevations or actual water flow. Ensure access routes, emergency egress, turning areas, and sightlines remain clear.

## Review
- Match fence and gate guides to the intended site boundary and real approach roads.
- Verify fence posts and rails do not intersect the building, vehicle paths, or emergency access.
- Check gate width against the largest planned vehicle and any security booth/checkpoint to be designed later.
- Confirm lighting locations avoid glare into windows and provide safe visibility without excessive draw calls.
- Keep planting clear of door swings, vehicle sightlines, emergency access, and collision paths.
- Have drainage and grading reviewed against the final ground surface.
- Hide/remove guide geometry before export if it is not intended to appear in-game.
