#!/usr/bin/env python3
"""Stage 50 read-only Blender audit for collision and visibility review.

Run with Blender:
  blender --background scene.blend --python stage50/audit_stage50_collision_visibility.py -- --output build/stage50_collision_visibility.json

This inventories likely collision meshes and visibility-transition geometry. It
does not author Sollumz collision, portals, occlusion, archetypes or map fixes.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector

COLLISION_TOKENS = ("collision", "collider", "physics", "_col", "col_")
VISIBILITY_TOKENS = (
    "door", "window", "glass", "lobby", "corridor", "hall", "stair",
    "elevator", "garage", "roof", "helipad", "cell", "booking",
    "dispatch", "interview", "evidence", "armory",
)
PLACEHOLDER_TOKENS = ("placeholder", "proxy", "blockout", "guide", "temp")


def bounds(obj):
    try:
        corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        return {
            "min": [round(min(v[i] for v in corners), 3) for i in range(3)],
            "max": [round(max(v[i] for v in corners), 3) for i in range(3)],
        }
    except Exception:
        return None


def mesh_quality(obj):
    bm = bmesh.new()
    try:
        bm.from_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()
        loose_vertices = sum(1 for v in bm.verts if not v.link_edges)
        loose_edges = sum(1 for e in bm.edges if not e.link_faces)
        non_manifold_edges = sum(1 for e in bm.edges if not e.is_manifold)
        degenerate_faces = sum(1 for f in bm.faces if f.calc_area() <= 1e-10)
        return {
            "vertices": len(bm.verts),
            "edges": len(bm.edges),
            "faces": len(bm.faces),
            "loose_vertices": loose_vertices,
            "loose_edges": loose_edges,
            "non_manifold_edges": non_manifold_edges,
            "degenerate_faces": degenerate_faces,
        }
    finally:
        bm.free()


def build_report():
    scene = bpy.context.scene
    objects = list(scene.objects)
    meshes = [obj for obj in objects if obj.type == "MESH"]
    collision_candidates = []
    visibility_candidates = []
    placeholder_candidates = []
    mesh_findings = []
    for obj in meshes:
        name = obj.name.lower()
        row = {
            "object": obj.name,
            "collections": sorted(c.name for c in obj.users_collection),
            "bounds": bounds(obj),
            "dimensions": [round(float(v), 3) for v in obj.dimensions],
            "scale": [round(float(v), 4) for v in obj.scale],
            "material_slots": len(obj.data.materials),
        }
        if any(token in name for token in COLLISION_TOKENS):
            row["mesh_quality"] = mesh_quality(obj)
            collision_candidates.append(row)
        if any(token in name for token in VISIBILITY_TOKENS):
            visibility_candidates.append(row)
        if any(token in name for token in PLACEHOLDER_TOKENS):
            placeholder_candidates.append({"object": obj.name, "collections": row["collections"]})
        quality = row.get("mesh_quality")
        issues = []
        if len(obj.users_collection) == 0:
            issues.append("mesh is not linked to a collection")
        if any(abs(float(s)) < 1e-6 for s in obj.scale):
            issues.append("zero scale component")
        if not obj.data.materials:
            issues.append("no material slots assigned")
        if quality:
            if quality["degenerate_faces"]:
                issues.append("degenerate faces in collision-named candidate")
            if quality["loose_vertices"] or quality["loose_edges"]:
                issues.append("loose geometry in collision-named candidate")
        if issues:
            mesh_findings.append({"object": obj.name, "issues": issues})

    warnings = []
    if not collision_candidates:
        warnings.append("No mesh names matched collision tokens; confirm collision geometry exists and naming conventions are consistent.")
    if not visibility_candidates:
        warnings.append("No mesh names matched visibility-transition tokens; manually review doors, windows, stairs, garage openings and roof access.")
    if placeholder_candidates:
        warnings.append("Potential blockout/proxy objects remain; manually decide whether each belongs in the export.")
    if mesh_findings:
        warnings.append("Mesh-level findings need review; findings are heuristics and are not automatically fatal.")
    return {
        "stage": 50,
        "title": "Collision and Visibility Preflight",
        "scene": scene.name,
        "production_ready": False,
        "status": "REVIEW_REQUIRED",
        "counts": {
            "objects": len(objects),
            "meshes": len(meshes),
            "collision_name_candidates": len(collision_candidates),
            "visibility_name_candidates": len(visibility_candidates),
            "placeholder_name_candidates": len(placeholder_candidates),
            "mesh_findings": len(mesh_findings),
        },
        "collision_candidates": collision_candidates,
        "visibility_transition_candidates": visibility_candidates,
        "placeholder_candidates": placeholder_candidates,
        "mesh_findings": mesh_findings,
        "warnings": warnings,
        "manual_acceptance_checks": [
            "Inspect collision shapes and flags in the compatible Sollumz/CodeWalker toolchain; names and Blender mesh topology alone do not prove GTA collision validity.",
            "Walk every floor, cell, garage bay, stair, roof and helipad; check floor penetration, blocked doors, invisible barriers and fall-through gaps.",
            "Verify interior archetypes, rooms, portals and occlusion using the supported workflow; this audit does not create them.",
            "Verify intended suppression of overlapping default GTA building geometry at the chosen map location.",
            "Check texture/material assignments, export paths, resource manifest and actual FiveM loading.",
            "Test fresh join, respawn, reconnect and at least two clients with multiple camera angles on the target server.",
        ],
        "limitations": [
            "Name matching is heuristic and can miss poorly named objects or include unrelated ones.",
            "Non-manifold geometry is not automatically invalid for every collision use case; inspect each finding.",
            "This script does not modify the scene or author collision, portals, occlusion, LODs or Sollumz metadata.",
            "Only real CodeWalker and FiveM testing can establish runtime behavior.",
        ],
    }


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="build/stage50_collision_visibility.json")
    args = parser.parse_args(argv)
    report = build_report()
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    text = bpy.data.texts.get("PDHQ_STAGE50_COLLISION_VISIBILITY_REPORT") or bpy.data.texts.new("PDHQ_STAGE50_COLLISION_VISIBILITY_REPORT")
    text.clear()
    text.write(json.dumps(report, indent=2))
    print("Stage 50 collision/visibility preflight:", json.dumps(report["counts"], sort_keys=True))
    print("Wrote", output)


if __name__ == "__main__":
    main()
