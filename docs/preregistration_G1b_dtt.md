# Pre-registration — G1b, a synchrony-driven escape layer on the G1 worlds

Written 14 October 2026. **Status: Sid chose on 15 October 2026 (amendment 1, at the end); nothing had been run when it was committed.** The choices marked
**[Sid]** below need his decision; my recommendation is given for each. Once he has chosen, the decisions are added
to this file as a dated amendment and committed, and only then does anything run (`CLAUDE.md` rule 3). Code will go
in `src/ef/gnn/g1b.py`; results in `gnn/G1b/` and `gnn/G1b_report.md`.

## The question

The past-only lead-1 of Paper 1 (S31: +0.379, p = 0.038 against 53 circular shifts) was not reproduced by any G1
setting: in the calibrated Kuramoto and Stuart–Landau worlds, with recessions dated from the real calendar or from each
world's own output, it rejected in 0.8–4.6% of worlds, never above chance. **Does a synchrony-driven escape layer on
top of the calibrated G1 Kuramoto world reproduce it?**

**Said plainly, before anything runs:** the layer makes recessions more likely when synchrony is high (synchrony →
larger common shocks → escape → recession). The coupling runs one way, so some lead of synchrony over recessions is
expected **by construction**. Finding one is not evidence for DTT. The informative parts are (1) whether the lead
survives what the Paper 1 pipeline does to it — annual sampling, 53 points, phases from past data only, and a handful
of events of which two carry the real result — at the size seen in the real data, and (2) whether it beats the same
layer with constant noise or with synchrony shuffled in time. If it does not survive, the escape layer cannot be the
explanation of the real past-only lead either.

## The worlds

