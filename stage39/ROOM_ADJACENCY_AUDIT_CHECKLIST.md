# Stage 39 — Room adjacency and circulation audit checklist

Run from the repository root:

```bash
python stage39/audit_stage39_adjacency.py --output build/stage39_adjacency_report.json
```

- [ ] Review `status_counts` and every item in `checks`.
- [ ] Fix invalid room references in the Stage 36 schedule.
- [ ] Review `NOT_ADJACENT_IN_PACKING` pairs against the intended operational workflow.
- [ ] Treat `SHARED_EDGE_CANDIDATE` as a geometric hint only, not proof of a door.
- [ ] Resolve cross-floor links through the actual stair/elevator cores.
- [ ] Check secure transfer, evidence, armory, public and vehicle routes separately.
- [ ] Verify actual wall openings, door widths/swings and accessibility in Blender.
- [ ] Keep the audit advisory until room layout is approved; it does not certify code or life safety.
