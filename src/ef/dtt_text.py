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


# ------------------------------------------------------------------ D3: real data

def d3(res):
    G = ('all years', 'recession years', 'lead-1 years', 'normal years'); S = ('S31', 'S30', 'S26')
    L = ["# D3 — the effective number of economies on real data (descriptive only)", "",
         "Computed by `python -m ef.dtt_real` (`src/ef/dtt_real.py`) from the Paper 1 pipeline: phases and swing sizes from "
         "the analytic signal, 1970–2022, convention P (the paper's) and C (past data only) beside it. **No p-values**: this "
         "describes, it does not test. Years: recessions 1975, 1982, 1991, 2009, 2020; lead-1 the year before each; normal "
         "years are neither recessions nor the downturns 1998, 2001, 2012 (Paper 1's definition).", "",
         "## What is computed", "",
         "- **N_eff = 1 / r²**, the report's effective number (equal swing sizes, the whole shock shared). Over a group of "
         "years it is summarized the report's way, **1 / E[r²]**, the variance-equivalent count. The arithmetic mean of the "
         "yearly 1/r² is not used: in years with r near 0 it explodes (it is "
         f"{res['S31']['P']['all years']['mean_of_yearly_neff_unstable']:.0f} for S31 over all years). Medians of the yearly "
         "values are given beside.",
         "- **1 / R_A²**, the amplitude-weighted version Sid asked for (1 / E[R_A²] over a group).",
         "- **mean(A²) / |Z_A|²** (E[mean A²] / E[|Z_A|²] over a group), the count the variance law implies exactly when swing "
         "sizes differ. It equals (1 + CV_A²) / R_A², so it is 1/R_A² scaled up by the spread of swing sizes; with equal "
         "swing sizes the three coincide.", "",
         "**Sid's cross-check (S26, convention P):** about 2.9 on average, 2.1 in recession years, 1.9 at lead-1, 1.04 in "
         f"2020. Computed: {res['S26']['P']['all years']['neff']:.2f}, {res['S26']['P']['recession years']['neff']:.2f}, "
         f"{res['S26']['P']['lead-1 years']['neff']:.2f} and {res['S26']['P']['by_year']['2020' if '2020' in res['S26']['P']['by_year'] else 2020]['neff']:.3f} "
         "— a match, with N_eff over a group taken as 1 / E[r²].", "",
         "## N_eff = 1 / E[r²] by group (median of the yearly values in brackets)", "",
         "| Sample | Convention | " + " | ".join(G) + " | 2020 |", "|---|---|" + "---|" * (len(G) + 1)]
    by = lambda s, c, y: res[s][c]['by_year'][str(y)] if str(y) in res[s][c]['by_year'] else res[s][c]['by_year'][y]
    for s in S:
        for c in ('P', 'C'):
            x = res[s][c]
            L.append(f"| {s} (N = {res[s]['N']}) | {c} | " + " | ".join(f"{x[g]['neff']:.2f} ({x[g]['median_neff']:.2f})" for g in G)
                     + f" | {by(s, c, 2020)['neff']:.2f} |")
    L += ["", "## Amplitude-weighted: 1 / E[R_A²], and the exact count E[mean A²] / E[|Z_A|²]", "",
          "| Sample | Convention | " + " | ".join(G) + " |", "|---|---|" + "---|" * len(G)]
    for s in S:
        for c in ('P', 'C'):
            x = res[s][c]
            L.append(f"| {s} | {c} | " + " | ".join(f"{x[g]['inv_RA2']:.2f} / {x[g]['neffA']:.2f}" for g in G) + " |")
    L += ["", "## Each recession year (S31)", "", "| Year | N_eff, P | N_eff, C | the year before, P | the year before, C |", "|---|---|---|---|---|"]
    for y in (1975, 1982, 1991, 2009, 2020):
        L.append(f"| {y} | {by('S31', 'P', y)['neff']:.2f} | {by('S31', 'C', y)['neff']:.2f} | {by('S31', 'P', y - 1)['neff']:.2f} | {by('S31', 'C', y - 1)['neff']:.2f} |")
    x = res['S31']['P']
    L += ["", "**Reading.** On the 31 economies the world behaves, by this measure, like about "
          f"{x['all years']['neff']:.1f} independent economies on average, {x['recession years']['neff']:.1f} in recession years "
          f"and {x['lead-1 years']['neff']:.1f} the year before, against {x['normal years']['neff']:.1f} in normal years (convention P). "
          "The group values are pulled down by 2009 and 2020, when N_eff is close to 1; 1975, 1982 and 1991 are not low, and "
          "the median recession year is not below the median year. With past-only phases (C) the gap between normal years "
          f"({res['S31']['C']['normal years']['neff']:.1f}) and recession and lead-1 years ({res['S31']['C']['recession years']['neff']:.1f}, "
          f"{res['S31']['C']['lead-1 years']['neff']:.1f}) is wider. Like every Paper 1 result on the lead, it rests on 2009 and 2020.", "",
          "## N_eff and the variance decomposition's co-movement share", "",
          "**Exact, instantaneous.** With equal weights and equal swing sizes, the variance law splits world variance into an "
          "own part 1/(2N) and the rest, so the co-movement (cross) share of world variance is exactly 1 − N_eff/N "
          f"(checked on S31: largest error {res['S31']['decomposition']['identity_equal_swings']:.1e}). With weights wᵢ and "
          "swing sizes Aᵢ it is 1 − Σwᵢ²Aᵢ² / |Σwᵢ Aᵢ e^{iθᵢ}|².",
          "",
          "**Over the decomposition's windows, close but not exact.** The decomposition (Methods 6.1) measures variance over "
          "10-year windows in time, not over shock directions. The two coincide only when, inside a window, swing sizes and "
          "phase gaps are fixed and the common phase turns through whole cycles. On the real windows (Phase 3 settings, "
          "1962–2022), the variance law averaged over each window against the decomposition itself:", "",
          "| Sample | Weights | World variance, law ÷ actual (median) | Own variance, law ÷ actual (median) | Cross share: correlation across windows; mean gap | Cross share of the recession excess: actual / law |",
          "|---|---|---|---|---|---|"]
    for s in S:
        for k, v in res[s]['decomposition'].items():
            if not isinstance(v, dict): continue
            L.append(f"| {s} | {'GDP (window mean)' if k == 'gdp_mean' else 'equal'} | {v['tot_ratio_median']:.3f} | {v['own_ratio_median']:.3f} | "
                     f"{v['cross_share_corr']:.3f}; {100 * v['cross_share_mean_abs_gap']:.1f} points | {100 * v['excess_from_cross']:.1f}% / {100 * v['excess_from_cross_law']:.1f}% |")
    d = res['S31']['decomposition']['gdp_mean']
    L += ["", f"So the decomposition's headline — the cross term supplies {100 * d['excess_from_cross']:.1f}% of the extra world "
          f"variance in recession windows on S31 (GDP weights) — is, to within a point ({100 * d['excess_from_cross_law']:.1f}% from the law), "
          "what the variance law gives when it is averaged over the same windows. That share is not a function of N_eff alone: "
          "it is ΔCROSS / (ΔOWN + ΔCROSS) between recession and normal windows, and own variances (swing sizes) rise in "
          "recessions too. What N_eff adds is the reading: a cross share of world variance of c means, with equal weights and swing sizes, the world varies like "
          "N(1 − c) independent economies of equal size."]
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------ D2: robustness

