# D0 — bringing in the DTT report and reproducing it

## What came in

Only the report: `dtt/legacy/DTT_Unified_Simulation_Report.pdf` (frozen, sha256 4e96a7cb…; see `dtt/legacy/README.md`).
**There is no code**, so the report's tables cannot be rerun from their own code. Following Sid's instruction, D0 goes
straight to D1: the rows Sid listed (sections B–F) are compared below with a clean implementation of the equations the
report states (`src/ef/dtt.py`, seed 1310). That is a reproduction of the report's *specification*, not of its runs:
Monte Carlo rows can at best agree within sampling error, and details the report does not state (integration step
for sections B and C, run-in, how R² was averaged) are my choices, listed with each section.

Marks: **EXACT** — the same number to the digits printed; **CLOSE** — within the stated tolerance; **DIFFERENT** —
outside it.

## Findings that need no code

- **Figure I4 is the mislabelled one, not its table.** The figure's y-axis ("absolute difference between sweep means")
  rises to 0.7, but the table printed under it gives max |state_up − state_down| = 2.977e-6, mean 9.6e-8, max
  |output_up − output_down| = 3.1e-6, and the *same* half-level crossing (g = 0.9) for both sweeps; the text says
  "effectively no hysteresis". The table is consistent with itself and with the text; a curve that reaches 0.7 cannot
  be a difference between two sweeps whose crossings coincide and whose largest gap is 3e-6. So the figure plots some
  other quantity under a wrong label. Which quantity cannot be determined without the code: its curve is neither the
  state (which reaches 0.9998 at g = 2, half-level at 0.9) nor the I3 branch gap (zero below g ≈ 1.25).
- **Figure F1's time axis cannot be matched to section F.** F1 is drawn on 0–40 "conditional simulation time" and its
  intermediate-coupling curve ends at 65%, but section F reports 800 steps, 93.5% events and median 202 steps for
  intermediate coupling (100%, median 34 steps, strong). No rescaling of the axis fits both curves: the medians read
  off F1 (about 25 and 6) have a ratio of about 4, the text's (202 and 34) about 6. F1 most likely shows a different run
  (its 0–40 range matches the cubic model's horizon of 40). The regenerated F1 (D2) is drawn in steps from the
  section F model.
- **Section C does not state its noise scale σ.** Figure C3 brackets it: the table's 23.6% at K = 0.8 lies between the
  σ = 0.75 and σ = 0.90 curves; σ = 0.82, the value of section D, is used below and checked.
- **The two K = 0 tipping rates disagree with each other** (section D 19/400 = 4.75%, section E 22/800 = 2.75%); the
  report says so ("distinct Monte Carlo runs").
