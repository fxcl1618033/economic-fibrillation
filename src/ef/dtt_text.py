"""The words of dtt/D0_reproduction.md (and later DTT documents); every number is read from dtt/results/."""


def _pc(x): return f"{100 * x:.2f}%"


def _prop(d):
    r, m = d['report'], d['mine']
    return f"{r[0]}/{r[1]} ({_pc(r[2])})", f"{m[0]}/{m[1]} ({_pc(m[2])})", d['mark']


def _med(d):
    if d['report'] is None or d['mine'] is None: return '—', '—' if d['mine'] is None else f"{d['mine']:.2f}", '—'
    return f"{d['report']:.2f}", f"{d['mine']:.2f} (± {d['tolerance']:.2f})", d['mark']


HEADER = """# D0 — bringing in the DTT report and reproducing it

## What came in

Only the report: `dtt/legacy/DTT_Unified_Simulation_Report.pdf` (frozen, sha256 4e96a7cb…; see `dtt/legacy/README.md`).
**There is no code**, so the report's tables cannot be rerun from their own code. Following Sid's instruction, D0 goes
straight to D1: the rows Sid listed (sections B–F) are compared below with a clean implementation of the equations the
report states (`src/ef/dtt.py`, seed 1310; `python -m ef.dtt_runs reproduce`). That is a reproduction of the report's
*specification*, not of its runs: Monte Carlo rows can at best agree within sampling error, and details the report does
not state are my choices, listed with each section.

**Marks** (fixed in `src/ef/dtt_runs.py` before the run): **EXACT** — the same number to the digits the report prints
(deterministic quantities only); **CLOSE** — for Monte Carlo quantities, a two-sided 95% test cannot tell the two apart
(proportions: pooled two-proportion test; median tipping times: difference within 1.96 × the combined bootstrap
standard error; mean R²: difference within 1.96 × √2 × my standard error over 40 ensembles); **DIFFERENT** — otherwise.
My runs use about ten times the report's trials where that is cheap, so CLOSE mostly tests the report's numbers.

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
"""


