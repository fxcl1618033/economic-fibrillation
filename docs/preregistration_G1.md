# Pre-registration — G1, simulated worlds with known coupling

Written 13 October 2026 on Sid's instruction of the same day, before the simulator is calibrated and before any Paper 1
test is run on a simulated world (`CLAUDE.md` rule 3). The only runs so far were engineering checks: three simulated
worlds pushed through the test code to time it, with no p-value looked at. Code: `src/ef/gnn/simulator.py` (the
worlds) and `src/ef/gnn/g1.py` (calibration and test runs), committed with this file. Any later change is added as a
dated amendment at the end, and results obtained before it are kept.

## Purpose

1. **The κ = 0 check.** How often do Paper 1's tests reject when the economies are not coupled at all?
2. **Known coupling.** When the coupling is known, what do the pipeline's r(t) and the tests show?

## The worlds

Two models (`HANDOFF.md` §7, G1), 31 economies (S31) and a world node that forces every economy equally:

- **Kuramoto** (phase only): dθᵢ = [ωᵢ + κ Σⱼ Wᵢⱼ(t) sin(θⱼ − θᵢ) + φ sin(θ_W − θᵢ)] dt + σ dBᵢ; the world node
  dθ_W = ω_W dt + σ dB_W. Cycle: Aᵢ cos θᵢ.
- **Stuart–Landau** (phase and swing size): dzᵢ = [(μ + iωᵢ) zᵢ − |zᵢ|² zᵢ + κ Σⱼ Wᵢⱼ(t)(zⱼ − zᵢ) + φ (z_W − zᵢ)] dt
  + σ (dBᵢ + i dB′ᵢ); the world node is an uncoupled Stuart–Landau oscillator with the same μ and σ. Cycle: Aᵢ Re zᵢ / m.

Fixed inputs, all from real S31 data:

- **Network W(t):** the G0 trade network, goods exports of j to i as a share of i's GDP (the primary weight fixed by
  Sid), the mean of the exporter's and the importer's reports where both exist, the matrix of each year; years before
  1970 use 1970's. A masked weight is no link (0): Russia has no links before 1992, and Brazil receives none before
  1989 (its GDP denominator is masked). κ and φ are the known couplings.
- **Intrinsic frequencies ωᵢ:** each economy's observed mean frequency (S31, convention P, 1970–2022; mean period 6.0
  years, range 4.8–8.0). ω_W = the mean of the ωᵢ. Observed frequencies are already pulled together by whatever
  coupling the real world has, so the intrinsic spread may be understated.
- **Swing sizes Aᵢ:** each economy's observed mean amplitude. **Trend:** each economy's linear trend in log GDP per
  capita, 1950–2022. **Population:** Maddison's, for GDP levels and weights.
