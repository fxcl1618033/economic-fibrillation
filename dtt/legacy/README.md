# DTT legacy record (frozen)

Sid's prior work on diversification-type tipping, brought in on 14 October 2026. **Frozen: never edited**, like
`paper1/scripts/`. New code is `src/ef/dtt.py`.

| File | What | sha256 |
|---|---|---|
| `DTT_Unified_Simulation_Report.pdf` | "DTT: Diversification-Type Tipping — Unified mathematical simulation report", 15 pages, prepared 13 October 2026. Copied unchanged from `~/Downloads/` (Sid's message pointed to `incoming/dtt/`, which does not exist) | 4e96a7cb0cb325fef08edaf99d231566a907bf6fa0d123c253df2745a008e2ca |
| `figures_extracted/figure_<ID>.png` | The 15 figures embedded in the PDF (B1, B2, C2, C3, D1, D2, E1, F1, G1, G2, H1, I1–I4), extracted byte for byte from the PDF's image streams with PyMuPDF 1.28.2 (`extract_image`), named by the caption on their page | — |

**No code.** No simulation code came with the report: none was found beside the PDF or anywhere on the Mac, and
the PDF has no embedded files. Its metadata: title "DTT Unified Mathematical Simulation Report", producer ReportLab,
author field "OpenAI", created 2026-10-13 01:39 UTC. The numbers in it therefore cannot be rerun from their own code;
`dtt/D0_reproduction.md` compares them with a clean implementation of the equations the report states
(`src/ef/dtt.py`).

Scope (Sid, 14 October 2026): sections A–F are worked on; cascades, asymmetric restoration and hysteresis
(sections G–I) are kept here as frozen records only.