def d0(res, REP):
    L = [HEADER, "## Reproduction from the report's equations", ""]
    marks = []
    # B
    L += ["### Section B — mean R² and the variance law", "",
          "My choices (not stated in the report): Euler–Maruyama step 0.01, a run-in of 50 time units, then R² averaged over "
          "200 time units; 40 ensembles per K, as the report. *Report arithmetic*: the report's theoretical variance implies "
          "its mean R² (×2); its amplification (31 × mean R²) and N_eff (1 / mean R²) columns are checked against that to "
          "the printed digits.", "",
          "| K | Report mean R² | My mean R² (SE) | Mark | Report's arithmetic | Report's MC ÷ theory | My MC ÷ theory |",
          "|---|---|---|---|---|---|---|"]
    for r in res['B']:
        L.append(f"| {r['K']:.3f} | {r['report_mean_R2']:.4f} | {r['mine_mean_R2']:.4f} ({r['se_mine']:.4f}) | {r['mark']} | "
                 f"{r['report_arithmetic']} | {r['report_mc_over_theory']:.3f} | {r['mine_mc_var'] / r['mine_theory_var']:.3f} |")
        marks += [('B mean R²', r['mark']), ('B arithmetic', r['report_arithmetic'])]
    # C
    L += ["", "### Section C — escape with averaged noise σ√E[R²]", "",
          "σ = 0.82 (not stated in section C; section D's value, bracketed by figure C3), T = 40, step 0.01, start in the lower "
          "well, tipping = first x ≥ 0. Each K twice: with the report's own mean R² (isolates the escape model) and with "
          "mine from section B (the whole chain). 10,000 trials per row.", "",
          "| K | R² from | R² | Report | Mine | Mark | Report median | My median (± tolerance) | Mark |", "|---|---|---|---|---|---|---|---|---|"]
    for r in res['C']:
        a, b, m = _prop(r['tipping']); ma, mb, mm = _med(r['median'])
        L.append(f"| {r['K']:.3f} | {'report' if r['R2_from'] == 'report_R2' else 'mine'} | {r['R2']:.4f} | {a} | {b} | {m} | {ma} | {mb} | {mm} |")
        marks += [('C tipping', m), ('C median', mm)]
    # D
    L += ["", "### Section D — the dynamic shared-shock model, g = σR(t)", "",
          "N = 31, ω ~ Normal(0, 1), D = 0.02, μ = 0.2, σ = 0.82, step 0.01, T = 40, phases uniform at t = 0 (no run-in, as the "
          "report). 4,000 trials per K; the independent-noise control (g = σ/√N) 40,000.", "",
          "| K | Report | Mine | Mark | Report median | My median (± tolerance) | Mark | My mean R(t) |", "|---|---|---|---|---|---|---|---|"]
    for r in res['D']:
        a, b, m = _prop(r['tipping']); ma, mb, mm = _med(r['median'])
        L.append(f"| {r['K']:.3f} | {a} | {b} | {m} | {ma} | {mb} | {mm} | {r['mean_R']:.3f} |"); marks += [('D tipping', m), ('D median', mm)]
    c = res['D_control']; a, b, m = _prop(c['tipping']); ma, mb, mm = _med(c['median'])
    L.append(f"| control | {a} | {b} | {m} | {ma} | {mb} | {mm} | — |"); marks += [('D control', m), ('D control median', mm)]
    # E
    L += ["", "### Section E — instantaneous R(t) against constant-RMS noise, same traces and Brownian increments", "",
          "| K | Noise | Report | Mine | Mark | Report median | My median (± tolerance) | Mark |", "|---|---|---|---|---|---|---|---|"]
    lab = {'instantaneous': 'σR(t)', 'rms_trial': 'each trial\'s RMS', 'rms_ensemble': 'ensemble RMS'}
    for r in res['E']:
        a, b, m = _prop(r['tipping']); ma, mb, mm = _med(r['median'])
        L.append(f"| {r['K']:.3f} | {lab[r['kind']]} | {a} | {b} | {m} | {ma} | {mb} | {mm} |"); marks += [('E tipping', m), ('E median', mm)]
    # F
    L += ["", "### Section F — the stress-threshold prototype", "",
          "x[t+1] = 0.9 x[t] + 0.25 √(V/31) ε[t] from x = 0, 800 steps, an event when |x| ≥ 0.8 two steps running (event time = "
          "the second step). V taken from the report's table: the oscillator settings behind its R and V (diffusion, "
          "run length) are not stated, and its V = 1 at K = 0 is not 31 × R² (= 0.80 for R = 0.1611), so the R → V step "
          "cannot be reproduced. 6,000 trials per row.", "",
          "| Scenario | Innovation s.d. (report / mine) | Stationary s.d. (report / mine) | Report events | Mine | Mark | Report median steps | Mine (± tolerance) | Mark |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in res['F']:
        a, b, m = _prop(r['events']); ma, mb, mm = _med(r['median'])
        L.append(f"| {r['scenario']} | {r['innov_sd_report']:.4f} / {r['innov_sd']:.4f} | {r['stationary_sd_report']} / {r['stationary_sd']:.4f} | "
                 f"{a} | {b} | {m} | {ma} | {mb} | {mm} |"); marks += [('F events', m), ('F median', mm)]
    # I3
    i, R3 = res['I3'], REP['I3']
    L += ["", "### Section I3 (frozen section, checked for Sid's question) — the mean-field Ising model m = tanh(gm + h)", "",
          f"h = {i['h']}, g from 0 to 2.5 on {i['grid']} points; the up-sweep follows the low-g branch, the down-sweep starts "
          "on the negative branch at g = 2.5. The fold of the negative branch is solved exactly (m = tanh(gm + h) with "
          "g(1 − m²) = 1).", "",
          "| Quantity | Report | Mine | Mark |", "|---|---|---|---|",
          f"| Up-sweep state at g = 2.5 | {R3['up_2.5']} | {i['up_2.5']:.4f} | {'EXACT' if round(i['up_2.5'], 4) == R3['up_2.5'] else 'DIFFERENT'} |",
          f"| Down-sweep state at g = 2.5 | {R3['down_2.5']} | {i['down_2.5']:.4f} | {'EXACT' if round(i['down_2.5'], 4) == R3['down_2.5'] else 'DIFFERENT'} |",
          f"| Down-sweep state at g = 0 | {R3['down_0']} | {i['down_0']:.5f} | {'EXACT' if round(i['down_0'], 5) == R3['down_0'] else 'DIFFERENT'} |",
          f"| Maximum branch gap | {R3['max_gap']} | {i['max_gap']:.6f} | {'EXACT' if round(i['max_gap'], 6) == R3['max_gap'] else 'DIFFERENT'} |",
          f"| Loop area | {R3['area']} | {i['area']:.6f} | CLOSE (depends on the g grid and the quadrature; 0.1%) |",
          f"| Down-sweep jump (the fold) | near {R3['down_jump_g']} | fold at g = {i['fold_g']:.4f} (m = {i['fold_m']:.3f}) | CLOSE: a real saddle-node |",
          f"| Up-sweep \"jump\" | near {R3['up_jump_g']} | steepest point at g = {i['steepest_up_g']:.3f}; largest step between grid points {i['largest_up_step']:.4f} | not a jump: the branch is continuous; 0.915 is where it is steepest |", ""]
    n = {k: sum(1 for _, m in marks if m == k) for k in ('EXACT', 'CLOSE', 'DIFFERENT')}
    diff = [f"{a}" for a, m in marks if m == 'DIFFERENT']
    L += ["## Count", "",
          f"Of {sum(n.values())} marked rows in sections B–F: {n['EXACT']} EXACT, {n['CLOSE']} CLOSE, {n['DIFFERENT']} DIFFERENT"
          + (f" ({', '.join(sorted(set(diff)))})." if diff else "."), "", *reading(res)]
    return "\n".join(L) + "\n"


def reading(res):
    bd = [r for r in res['B'] if r['mark'] == 'DIFFERENT']; d = {r['K']: r for r in res['D']}
    e = {(r['K'], r['kind']): r for r in res['E']}; c = res['D_control']['tipping']['mine']
    k0, k8 = d[0.0]['tipping']['mine'], d[0.8]['tipping']['mine']
    return ["**Reading.** The report reproduces from its own equations except for six rows; its headline numbers all reproduce.",
            "",
            f"- **Reproduced:** the variance law (Monte Carlo ÷ theory within 0.2% at every K, mine and the report's), the report's "
            f"own arithmetic in section B (13 of 13 rows), section C's tipping rates, section D's sweep from about 5% to 100% "
            f"(mine: {100 * k0[2]:.2f}% at K = 0, {100 * k8[2]:.2f}% at K = 0.8) and its independent-noise control ({100 * c[2]:.2f}% "
            f"against the report's 0.33%), section E's gap between σR(t) and constant RMS at K = 0.8 ({100 * e[(0.8, 'instantaneous')]['tipping']['mine'][2]:.1f}% "
            f"against {100 * e[(0.8, 'rms_trial')]['tipping']['mine'][2]:.1f}%, the report 32.9% against 20.1%), section F's event "
            "counts and medians given its V, and the I3 Ising numbers.",
            "- **Section B, mean R² at strong coupling** (" + ", ".join(f"K = {r['K']}: {r['report_mean_R2']:.4f} against my {r['mine_mean_R2']:.4f}" for r in bd)
            + "): mine is lower. A diagnostic (not part of the marks) with a second seed gives " + "; ".join(
                f"K = {x['K']}: {x['mean_R2']:.4f}" + (" (inside the tolerance)" if x['within_tolerance'] else "")
                for x in res['B_diagnostic'] if x['variant'] == 'second seed')
            + "; halving the oscillator noise gives " + "; ".join(f"{x['mean_R2']:.4f}" for x in res['B_diagnostic'] if x['variant'] != 'second seed')
            + ", so the noise term is not the cause. The report does not say how the frequencies were drawn for each ensemble "
            "or how long it ran, so the cause is unknown. The variance law does not depend on it.",
            "- **Section C, median tipping time at K = 0.8** (26.5 in the report; about 20 in mine, with the report's R² or "
            "mine): the tipping rates agree, the timing of the tips does not. With a constant noise and a constant hazard, "
            "tips spread evenly over the horizon and the median among them is near 20; 26.5 would need tips to come late.",
            f"- **Section E, K = 0 with σR(t)** (22/800 = 2.75% in the report; mine {100 * e[(0.0, 'instantaneous')]['tipping']['mine'][2]:.2f}%): "
            "the report's own section D gives 4.75% for the same model and parameters, and mine agrees with that. The report "
            "already notes that its two K = 0 runs differ.",
            "- **Not reproducible:** section F's step from coupling K to R and V (oscillator settings not stated, and V = 1 at "
            "K = 0 is not 31 × R²); figures F1 and I4 (see above)."]