The G1 Kuramoto worlds exactly as run in G1 (`gnn/G1_report.md`, `docs/preregistration_G1.md`): 31 economies on the
**saved G1 trade network** (`gnn/G1/trade_network.npz`, the G0 build of 13 October with the earlier World Bank
denominators — Sid, 14 October 2026, so the controls compare directly with the reported G1 results), the G1
calibration (`gnn/G1/calibration.json`: σ = 1.58, κ\* = 15.5, φ\* = 1.95), Euler–Maruyama with dt = 0.01 years from
1850, 1950–2022 kept, the same world seeds as G1 (`[2001, model, setting]`), so a G1b world is the G1 world with the
same index plus a layer that does not feed back on it. Three settings, 1,000 worlds each: **trade links at κ\***
(primary), **no coupling** (κ = φ = 0) and **common forcing only** (φ\*). Kuramoto only (Sid: "on top of the
calibrated G1 Kuramoto world").

## The escape layer

**Primary — one world-level bistable state** (recommended; **[Sid]** world-level vs per-economy):

  dx = (μ + x − x³) dt + g(t) dW,  g(t) = σ_e · r(t),

integrated in the same time loop as the oscillators (dt = 0.01, time in years, so the state relaxes in its well in
about 0.8 years), with r(t) the instantaneous order parameter of the 31 phases and an independent Brownian motion W.
**[Sid]** r(t) unweighted (recommended; the report's form) or the GDP-weighted |Σ wᵢ Aᵢ e^{iθᵢ}| (closer to world
output, but it brings swing sizes in).

**Sensitivity — one bistable state per economy:** dxᵢ = (μ + xᵢ − xᵢ³) dt + σ_e vᵢ·dW with vᵢ = (cos θᵢ, sin θᵢ) and
one common two-dimensional Brownian motion W. Each economy's noise has variance σ_e² dt; two economies' pushes are
correlated by cos(θᵢ − θⱼ), so aligned economies are pushed together. The world average reproduces the primary
model's noise exactly (variance σ_e² r²). A year is a recession when at least **X = 50%** of economies escape in it
(**[Sid]** X; 50% recommended).

**Recession dating on the annual grid.** A year is a recession year when an escape (the state reaching x ≥ 0 from the
lower well) happens in it. Only 1970–2022 count, as in Paper 1.

**Recovery and reset (fixed before anything runs).** At an escape the state is reset to the lower well (x = −0.879
for μ = 0.2) at once, and escapes in the next **2 calendar years** are not counted as new recessions (refractory, so one
episode is one recession). **[Sid]** this rule (recommended) or letting the state sit in the upper well until it
returns on its own (two more parameters' worth of behaviour, harder to calibrate).

**Calibration — to the frequency of global recessions only, never to their timing.** μ is fixed at the report's 0.2
and σ_e is set by bisection so that the mean number of recession years in 1970–2022 is **5** (Kose, Sugawara and
Terrones), over 500 calibration worlds per setting (seed 5001). **[Sid]** fix μ = 0.2 and calibrate σ_e (recommended;
one target cannot pin two parameters), with μ = 0.1 and 0.3, each with its own σ_e, as a sensitivity on the primary
setting. Nothing in the calibration uses which years are recessions.

## Controls, each calibrated to the same recession frequency

1. **Constant-noise layer:** g = σ_c, not scaled by synchrony (σ_c calibrated to 5 recessions). Recessions then have
   nothing to do with the world's phases.
2. **Time-shuffled synchrony:** g(t) = σ_e r(π(t)), each world's own r(t) with its years shuffled (blocks of one
   year), σ_e recalibrated. Same distribution of noise, timing unrelated to the phases.
3. **The plain G1 world:** recessions dated from world output (G1's rule B: the five worst years for world GDP per
   capita, at least 5 years apart) on the same worlds — already computed in `gnn/G1/` (the past-only lead-1 rejected in
   1.7% of κ\* worlds, 2.9% with no coupling, 2.5% with forcing).

## Outcomes

For every setting and layer, over 1,000 worlds, with the Paper 1 pipeline unchanged (convention P for the two-sided
arc, convention C for the past-only arc, circular shifts, `ef.paper1`):

- the share of worlds in which the **past-only lead-1** rejects at p ≤ 0.05 (exact rate if nothing is there: 2/53 =
  3.8%), with its Wilson 95% interval;
- the same for the **two-sided arc** at lead-2, lead-1, the crisis year, after-1 and after-2;
- **where the real result falls**: the share of worlds whose past-only lead-1 has p ≤ 0.038 (the real p, the second
  smallest value 53 shifts allow) and the share whose correlation is at least +0.379 (the real value);
- the number of recession years per world (its distribution), and the same rates for the worlds with 4–6 recessions;
- descriptive: the mean r in recession years, the year before and other years.

## Thresholds, stated before any run (proposals; **[Sid]**)

The escape layer **reproduces the lead** if all three hold on the primary setting (κ\*, world-level, μ = 0.2):

1. the past-only lead-1 rejects more often than chance: the lower end of its 95% interval is above 3.8%;
2. it rejects more often than both the constant-noise and the time-shuffled controls: the 95% interval of each
   difference (escape layer minus control, worlds paired by index) lies above 0;
3. the real result is an ordinary outcome of the layer: at least **20%** of worlds reach p ≤ 0.038.

**Partly** if 1 and 2 hold but fewer than 20% of worlds reach p ≤ 0.038 (the layer makes the lead possible but the real
size is unusual for it). **Not reproduced** otherwise. The same verdicts are reported for the no-coupling and forcing
settings, the per-economy sensitivity and the μ sensitivity, without changing the thresholds.

## Runtime estimate (this Mac: 4 performance and 6 efficiency cores)

From the G1 runs: 1,000 Kuramoto worlds take about 25 seconds to simulate with the layer, and the two arcs (P and C)
about 0.1 seconds per world, so about a minute per setting on 8 processes; calibration (16 bisection steps of 500
worlds, simulation only) about 3–4 minutes per setting. Three world settings × four layers (escape, per-economy,
constant noise, shuffled) plus two μ sensitivities: about **1 to 1.5 hours** in all.

## What this will not do

It will not fit anything to the recession years, change any G1 or Paper 1 number, or enter Paper 1 (Sid: no tipping
simulations in Paper 1). Cascades, asymmetric restoration and hysteresis (DTT sections G–I) stay out.

---

## Amendment 1 — Sid's decisions (15 October 2026, committed before any G1b run)

Sid chose on 15 October 2026. Where this amendment and the draft above differ, this amendment holds. **G1b is the last
test Paper 1 takes; after it Paper 1 is locked** (`docs/decisions.md`).

**1. Layer.** World-level bistable state is primary. Per-economy states are a sensitivity: a year is a recession year
when at least **50%** of the 31 economies escape in it (each economy resets at its own escape; the refractory rule
below applies to recession years).

**2. Synchrony measure.** Unweighted r(t) = |mean_i e^{iθᵢ(t)}| is primary; the amplitude-weighted Ā·R_A(t) =
|mean_i Aᵢ e^{iθᵢ(t)}| (Aᵢ the fixed swing sizes of the G1 Kuramoto worlds, `simulator.targets()['A']`) is a
sensitivity. **The escape noise is driven by the model's true phases θᵢ(t)** at every Euler step, never by pipeline
phases. **The tests run on pipeline phases** of the simulated output (annual GDP, band-pass, Hilbert transform,
conventions P and C), exactly as for the real data.

**3. Calibration.** μ = 0.2. σ is set by log-scale bisection (16 steps) so that the **mean over worlds of the number of
recession years in 1970–2022 is 5**, over 500 calibration worlds per setting that are not the test worlds (oscillators
seeded `[5001, setting]`, escape noise `[5002, setting, layer]`, common random numbers across bisection steps). Nothing
in the calibration uses which years are recessions. μ = 0.1 and 0.3 (each with its own σ) are sensitivities.

**4. Reset and refractory.** At an escape (x reaches 0 from below) the state is reset at once to the lower equilibrium
of μ. A year with an escape is a recession year unless a recession year was counted in the previous **2** calendar
years (escapes then still reset the state but are not counted). Refractory periods of **0 and 4** years are
sensitivities.

**5. Worlds.** Kuramoto only, on the saved G1 network (`gnn/G1/trade_network.npz`) with the G1 calibration. Three
settings, the **identical G1 worlds** (seed `[2001, 0, cell]`, simulated in chunks of 250 from the same generator, so
world k of G1b is world k of G1): **trade-coupled κ\*** (primary; G1 cell `network`), **no coupling** (cell `null`) and
**common forcing φ\*** (cell `forcing`), 1,000 worlds each. The layer is integrated alongside the oscillators from 1950
(state starting at the lower equilibrium), with its own independent noise (seed `[6001, setting, layer]`); it does not
feed back on the oscillators. Only escapes in 1970–2022 date recessions.

**6. Time unit.** 1 model unit = 1 year, justified only because the G1 oscillators are calibrated in years. With
τ years per model unit the layer is dx = (μ + x − x³) dt/τ + g(t) dW_t/√τ (t in years, dt = 0.01). τ = 0.5 and 2 are
sensitivities. **A lead at lag 2 but not at lag 1 does not count as reproducing lead-1.** Every lag is reported.

**7. Verdict — "reproduces the lead" requires all three**, on the primary setting (κ\*, world-level, unweighted r,
μ = 0.2, refractory 2, τ = 1), for the **past-only lead-1** (convention C, circular shifts, upper tail, as in Paper 1):

- (a) the Wilson 95% lower bound of its rejection rate (p ≤ 0.05, which with 53 shifts means p ≤ 2/53) is above
  **3.8%** (2/53, the exact rate with nothing there);
- (b) its rate beats both the **constant-noise** and the **shuffled-synchrony** controls: for each, the 95% interval of
  the paired difference (layer minus control, same worlds, same escape noise) lies above zero;
- (c) at least **20%** of worlds reach p ≤ 0.038 (2/53, the real p).

**Partly** if (a) and (b) hold but not (c); **not reproduced** otherwise. Pass or fail is reported exactly as
pre-registered, for every setting and sensitivity, without changing the thresholds.

**Controls**, each recalibrated to five recession years under the same μ, refractory and τ:

- *Constant noise:* g = σ_c, the same in every world and year.
- *Shuffled synchrony:* each world's own r(t) (or Ā·R_A(t)) with its 73 one-year blocks of 1950–2022 permuted (seed
  `[6101, setting]`), σ recalibrated.
