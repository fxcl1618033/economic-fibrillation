# results/

Analysis results kept in git, one file per test: `results/<sample>/<convention>/<test>.json`, each with its config,
seed, code version and timestamp (Phase 3 of `HANDOFF.md`). Generated files that need not be kept go to `build/`
(git-ignored).

- `S26/`, `S30/`: every pre-registered test under convention P and the sensitivity conventions W, N, E and C
  (`make phase3`; `docs/preregistration_S30.md`). Variants: `*_strict/` (rolling windows inside 1970–2022),
  `*_gmd_growth/` (open issue 13), `S30_minus_<ISO>/` (added economies left out).
- `COMPARISON.md`: every registry quantity on S26 and S30, with the sensitivity tables; `SUMMARY.md` is the plain-words
  summary written after the run.
- `followup/` and `FOLLOWUP.md`: checks Sid asked for after reading the results (`make followup`). **Not
  pre-registered**; labelled so in each file.
