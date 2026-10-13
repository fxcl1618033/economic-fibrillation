# D2 plan — robustness of the DTT escape model (simulation only)

Written 14 October 2026 and committed before any D2 run. Runs Sid's own "recommended next simulation sequence" (report,
section J) with the clean implementation (`src/ef/dtt.py`, seed 1310), plus one item on timing. No real data. Every
condition is reported, including those where an effect vanishes. Results: `dtt/results/d2_*.json`,
`dtt/D2_report.md`, figures in `dtt/fig/` (the report's own figures stay in `dtt/legacy/figures_extracted/`).

## Base configuration

The report's sections D and E: N = 31 oscillators, ωᵢ ~ Normal(0, 1) drawn per trial, oscillator diffusion D = 0.02,
phases uniform at t = 0 (no run-in), bistable state dx = (μ + x − x³)dt + g(t)dW with μ = 0.2 from the lower well,
tipping = first x ≥ 0 within T = 40, noise σ = 0.82, Euler–Maruyama step 0.01. K ∈ {0, 0.8, 1.333, 1.867, 3.2} unless
stated. Uncertainty: Wilson 95% intervals for rates; for differences between formulations run on the same R(t) traces
and the same Brownian increments, the paired 95% interval of the difference (normal approximation on the per-trial
differences). An effect "vanishes" in a condition when its 95% interval contains 0.

## What each comparison measures (Sid's first two "known problems")

- **Coupling** — tipping at K > 0 against K = 0 *within the same model*. This is the fair measure of what coupling
  does.
- **Fluctuation of R** — σR(t) at K = 0 against the independent-noise control σ/√N. At K = 0, E[R²] = 1/N exactly,
  so the two have the same mean square noise; any gap comes from R(t) fluctuating (escape is convex in the noise), not
  from coupling. This is what the report's 4.75% vs 0.325% measures.
- **Time variation** — σR(t) against each trial's constant RMS of σR(t) (same traces, same increments): whether the
  path of R matters beyond its mean square (the report's section E).
- **Order in time** — σR(t) against R(t) with its time order permuted: step by step (destroys persistence; close to
  constant RMS by construction) and in blocks of 1 time unit (keeps episodes, randomizes when they happen).
- "More synchrony → more tipping" is partly built in (g rises with R by assumption, and escape rises with noise); the
  sweeps report it but it is not the finding. The informative parts are the time-variation and order effects and the
  timing.

## Runs

1. **Euler–Maruyama convergence.** Steps 0.02, 0.01, 0.005 and 0.0025 with common random numbers: oscillator and
   state increments drawn at 0.0025 and summed for the coarser steps, all four integrated side by side. Outcomes per K:
   tipping with σR(t), with each trial's constant RMS, and with independent noise; mean R. 1,000 trials per K.
   Converged when the 0.005 and 0.0025 estimates agree within the paired 95% interval; the gap between 0.01 (the
   report's step) and 0.0025 is reported.
2. **Parameter sweeps**, one at a time around the base, K ∈ {0, 0.8, 1.333, 1.867}, 2,000 trials per condition; for
   each condition the coupling, fluctuation, time-variation and order comparisons above with their intervals:
   oscillator diffusion D ∈ {0.005, 0.01, 0.02, 0.04, 0.08}; frequency dispersion (s.d. of ω) ∈ {0.5, 0.75, 1, 1.5, 2};
   N ∈ {11, 21, 31, 61, 121}; μ ∈ {0, 0.1, 0.2, 0.3}; σ ∈ {0.5, 0.65, 0.82, 1.0, 1.2}; horizon T ∈ {10, 20, 40, 80}.
3. **Mechanism ablation on the same R(t) traces**, K ∈ {0, 0.8, 1.333, 1.6, 1.867, 3.2}, 4,000 trials: σR(t); each
   trial's constant RMS; the ensemble RMS; step-permuted R(t); block-permuted R(t) (1 time unit); independent noise.
4. **Shared fraction ρ from 0 to 1** in steps of 0.1, g = σ√(ρR(t)² + (1 − ρ)/N) (ρ = 0 is the independent control,
   ρ = 1 the report's model), K ∈ {0, 0.8, 1.333, 1.867}, 2,000 trials, on common traces; with σR-type noise and its
   per-trial constant RMS at each ρ.
5. **Timing (added).** For the tipping trials of run 3 at K = 0.8 and 1.333: the mean of R(t) in the 10 time units
   before first passage (superposed on the passage time) against the mean R at the same clock times in trials that had
   not tipped by then; and the autocorrelation time of R(t). Under the model, escape happens when the noise is large,
   so R is raised before escape by construction; what this measures is how far ahead it is raised, in model time. It is
   descriptive and sets up G1b, which asks whether such a lead survives the Paper 1 pipeline.
6. **Figures regenerated** from this code with the project palette: B1, B2, C2, C3, D1, D2, E1 and F1 (F1 with its time
   axis in steps, from the section F model), plus one figure per run above.

Runtime estimate on this Mac: about 30 minutes in all (the sweeps dominate; conditions run in parallel).