def _ci(d, scale=100, digits=1): return f"{scale * d['diff']:+.{digits}f} [{scale * d['lo']:+.{digits}f}, {scale * d['hi']:+.{digits}f}]"


def _r(x): return f"{100 * x['p']:.1f}"


def _vanish(d): return d['lo'] <= 0 <= d['hi']


def write_d2():
    import json
    import os
    from ef import config
    R = os.path.join(config.repo_root(), 'dtt', 'results'); L_ = lambda f: json.load(open(os.path.join(R, f)))
    conv, abl, rho, sw, fd = L_('d2_convergence.json'), L_('d2_ablation.json'), L_('d2_rho.json'), L_('d2_sweeps.json'), L_('figdata_C3_F1.json')
    A = {round(a['K'], 3): a for a in abl}; base = A[0.0]
    mid = [r for r in sw if 0.02 < r['instantaneous']['p'] < 0.98]         # conditions where tipping is neither rare nor certain
    tv_pos = [r for r in sw if r['inst_minus_rms']['lo'] > 0]; tv_van = [r for r in sw if _vanish(r['inst_minus_rms'])]
    tv_neg = [r for r in sw if r['inst_minus_rms']['hi'] < 0]
    ord_pos = [r for r in sw if r['inst_minus_block']['lo'] > 0]; ord_van = [r for r in sw if _vanish(r['inst_minus_block'])]
    mid_van = [r for r in mid if _vanish(r['inst_minus_rms'])]
    lab = {'D': 'D', 'omega_sd': 'ω s.d.', 'N': 'N', 'mu': 'μ', 'sigma': 'σ', 'T': 'T'}
    cond = lambda r: f"{lab[r['param']]} = {r['value']:g}, K = {r['K']:.3g}"
    t08, t13 = A[0.8]['timing'], A[1.333]['timing']

    def lead_time(t):
        b, c, lags = np.array(t['R_before']), np.array(t['R_alive_same_time']), np.array(t['lags'])
        base_gap = (b - c)[lags >= 8].mean(); far = [l for l, x, y in zip(lags, b, c) if (x - y) > base_gap + 0.5 * ((b - c)[0] - base_gap)]
        return max(far) if far else 0.0
    L = ["# D2 — robustness of the DTT escape model (simulation only)", "",
         "Runs the plan committed before any D2 run (`dtt/D2_plan.md`, commit a4d6e36): Sid's recommended next simulation "
         "sequence plus a timing item. Code `src/ef/dtt_d2.py` and `src/ef/dtt.py`, seed 1310; `python -m ef.dtt_d2 run | rho | "
         "figures | report` (about 15 minutes on this Mac with 8 processes). Every number below is read from `dtt/results/d2_*.json`. "
         "One correction during the run: the constant-RMS control ignored ρ in the ρ sweep (it used σ√E[R²] for every ρ); "
         "fixed to each trial's RMS of its own ρ-weighted noise and the ρ sweep rerun (`rho` step). Nothing else used ρ < 1, "
         "and the reproduction (D0) is unchanged to every digit.", "",
         "Base: N = 31, ω ~ Normal(0, 1), D = 0.02, μ = 0.2, σ = 0.82, T = 40, step 0.01, uniform phases at t = 0. Uncertainty: "
         "Wilson 95% intervals for rates; paired 95% intervals for differences between noise formulations on the same R(t) "
         "traces and Brownian increments. An effect *vanishes* where its interval contains 0.", "",
         "## In short", "",
         f"- **Numerically sound.** The four step sizes agree to within about a point; the report's step (0.01) is at most "
         f"{max(abs(100 * c['by_dt']['0.01']['gap_to_finest']['instantaneous']['diff']) for c in conv):.1f} points from the finest (0.0025).",
         f"- **Coupling, measured within the model** (K against K = 0, same noise rule): tipping rises with K in "
         f"{sum(1 for r in sw if r['K'] > 0 and r['coupling_effect']['lo'] > 0)} of {sum(1 for r in sw if r['K'] > 0)} swept conditions. "
         "This is the fair measure of coupling, but most of it is built in: the noise is σR(t) by assumption, R rises with K, "
         "and escape rises with noise.",
         f"- **The report's 4.75% against 0.325% is not a coupling effect.** At K = 0, σR(t) tips in {_r(base['instantaneous'])}% "
         f"of paths against {100 * base['independent']['p']:.2f}% with independent noise, although the two have the same mean square noise "
         f"(E[R²] = 1/N exactly). With each path's constant RMS it is {_r(base['rms_trial'])}%. The gap comes from R(t) "
         f"fluctuating, and from its persistence: shuffling R in 1-unit blocks keeps most of it ({_r(base['block_permuted'])}%), "
         f"shuffling step by step removes it ({_r(base['permuted'])}%). The ρ sweep shows it enters only through the shared "
         f"part of the shock (K = 0: {100 * rho[0]['rows'][0]['instantaneous']['p']:.1f}% at ρ = 0 to "
         f"{100 * rho[0]['rows'][-1]['instantaneous']['p']:.1f}% at ρ = 1, constant RMS flat).",
         f"- **Time variation (σR(t) against each path's constant RMS) mostly survives.** Positive in {len(tv_pos)} of {len(sw)} swept "
         f"conditions, vanishing in {len(tv_van)}, significantly negative in {len(tv_neg)}. Where tipping is neither rare nor "
         f"certain (between 2% and 98%; {len(mid)} conditions) it vanishes in {len(mid_van)}"
         + (": " + "; ".join(cond(r) for r in mid_van) if mid_van else "") + ". Its size: up to "
         f"{100 * max(r['inst_minus_rms']['diff'] for r in sw):.0f} points; it shrinks to nothing as tipping saturates (K ≥ 1.87 at the "
         "base, large σ, μ = 0.3).",
         f"- **But 'time-varying R tips more' is not general.** Against the *ensemble* RMS (every path given the same average "
         f"noise), σR(t) tips less at K ≥ 1.33 ({_r(A[1.333]['instantaneous'])}% against {_r(A[1.333]['rms_ensemble'])}% at K = 1.333): "
         "spreading noise unevenly across paths helps when escape is unlikely and hurts when it is likely. The report's 32.9% "
         "against 20% (K = 0.8) is the first regime.",
         f"- **Order in time matters less.** σR(t) against R(t) shuffled in 1-unit blocks: positive in {len(ord_pos)} of {len(sw)} "
         f"conditions, vanishing in {len(ord_van)}; at most {100 * max(r['inst_minus_block']['diff'] for r in sw):.0f} points.",
         f"- **Timing.** R rises over the last few model time units before an escape: at K = 0.8 it is "
         f"{t08['R_before'][8]:.2f} four units before, {t08['R_before'][4]:.2f} two units before and {t08['R_before'][0]:.2f} at passage, "
         f"against {t08['R_alive_same_time'][0]:.2f} in paths not yet tipped; the rise is more than half done about "
         f"{lead_time(t08):.1f} units before passage (K = 1.333: {lead_time(t13):.1f}), a little longer than R's autocorrelation "
         f"time ({t08['autocorr_time']:.1f} and {t13['autocorr_time']:.1f} units). This is built in — the noise is "
         "largest when R is — and it is in model time; whether a lead of this kind survives annual sampling and the Paper 1 "
         "pipeline is the G1b question.", "",
         "## 1. Convergence (common random numbers, 1,000 paths per K)", "",
         "| K | dt | Tipping, σR(t) | Each path's RMS | Independent | Mean R | σR(t): gap to dt = 0.0025 |", "|---|---|---|---|---|---|---|"]
    for c in conv:
        for d, v in c['by_dt'].items():
            gap = _ci(v['gap_to_finest']['instantaneous']) if 'gap_to_finest' in v else '—'
            L.append(f"| {c['K']:.3g} | {d} | {_r(v['instantaneous'])}% | {_r(v['rms_trial'])}% | {_r(v['independent'])}% | {v['mean_R']:.3f} | {gap} |")
    L += ["", "## 2. Mechanism ablation on the same R(t) traces (4,000 paths per K)", "",
          "| K | Mean R | σR(t) | Each path's RMS | Ensemble RMS | Step-permuted | Block-permuted (1 unit) | Independent | σR(t) − path RMS | σR(t) − block-permuted |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for a in abl:
        v = a['vs_instantaneous']
        L.append(f"| {a['K']:.3g} | {a['mean_R']:.3f} | {_r(a['instantaneous'])}% | {_r(a['rms_trial'])}% | {_r(a['rms_ensemble'])}% | "
                 f"{_r(a['permuted'])}% | {_r(a['block_permuted'])}% | {_r(a['independent'])}% | {_ci(v['rms_trial'])} | {_ci(v['block_permuted'])} |")
    L += ["", "## 3. Shared fraction ρ (2,000 paths per K, same traces for every ρ)", "",
          "Tipping with g = σ√(ρR(t)² + (1 − ρ)/N) / with each path's constant RMS of that g; ρ = 0 is independent noise, ρ = 1 the "
          "report's model.", "", "| ρ | " + " | ".join(f"K = {r['K']:.3g}" for r in rho) + " |", "|---|" + "---|" * len(rho)]
    for i, x in enumerate(rho[0]['rows']):
        L.append(f"| {x['rho']:.1f} | " + " | ".join(f"{_r(r['rows'][i]['instantaneous'])} / {_r(r['rows'][i]['rms_trial'])}" for r in rho) + " |")
    L += ["", "## 4. One-at-a-time sweeps (2,000 paths per condition)", "",
          "Tipping (%) with σR(t), each path's RMS, block-permuted R and independent noise; the time-variation effect (σR(t) − path "
          "RMS) and the coupling effect (K against K = 0 in the same condition), points with 95% intervals.", ""]
    for prm in dict.fromkeys(r['param'] for r in sw):
        L += [f"**{lab[prm]}**", "", "| Value | K | Mean R | σR(t) | Path RMS | Block-perm. | Independent | Time variation | Coupling |", "|---|---|---|---|---|---|---|---|---|"]
        for r in [r for r in sw if r['param'] == prm]:
            L.append(f"| {r['value']:g} | {r['K']:.3g} | {r['mean_R']:.2f} | {_r(r['instantaneous'])} | {_r(r['rms_trial'])} | {_r(r['block_permuted'])} | "
                     f"{100 * r['independent']['p']:.2f} | {_ci(r['inst_minus_rms'])} | {_ci(r['coupling_effect'])} |")
        L.append("")
    L += ["## 5. Timing: R before first passage", "",
          "| Time before passage | " + " | ".join(f"K = {a['K']:.3g}: tipping paths / not yet tipped" for a in abl if 'timing' in a) + " |", "|---|---|---|"]
    for i, lag in enumerate(t08['lags']):
        if i % 2: continue
        L.append(f"| {lag:g} | " + " | ".join(f"{a['timing']['R_before'][i]:.3f} / {a['timing']['R_alive_same_time'][i]:.3f}" for a in abl if 'timing' in a) + " |")
    L += ["", f"Paths: {t08['n_tippers']} (K = 0.8) and {t13['n_tippers']} (K = 1.333), at most 500 sampled. At K = 1.333 tipping paths "
          "have higher R even 10 units before (each path draws its own frequencies, so some paths synchronize more throughout); "
          "the rise in the last few units comes on top of that.", "",
          "## 6. Figures", "",
          "Regenerated from this code with the project palette in `dtt/fig/` (Inter is not installed on this Mac; matplotlib "
          "falls back to DejaVu Sans): B1, B2, C2, C3, D1, D2, E1 and F1 — F1 now in steps, from the section F model "
          f"(intermediate {100 * fd['F1']['intermediate (V = 10.7)']['share_by_800']:.1f}% by step 800, median "
          f"{fd['F1']['intermediate (V = 10.7)']['median_steps']:.0f} steps; strong 100%, median {fd['F1']['strong (V = 27.2)']['median_steps']:.0f}) — and one per run "
          "(D2a convergence, D2b ablation, D2c ρ, D2d timing, D2e and D2f sweeps). The report's own figures stay unchanged in "
          "`dtt/legacy/figures_extracted/`.", "",
          "## 7. What survives, plainly", "",
          "- The variance law (section A) is exact and is the informative core; it needs no simulation.",
          "- 'More synchrony → more tipping' survives everywhere it can, but it is built in and says little.",
          "- The time-variation effect (section E) survives in most conditions where tipping is neither rare nor certain, and is "
          "driven by persistent episodes of high R; it reverses against an ensemble-average control at high tipping rates.",
          "- The section D comparison (4.75% against 0.325%) measures R fluctuating, not coupling.",
          "- Synchrony leads escape in model time by a few units, by construction. The open question is the G1b one."]
    p = os.path.join(config.repo_root(), 'dtt', 'D2_report.md'); open(p, 'w').write("\n".join(L) + "\n"); print('wrote dtt/D2_report.md')


import numpy as np  # noqa: E402  (used by write_d2)