- **Integration:** Euler–Maruyama, dt = 0.01 years, from 1850 (a 100-year burn-in with 1970's network) to 2022. Log GDP
  per capita of year y = trend + the mean of the cycle over year y (GDP is a flow). The years 1950–2022 go through
  the Paper 1 pipeline exactly as the real data do (band-pass, Hilbert transform, convention P; `ef.paper1`).
- **Not included:** slow forcing ramps (optional in `HANDOFF.md`; later, for rate-induced tipping).

## Calibration (before any test; never on the recession years)

Targets, real S31 under convention P, 1970–2022: the median over economies of the standard deviation of annual phase
steps (0.996 radians), the median coefficient of variation of the swing size (0.659), and the mean of r(t) (0.484).

1. At κ = φ = 0, the noise σ (Kuramoto) or the pair (μ, σ) (Stuart–Landau) is the grid point whose pipeline phases come
   closest to the target phase-step spread (Kuramoto) or to both targets (Stuart–Landau; the sum of squared relative
   errors). Grids: σ = 25 values spaced evenly in log from 0.05 to 5; μ ∈ {−1, −0.5, −0.25, 0, 0.25, 0.5, 1}.
2. m = the mean size of the uncoupled annual signal, so that coupling can change swing sizes.
3. **κ\*** (with φ = 0) and **φ\*** (with κ = 0): the values whose mean r over 1970–2022 matches the real 0.484, by
   bisection on a log scale between 0.001 and 1000 (16 steps).

Each evaluation uses 200 worlds with the same random numbers (seed 1001). Expected limits, stated now: in the Kuramoto
model swing sizes vary only through noise and filtering; a Stuart–Landau world driven by Gaussian noise may not reach a
swing-size variation of 0.66 (narrow-band Gaussian noise gives about 0.52). If a target is out of reach, the closest
grid point is used and the gap is reported.

## Settings run (per model, 1,000 worlds each)

| Setting | κ | φ | What it is |
|---|---|---|---|
| null | 0 | 0 | **the κ = 0 check**: no coupling at all |
| forcing | 0 | φ\* | a common shock only, no links between economies |
| network_half | κ\*/2 | 0 | trade links at half strength |
| network | κ\* | 0 | trade links strong enough to match the real mean r |

Seeds: worlds from (2001, model, setting); surrogates per world and test from 3001. Also `r_curve.csv`: mean r (and by
decade) for κ and φ at 0, ⅛, ¼, ½, 1, 2 and 4 times κ\* and φ\* (200 worlds each), against the real values.

## Recession dates

- **Rule A:** the real dates 1975, 1982, 1991, 2009 and 2020. They have nothing to do with a simulated world.
- **Rule B:** each world's own, dated the way Kose, Sugawara and Terrones date global recessions from world GDP per
  capita: the five years of lowest growth of the 31's total real GDP per capita in 1970–2022, lowest first, each at
  least 5 years from any year already taken. The next three are that world's downturns (description only).

## Tests

Every Paper 1 test in `ef.paper1` with the S31 Phase 3 settings (`configs/runs/phase3_s31.yaml`; convention P;
rolling windows from 1962; the pre-registered directions), with three changes for speed: 199 surrogates per surrogate
test instead of 5,000 (p floor 0.005); convention C only among the alternative conventions (the past-only lead check);
200 bootstrap draws for the arc's descriptive intervals. Robustness variants and the cross-term split are not run.
Twenty p-values per world:

- arc of r(t) against the recession years: lead-2, lead-1, crisis (upper tail), after-1, after-2 (lower tail);
  circular shifts;
- arc under past-only phases (convention C): lead-2, lead-1;
- r against swing size: circular shifts and surrogates (no recession dates);
- diversification, the cross term's share at recessions: GDP-weighted and equal weights; surrogates;
- fibrillation identity: alignment and swing size at recessions; surrogates;
- MST: pre-crisis contraction (raw and detrended) and fragility; surrogates;
- phase leads: spread smaller than surrogates (no recession dates);
- critical slowing down: pre-crisis trends in the lag-1 autocorrelation and the variance of r; surrogates;
- bifurcation: slower recovery after recessions; surrogates.

**Rejection:** p ≤ 0.05. **Exact rate** (what a test that is right under no coupling rejects): 2/53 = 3.8% for the
circular-shift tests (below 0.05, p can only be 1/53 or 2/53) and 10/200 = 5.0% for the surrogate tests. Each
rejection rate is reported with its 95% Wilson interval, per model, setting and rule; with 1,000 worlds the interval
around 5% is about 3.8–6.5%. Also the family rates: any of the five arc lags, and any of lead-2, lead-1 and crisis.

## Hypotheses, stated before running

- **H1, size (null, rule A).** Every test rejects at about its exact rate. A test **passes** if its 95% interval
  contains its exact rate, and **over-rejects** if the interval lies above it. This is the G1 gate in `gnn/README.md`
  ("κ = 0 gives about 5% false positives on the Paper 1 tests").
- **H2, selection (null, rule B).** The arc test at the crisis year and at lead-1 rejects **more** often than its
  exact rate. Reason: the years in which world output falls most are years in which many economies happen to be in a
  downswing together, which is when their phases are aligned. If so, part of Paper 1's arc result could come from how
  global recessions are dated, with no coupling at all, and the paper needs to say so. The identity's alignment term
  and the diversification cross term are expected to over-reject for the same reason.
- **H3, known coupling.** Mean r rises with κ and with φ. Under rule A the date-based tests stay near their exact rate
  at every coupling, because the dates are unrelated to the worlds; under rule B their rejection rates at κ\* exceed
  those at κ = 0.
- **H4, exploratory.** Forcing-only and network worlds matched to the same mean r give similar rejection rates. If so,
  Paper 1's tests cannot tell transmission through trade links from a common shock.

## Outputs

`gnn/G1/calibration.json`, `r_curve.csv`, `pvalues.csv.gz` (every p-value of every world), `rule_b_recessions.csv.gz`,
`rejections.csv`, and the report `gnn/G1_report.md`; `make gnn-g1` reruns everything.
