# Hash map

The public history of this repository was filtered with `git filter-repo` on 27 October 2026, before its first publication: third-party data whose terms do not allow redistribution, personal material and work for later papers were removed from every commit; in the files that remain, the personal parts of CLAUDE.md, a credit line in two frozen atlas scripts, two local paths, six rows of docs/decisions.md (about later work) and the title of a personal book in docs/open_issues.md were removed too, and the author's email was replaced by a GitHub no-reply address. Everything else is unchanged, including every commit's date and order, but every commit has a new hash. Documents written before the release cite the old hashes; this table translates them.

59 commits kept, 7 not in the public history (they held only removed material).

| Hash before the release | Public hash | Date | Subject |
|---|---|---|---|
| `96d2270` | `c4e9621` | 2026-10-11 | Import repository exactly as received (handoff of 11 October 2026) |
| `280b1f8` | `a0685b9` | 2026-10-11 | Phase 0: pinned environment, Makefile, src/ef package, three-outcome reproduction check |
| `1fe4d69` | `a66e8b3` | 2026-10-11 | Phase 1: reproducible data build (make data) |
| `57432e7` | `8b4cff0` | 2026-10-11 | Pin BIS bank lending and IMF bilateral trade data for the GNN |
| `47cbdfd` | `58af50e` | 2026-10-11 | Float64 GMD reads in src, D10 wording, BIS release record, Phase 3 and GNN requirements |
| `3d8503d` | `a59cfa4` | 2026-10-11 | Fix invalid YAML in the BIS entry of data/sources.yaml; add a parse test |
| `6ecf40c` | `2c1f33f` | 2026-10-11 | Phase 2: core library in src/ef reproducing every Paper 1 golden number |
| `56df70d` | `bec4158` | 2026-10-11 | Golden check report for the Phase 2 library (docs/golden_check.md) |
| `4872c0b` | `fd16dab` | 2026-10-11 | Pre-register the S30 rerun; propose Methods edits; apply Sid's decisions |
| `698e38d` | `3ed6525` | 2026-10-11 | Pre-registration: one rolling-window rule (windows from 1962, never earlier); strict inside-1970-2022 as sensitivity |
| `902cfc2` | `7e87928` | 2026-10-11 | Sign the S30 pre-registration |
| `05836e0` | `45fe40b` | 2026-10-11 | Pre-registration amendment 1: implementation clarifications, before any S30 run |
| `094f350` | `5614b1c` | 2026-10-11 | Pre-registration amendment 2: past-only channel phases need 16 years of history |
| `df8edd6` | `6088c0b` | 2026-10-11 | Phase 3 driver, channel tests and comparison report |
| `07bbdd8` | `41d9965` | 2026-10-11 | Decision log: pre-registration signed, amendments, Phase 3 run notes, D6 counts |
| `0617bf6` | `1970dfb` | 2026-10-11 | Phase 3 results: pre-registered rerun on S26 and S30 with every variant |
| `404ea25` | `ee2bdb8` | 2026-10-11 | Leave-one-crisis-out follow-up for the early-warning trends (not pre-registered) |
| `2671564` | `23dadb2` | 2026-10-11 | Second draft of the Methods edits and the registry on S30 after Phase 3 |
| `f60ed64` | `658521a` | 2026-10-11 | Follow-up results, decision log and issue statuses after Sid's Phase 3 review |
| `26f8ea8` | `6c21b19` | 2026-10-11 | Share of world GDP for each sample in the data validation report |
| `f0e9d3b` | `eda3e94` | 2026-10-11 | Third draft of the Methods edits after Sid's second round |
| `ef0dc40` | `532a366` | 2026-10-13 | Pre-registration amendment 3: Russia, the S31 sensitivity sample |
| `f8f32e2` | `427c14e` | 2026-10-13 | Amendment 3 replaced: S31 (S30 + Russia) becomes the main sample |
| `5337eab` | `e886f9e` | 2026-10-13 | Phase 3 driver and report for S31: base sample, late entrants, S30-S31 sections |
| `2a686a3` | `a51d53a` | 2026-10-13 | Russia's data for S31 (amendment 3): atlas panel, validation, IMF trade |
| `0e02ec8` | `cf12810` | 2026-10-13 | Comparison: every S30-S31 crossing; follow-up runs on S26, S30 and S31 |
| `b741410` | `cdc6ee7` | 2026-10-13 | Phase 3 results on S31 (S30 + Russia), pre-registered in amendment 3 |
| `091453b` | `a90fafb` | 2026-10-13 | Follow-up (not pre-registered): leave-one-crisis-out of the variance trend on S31 |
| `93fa8ff` | `dbfb894` | 2026-10-13 | S31 summary in plain words, included in COMPARISON.md |
| `b5ab8ce` | `25259ad` | 2026-10-13 | Registry: S31 column (main sample), S31 robustness table, Russia-from-1992 rows |
| `e4a6e9b` | `1a6b914` | 2026-10-13 | S31 summary: exact count of leave-outs that move after-2 |
| `c842019` | `8791a2c` | 2026-10-13 | Methods edits (fourth draft), decisions and plan for S31 as the main sample |
| `a4ea871` | `d04680e` | 2026-10-13 | GNN stage G0: yearly heterogeneous graphs on S31, data card and missing-data report |
| `69cf512` | `ce302cc` | 2026-10-13 | G0 finished: oil weights, edge normalisation, World Bank GDP denominators |
| `0b6f6e3` | `dd49fc2` | 2026-10-13 | Decision log: EIA vs OWID oil production tolerance, fixed before the comparison is run |
| `ef632d4` | `2c9c9f0` | 2026-10-13 | G0 third build: EIA oil production within the pre-set tolerance, true-zero producers, price flags; fresh World Bank download fails its exact-match check |
| `9c532fc` | `607c166` | 2026-10-13 | G1 pre-registration: simulated worlds with known coupling, committed before calibration and before any test run |
| `30b095e` | `57619e5` | 2026-10-13 | G1 pre-registration amendment 1: coupling bracket 0.001-50 for numerical stability, before any test run |
| `a868bba` | `84a0d8d` | 2026-10-14 | GNN stage G1: simulated worlds with known coupling through every Paper 1 test, and the kappa = 0 check |
| `c1054a9` | `650430f` | 2026-10-14 | G0 denominators from the fresh World Bank vintage (Sid, option b); Brazil 1970-88 and Iran 1991-92 unmasked |
| `864317a` | `ad7a028` | 2026-10-14 | Pre-registration amendment 4: edge-matched nulls for the tests that lean on 2019-2022, committed before any run |
| `fc63e87` | `3ebaacc` | 2026-10-14 | Edge-matched nulls (amendment 4): code, committed before any run |
| `83a86b4` | `8ee664e` | 2026-10-14 | Amendment 4 run: edge-matched nulls validated on the G1 worlds and run on S31/S30/S26; Methods edits fifth draft |
| `1671a2a` | `36a3159` | 2026-10-14 | DTT D0: Sid's report brought in as a frozen record (no code exists); first findings |
| `c480fbc` | `2e9969a` | 2026-10-14 | DTT D1: clean implementation (src/ef/dtt.py, seed 1310), tests, and the report reproduced from its equations |
| `a4d6e36` | `31a68c4` | 2026-10-14 | DTT D2 plan, committed before any D2 run |
| `a2f2d16` | `fbb4a2d` | 2026-10-14 | DTT D2: robustness runs (convergence, sweeps, mechanism ablation, shared fraction rho, timing) and regenerated figures |
| `dfb7261` | `bb10b71` | 2026-10-14 | DTT D3: effective number of economies on real data (descriptive), Paper 1 theory box draft, literature |
| `bf44e89` | `607d5a3` | 2026-10-14 | DTT D4: G1b pre-registration drafted (escape layer on the saved G1 network), not run |
| `8e7e67a` | `c2f63a0` | 2026-10-15 | G1b pre-registration amendment 1: Sid's choices, committed before any G1b run |
| `77cfb71` | `410b327` | 2026-10-15 | G1b code: escape layer on the G1 Kuramoto worlds, calibration, controls and checks (tests pass before the run) |
| `076920f` | `72d2833` | 2026-10-15 | G1b run: escape layer on the G1 Kuramoto worlds; verdict as pre-registered: partly (past-only lead-1 6.3%, above chance and both controls, but 6.3% of worlds at the real p against 20% required); G1 closing note |
| `62109da` | `434e97d` | 2026-10-15 | Paper 1 manuscript generator and first full draft; fifth-draft Methods edits applied to docs/methods.md (generated, every number from results files; changes logged per rule 6); main figures redrawn on S31 |
| `7b569ab` | `972b863` | 2026-10-15 | Close every Paper 1 issue (FIXED with commits, LIMITATIONS or FUTURE WORK); Paper 1 locked after G1b |
| `cabff32` | `13605a6` | 2026-10-15 | Paper 1 complete draft: caveats for Sid, Methods-vs-Results checks (three wording errors corrected), reference check, PDF install note (LaTeX, pandoc, poppler and Inter missing), manuscript tests |
| `70de0c4` | `dbe6d50` | 2026-10-15 | Paper 1 PDF built (pandoc + xelatex; TeX Gyre Pagella, Inter, Latin Modern Math by file name); figures redrawn in Inter; table column widths; caveats and checks updated |
| `9bc2238` | `26782d2` | 2026-10-15 | Paper 1: figures redesigned for print (vector, journal style); classic title block and abstract; editable LaTeX source in paper1/manuscript/latex/ (self-contained, XeLaTeX/Overleaf) from which the PDF is built |
| `57ac50e` | `1c741b5` | 2026-10-15 | Paper 1 LaTeX source compiles with pdfLaTeX (Overleaf default), XeLaTeX or LuaLaTeX; one line per paragraph, real dashes; plain date line on the title page; Overleaf zip |
| `8f364a7` | not in the public history | 2026-10-16 | |
| `51f8804` | not in the public history | 2026-10-16 | |
| `28b650e` | not in the public history | 2026-10-16 | |
| `8fd3357` | not in the public history | 2026-10-16 | |
| `f69fcc9` | not in the public history | 2026-10-16 | |
| `5e5d8d5` | not in the public history | 2026-10-16 | |
| `d1357bd` | not in the public history | 2026-10-16 | |
| `18dd2d9` | `52a2dac` | 2026-10-20 | Public release preparation: licences, attribution notes, README, Data and code availability section |

## Tags

| Tag | Before the release | Public |
|---|---|---|
| `paper1-complete-v1` | `407fdb6` | `cd44061` |
| `paper1-complete-v1.1` | `5709c65` | `1ead1f1` |
| `paper1-complete-v1.2` | `4c356c0` | `f977962` |
| `paper1-complete-v1.3` | `9ea11f8` | `a00dc83` |
