# Pre-registration — G1b, a synchrony-driven escape layer on the G1 worlds

Written 14 October 2026. **Status: draft for Sid's choices; nothing has been run.** The choices marked
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