- *Per-economy sensitivity:* the shuffled control moves the whole vector of phases by the same block permutation; the
  constant control gives every economy noise σ_c(√c dW₀ + √(1 − c) dWᵢ), with c the world's mean over 1950–2022 of
  the pairwise alignment (N r² − 1)/(N − 1) (clipped at 0), so the world-average noise has the world's mean square but
  no timing.
- *The plain G1 world* (rule B, already computed): reference only, not part of (b).

**Sensitivities** run on the primary setting (κ\*) only, each with its own controls and its own verdict: per-economy;
Ā·R_A; μ = 0.1 and 0.3; refractory 0 and 4; τ = 0.5 and 2. The no-coupling and forcing settings run the primary layer
and both controls.

**Reported, for every setting and layer:** the rejection rate with its Wilson interval at every lag of the two-sided
arc (convention P: lead-2, lead-1, crisis, after-1, after-2) and of the past-only arc (convention C, the same five
lags); the full distribution of the past-only lead-1 p over its 53 possible values; the share of worlds at p ≤ 0.038
and the share with a past-only lead-1 correlation of at least +0.379 (the real value); the distribution of recession
years per world and the rates among worlds with 4–6; the mean true and pipeline r in recession years, the year before
and other years (description). The pipeline r(t) of each world is computed once; only the recession dates change
between layers.

**Code and outputs:** `src/ef/gnn/g1b.py` (the layer, calibration and tests), `src/ef/gnn/g1b_report.py` (the
report); results in `gnn/G1b/`, report `gnn/G1b_report.md`. Tests in `tests/test_gnn_g1b.py` check that the G1b
worlds equal the G1 worlds, the escape rule, the refractory rule and the shuffling, before the run.
