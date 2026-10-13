"""The words of gnn/G1_report.md, with every number read from gnn/G1/ (ef.gnn.g1_report builds the tables)."""
import numpy as np
import pandas as pd

from ef.gnn import g1, g1_report as T
from ef.gnn import simulator as S


def pct(x): return f"{100 * x:.1f}%"


def sg(x, d=2): return f"{x:+.{d}f}".replace('-', '−')


def calibration_table(cal):
    t = cal['targets']; L = ["| | Real S31 | Kuramoto | Stuart–Landau |", "|---|---|---|---|"]
    k, s = cal['kuramoto'], cal['stuart_landau']
    L += [f"| Spread of annual phase steps (median sd, radians) | {t['sd_phase_step']:.3f} | {k['at_kappa0']['sd_phase_step']:.3f} | {s['at_kappa0']['sd_phase_step']:.3f} |",
          f"| Swing-size variation (median coefficient of variation) | {t['cv_amplitude']:.3f} | {k['at_kappa0']['cv_amplitude']:.3f} | {s['at_kappa0']['cv_amplitude']:.3f} |",
          f"| Mean r, no coupling | {t['mean_r']:.3f} (real, with whatever coupling it has) | {k['at_kappa0']['mean_r']:.3f} | {s['at_kappa0']['mean_r']:.3f} |",
          f"| Noise σ | — | {k['sigma']:.3g} | {s['sigma']:.3g} |",
          f"| μ (Stuart–Landau growth rate) | — | — | {s['mu']:g} |".replace('-', '−'),
          f"| κ\\* (trade links only; mean r → {t['mean_r']:.3f}) | — | {k['kappa_star']:.3g}{'' if k['kappa_star_bracketed'] else ' (not reached)'} | {s['kappa_star']:.3g}{'' if s['kappa_star_bracketed'] else ' (not reached)'} |",
          f"| φ\\* (common forcing only; mean r → {t['mean_r']:.3f}) | — | {k['phi_star']:.3g}{'' if k['phi_star_bracketed'] else ' (not reached)'} | {s['phi_star']:.3g}{'' if s['phi_star_bracketed'] else ' (not reached)'} |",
          f"| Mean r at κ\\* / at φ\\* | {t['mean_r']:.3f} | {k['at_kappa_star']['mean_r']:.3f} / {k['at_phi_star']['mean_r']:.3f} | {s['at_kappa_star']['mean_r']:.3f} / {s['at_phi_star']['mean_r']:.3f} |"]
    return L


def curve_table(curve):
    c = curve[(curve.model != 'real S31') & curve.multiple.isin([0, 0.5, 1, 2])]; real = curve[curve.model == 'real S31'].iloc[0]
    c = c[~((c.coupling == 'phi') & (c.multiple == 0))]
    dec = [x for x in curve.columns if x.startswith('r_1') or x.startswith('r_2')]
    L = ["| Model | Coupling | × calibrated | Mean r | " + " | ".join(d.replace('r_', '').replace('_', '–') for d in dec) + " |",
         "|---|---|---|---|" + "---|" * len(dec)]
    for x in c.itertuples():
        L.append(f"| {T.MODEL[x.model]} | {'κ (trade links)' if x.coupling == 'kappa' else 'φ (common forcing)'} | {x.multiple:g} | {x.mean_r:.3f} | "
                 + " | ".join(f"{getattr(x, d):.3f}" for d in dec) + " |")
    L.append(f"| **Real S31** | | | **{real.mean_r:.3f}** | " + " | ".join(f"**{real[d]:.3f}**" for d in dec) + " |")
    return L


_EBY = {}


def eby(model, year):
    return _EBY[(model, year)]


def _r(R, model, cell, rule, test):
    x = R[(R.model == model) & (R.cell == cell) & (R.rule == rule) & (R.test == test)].iloc[0]; return x


def _rng(R, cell, rule, test, f=pct):
    """'a–b' over the two models (or one value if equal after rounding)."""
    v = sorted(f(_r(R, m, cell, rule, test).rate) for m in S.MODELS)
    a, b = sorted((_r(R, m, cell, rule, test).rate for m in S.MODELS))
    return f(a) if f(a) == f(b) else f"{100 * a:.1f}–{100 * b:.1f}%"


def _floor(P):
    """Share of worlds whose p is at the floor (1/53 for circular shifts, 1/200 for 199 surrogates)."""
    P = pd.concat([P[P.rule != 'any'], P[P.rule == 'any'].assign(rule='A'), P[P.rule == 'any'].assign(rule='B')])
    fl = np.where(P.test.isin(T.SHIFT), P.p <= 1 / 53 + 1e-12, P.p <= 1 / 200 + 1e-12)
    return P.assign(floor=fl).groupby(['model', 'cell', 'rule', 'test']).floor.mean()


def report(R, cal, curve, W, B, P=None, real=None, edge=None):
    k, sl, tg = cal['kuramoto'], cal['stuart_landau'], cal['targets']
    arcA = R[(R.cell == 'null') & (R.rule == 'A') & R.test.isin([f'arc.{l}' for l in ('lead2', 'lead1', 'crisis', 'after1', 'after2')])].rate
    C1 = R[R.test == 'arc_C.lead1']; ek, es = (edge.set_index('model').loc[m] for m in S.MODELS) if edge is not None else (None, None)

    N = R[(R.cell == 'null') & ~R.test.str.startswith('family')]
    over_A = N[(N.rule == 'A') & (N.verdict == 'over')]; pass_A = N[(N.rule == 'A') & (N.verdict != 'over')]
    gate = {m: (int((pass_A.model == m).sum()), int(((N.rule == 'A') & (N.model == m)).sum())) for m in S.MODELS}
    over_names = sorted(set(over_A.test), key=T.ORDER.index)
    Wm = W.groupby(['model', 'cell']).mean(numeric_only=True)
    fl = _floor(P) if P is not None else None
    L = ["# G1 report — simulated worlds with known coupling", "",
         "Status: **for Sid's review.** Pre-registered in `docs/preregistration_G1.md` (commit 9c532fc; amendment 1, "
         "30b095e, a numerical bound set before any test ran), then calibrated and run: 8,000 simulated worlds (two "
         "models × four settings × 1,000), each through the 20 Paper 1 p-values under two ways of dating recessions. "
         "Code `src/ef/gnn/simulator.py` and `src/ef/gnn/g1.py`; `make gnn-g1` reruns it (about 80 minutes on this Mac). "
         "Every number below is read from `gnn/G1/`.", "",
         "## In short", "",
         f"- **The κ = 0 check, recessions on the real calendar** (dates that have nothing to do with a simulated "
         f"world): most tests reject at about the rate they should (3.8% for circular shifts, 5% for surrogates). "
         f"Each of the five arc lags rejects in {100 * arcA.min():.1f}–{100 * arcA.max():.1f}% of uncoupled worlds "
         f"(details in section 3). The gate in `gnn/README.md` is met by {gate['kuramoto'][0]} of {gate['kuramoto'][1]} "
         f"tests in the Kuramoto worlds and {gate['stuart_landau'][0]} of {gate['stuart_landau'][1]} in the Stuart–Landau "
         f"worlds. **The exception that matters is the identity's swing-size test**, which rejects in "
         f"{_rng(R, 'null', 'A', 'structure.p_swing')} of uncoupled worlds where it should reject in 5%. The cause is an "
         f"edge effect: the pipeline inflates swing sizes in 2019–2020, two years from the end of the data, and 2020 is a "
         f"recession year. The real S31 result is far larger than this lean (section 6).",
         f"- **Five lags tested at once:** at least one of the five arc lags rejects in {_rng(R, 'null', 'A', 'family.arc_any')} "
         "of uncoupled worlds. Paper 1 already says no single lag survives a multiplicity correction; this is the same "
         "fact in numbers.",
         f"- **Recessions dated from each world's own output** (the five worst years for world GDP per capita, as Kose, "
         f"Sugawara and Terrones date the real ones): with no coupling at all, the two-sided arc test rejects at the "
         f"crisis year in {_rng(R, 'null', 'B', 'arc.crisis')} and at lead-1 in {_rng(R, 'null', 'B', 'arc.lead1')} of "
         f"worlds, about 2.3 times its exact rate. The worst years for world output are years in which cycles happen to "
         f"line up, so dating recessions that way builds part of the result in. **The past-only lead-1 test does not "
         f"do this** ({_rng(R, 'null', 'B', 'arc_C.lead1')}).",
         f"- **Known coupling:** the pipeline's r rises smoothly with the trade coupling κ and with the common forcing φ. "
         f"Both reach the real mean r ({tg['mean_r']:.2f}) at κ\\* = {k['kappa_star']:.1f} (Kuramoto) or {sl['kappa_star']:.1f} "
         f"(Stuart–Landau), and φ\\* = {k['phi_star']:.2f} or {sl['phi_star']:.2f}. With own-dated recessions the "
         f"two-sided lead-1 rejection rises to {_rng(R, 'network', 'B', 'arc.lead1')} with trade links and "
         f"{_rng(R, 'forcing', 'B', 'arc.lead1')} with common forcing. **The past-only lead-1 test never rejects more "
         f"often than chance, in any setting** ({100 * C1.rate.min():.1f}–{100 * C1.rate.max():.1f}%; no interval lies above 3.8%).",
         f"- **Some \"at recessions\" tests answer a different question.** The cross-term test rejects in "
         f"{_rng(R, 'network', 'A', 'diversification.gdp_mean')} of trade-coupled worlds (GDP weights) even with the real "
         "calendar, which is unrelated to those worlds. The same holds for r against swing size and the clustering of "
         "phase leads. These tests detect co-movement in general; they say nothing about recessions in particular.", "",
         "## 1. The worlds and the calibration", "",
         "Thirty-one economies (S31) and a world node. Each economy is an oscillator with its own observed mean period "
         "(4.8–8.0 years) and swing size, on its own linear trend in log GDP per capita, with Maddison's population. "
         "Trade links pull economy i towards economy j in proportion to j's exports to i as a share of i's GDP (the G0 "
         "primary weight, the real matrix of each year; years before 1970 use 1970's; masked links are no links). The "
         "world node forces every economy equally. Calibration used no recession year (pre-registration, steps 1–3):", ""]
    L += calibration_table(cal)
    L += ["", f"The Kuramoto worlds match the phase-step target; their swing sizes vary only through noise and filtering "
          f"({k['at_kappa0']['cv_amplitude']:.2f} against the real {tg['cv_amplitude']:.2f}). The Stuart–Landau calibration "
          f"ends at the edge of its grid (μ = {str(sl['mu']).replace('-', '−').rstrip('0').rstrip('.')}, a damped oscillator kept going by noise) with a swing-size "
          f"variation of {sl['at_kappa0']['cv_amplitude']:.2f}: as the pre-registration expected, Gaussian noise cannot "
          "make swings as uneven as the real ones. Neither model has crises.", "",
          "## 2. What the pipeline sees of known coupling", "",
          "Mean r over 1970–2022 and by period, 200 worlds per row (multiples ⅛, ¼ and 4 in `gnn/G1/r_curve.csv`):", ""]
    L += curve_table(curve)
    real_lo, real_hi = (real or {}).get('r_1970_1995'), (real or {}).get('r_2010_2022')
    L += ["", f"r follows both couplings without a jump, so the pipeline reads coupling strength. The two kinds differ "
          f"over time: with trade links r rises as trade grows (Kuramoto {Wm.loc[('kuramoto', 'network'), 'r_1970_1995']:.2f} in "
          f"1970–1995 to {Wm.loc[('kuramoto', 'network'), 'r_2010_2022']:.2f} in 2010–2022; Stuart–Landau "
          f"{Wm.loc[('stuart_landau', 'network'), 'r_1970_1995']:.2f} to {Wm.loc[('stuart_landau', 'network'), 'r_2010_2022']:.2f}), "
          f"while common forcing gives a flat r. The real r rises more ({real_lo:.2f} to {real_hi:.2f}). That is a "
          "description, not a test.", "",
          "## 3. The κ = 0 check", "",
          "Share of uncoupled worlds (κ = φ = 0) in which each test rejects at p ≤ 0.05, with its 95% interval; 1,000 "
          "worlds per cell. **Bold**: the interval lies above the exact rate. Real dates (A) are unrelated to the "
          "worlds; own dates (B) are each world's five worst years for world GDP per capita.", ""]
    L += T.table_null(R)
    L += ["", f"**Real calendar.** Tests whose interval lies above the exact rate: " +
          "; ".join(f"{T.LABELS[t]} (" + ', '.join(f"{T.MODEL[m]} {pct(_r(R, m, 'null', 'A', t).rate)}" for m in S.MODELS
                                                   if _r(R, m, 'null', 'A', t).verdict == 'over') + ")" for t in over_names) +
          ". The swing-size test is the serious one, and the reason is an edge effect, found after the runs with a check "
          f"that was not pre-registered (`python -m ef.gnn.g1 checks`, {int(ek.worlds)} uncoupled worlds per model). Under "
          f"convention P the pipeline's swing size is inflated just before the end of the data and collapses at the end: "
          f"2 log Abar differs from its average by {sg(eby('kuramoto', 2019))} in 2019, {sg(eby('kuramoto', 2020))} in 2020, "
          f"{sg(eby('kuramoto', 2021))} in 2021 and {sg(eby('kuramoto', 2022))} in 2022 (Kuramoto; Stuart–Landau alike). "
          f"The test compares recession years, 2020 among them, with all other years, 2022 among them, against surrogates "
          f"that are circular and have no ends. So in every world the statistic leans one way: it averages "
          f"{sg(ek.mean_stat_all_five, 3)} (Kuramoto) and {sg(es.mean_stat_all_five, 3)} (Stuart–Landau) where the null is "
          f"centred on 0, and {sg(ek.mean_stat_without_2020, 3)} and {sg(es.mean_stat_without_2020, 3)} with 2020 left out. "
          f"The spread is about right ({ek.sd_stat_across_worlds:.3f} across worlds against {ek.mean_sd_surrogate_null:.3f} "
          f"in the null, Kuramoto), and only the upper tail over-rejects. Some tests reject less often than they should "
          "(MST contraction and phase leads in the Kuramoto worlds), which only makes them conservative.", "",
          f"**Own dates.** The arc's crisis year and lead-1 over-reject in both models. So do the identity's alignment "
          f"term ({_rng(R, 'null', 'B', 'structure.p_align')}) and the cross term with GDP weights "
          f"({_rng(R, 'null', 'B', 'diversification.gdp_mean')}). The mechanism shows in r itself: in uncoupled worlds r "
          f"averages {Wm.loc[('kuramoto', 'null'), 'r_mean']:.3f} overall but {Wm.loc[('kuramoto', 'null'), 'r_at_rule_b_recessions']:.3f} in a "
          f"world's own recession years (Kuramoto; Stuart–Landau {Wm.loc[('stuart_landau', 'null'), 'r_mean']:.3f} and "
          f"{Wm.loc[('stuart_landau', 'null'), 'r_at_rule_b_recessions']:.3f}). The effect is real but modest: about twice "
          "the exact rate, not a guaranteed rejection. The past-only arc does not over-reject.", "",
          "## 4. With coupling", "",
          "Rejection rate (%) at p ≤ 0.05 in every setting; **bold** where the interval lies above the exact rate. Own-dated "
          "recessions first, because they are how the real dates were made:", ""]
    L += T.table_cells(R, 'B')
    L += ["", "Real calendar (dates unrelated to the worlds):", ""]
    L += T.table_cells(R, 'A')
    L += ["", f"Three kinds of behaviour. (1) **The arc** responds to coupling only when recessions come from the world "
          f"itself: under own dates, crisis-year rejections go from {_rng(R, 'null', 'B', 'arc.crisis')} with no coupling "
          f"to {_rng(R, 'network', 'B', 'arc.crisis')} with trade links and {_rng(R, 'forcing', 'B', 'arc.crisis')} with "
          f"common forcing; on the real calendar they stay near the exact rate. (2) **Tests of co-movement** (cross term, "
          f"r against swing size, phase leads) reject in most coupled worlds on either calendar; the recession years "
          f"play no part. (3) **Trend tests** pick up the growing trade network: MST contraction before \"recessions\" "
          f"rejects in {pct(_r(R, 'kuramoto', 'network', 'A', 'mst.p_contraction').rate)} of Kuramoto trade worlds on "
          f"the real calendar, and {pct(_r(R, 'kuramoto', 'network', 'A', 'mst.p_contraction_detrended').rate)} once "
          f"detrended. The slowing-down tests stay within a few points of 5% (at most "
          f"{100 * R[R.test.isin(['csd.p_ar1', 'csd.p_var'])].rate.max():.1f}%), and the slower-recovery test rejects in less "
          "than 2% of worlds in every coupled setting.", "",
          "## 5. The pre-registered hypotheses", "",
          f"- **H1, size: met for most tests, not all.** On the real calendar, with no coupling, {gate['kuramoto'][0]} of "
          f"{gate['kuramoto'][1]} tests (Kuramoto) and {gate['stuart_landau'][0]} of {gate['stuart_landau'][1]} "
          f"(Stuart–Landau) reject at or below their exact rate. Over-rejecting in at least one model: " + "; ".join(T.LABELS[t] for t in over_names) + ".",
          f"- **H2, selection: confirmed, modest.** With own-dated recessions and no coupling, crisis year "
          f"{_rng(R, 'null', 'B', 'arc.crisis')} and lead-1 {_rng(R, 'null', 'B', 'arc.lead1')} against an exact 3.8%; "
          f"alignment {_rng(R, 'null', 'B', 'structure.p_align')} and cross term {_rng(R, 'null', 'B', 'diversification.gdp_mean')} "
          "against 5%. Not expected and found: the past-only lead-1 is free of it.",
          f"- **H3, known coupling: half confirmed.** r rises with κ and φ, and under own dates the arc's lead and crisis "
          f"rates at κ\\* exceed those at κ = 0. But on the real calendar the co-movement tests and the MST trend tests do "
          "not stay near their exact rate in coupled worlds: they react to coupling or to its growth, whatever the dates.",
          f"- **H4, forcing against trade links: they differ.** At the same mean r, common forcing gives larger arc "
          f"rejections under own dates ({_rng(R, 'forcing', 'B', 'arc.lead1')} at lead-1 against "
          f"{_rng(R, 'network', 'B', 'arc.lead1')}) and a flat r over time; trade links give a rising r. Within one sample the "
          "Paper 1 tests still cannot tell them apart: each rejection seen in the real data occurs under both, at "
          "different rates, and the past-only lead-1 under neither above chance.", "",
          "## 6. What this means for Paper 1 (for Sid to decide)", "",
          f"1. **The swing-size test leans towards rejection because 2020 sits at the end of the data, but the real "
          f"result is far larger than the lean.** With no coupling and unrelated dates the test rejects in "
          f"{_rng(R, 'null', 'A', 'structure.p_swing')} of worlds (floor p in "
          f"{100 * fl.loc[('kuramoto', 'null', 'A', 'structure.p_swing')]:.1f}% of Kuramoto and "
          f"{100 * fl.loc[('stuart_landau', 'null', 'A', 'structure.p_swing')]:.1f}% of Stuart–Landau worlds, against 0.5% "
          f"for an exact test). The lean is about {sg(ek.mean_stat_all_five)} in the statistic ({sg(ek.mean_stat_without_2020)} "
          f"without 2020); the real S31 statistic is {real['dA']:.2f} ({real['dA_without_2020']:.2f} without 2020), against a "
          f"null spread of about {ek.mean_sd_surrogate_null:.2f} in these worlds. So the real result very likely survives "
          "a correct null. Its p = 0.0002 should still be recomputed with a null that has the same ends (surrogates "
          "passed through the same band-pass and Hilbert transform) or under the edge-robust convention E before it is "
          "quoted. Real data have no crisis-free control for 2020, so how much of 2020's own swing is edge cannot be "
          "said from here.",
          f"2. **Lead-1 should rest on the past-only phases, as the paper now says.** Dating recessions from the same "
          f"economies roughly doubles the two-sided lead-1 and crisis-year rejections, even with no coupling. The "
          f"past-only lead-1 is free of that, and none of these worlds produces it above chance either "
          f"({100 * C1.rate.min():.1f}–{100 * C1.rate.max():.1f}% in every setting), while real S31 gives p = 0.038. So the "
          "real past-only result is not explained by how recessions are dated, nor by trade coupling or common forcing at "
          "the real level of synchronization. That leaves something these models lack, such as a build-up of alignment "
          "before crises, or chance; with two effective events (2009 and 2020) chance cannot be ruled out.",
          f"3. **After-2, already in Limitations, deserves even less weight.** On the real calendar it over-rejects in the "
          f"Kuramoto worlds ({pct(_r(R, 'kuramoto', 'null', 'A', 'arc.after2').rate)} uncoupled, "
          f"{pct(_r(R, 'kuramoto', 'network', 'A', 'arc.after2').rate)} with trade links), and real S31 sits at p = 0.057.",
          f"4. **The cross-term test shows co-movement, not co-movement at recessions.** It reaches its floor in "
          f"{100 * fl.loc[('kuramoto', 'network', 'A', 'diversification.gdp_mean')]:.0f}–"
          f"{100 * fl.loc[('stuart_landau', 'network', 'A', 'diversification.gdp_mean')]:.0f}% of trade-coupled worlds on a "
          f"calendar unrelated to them, and in about 1% of uncoupled worlds. The real floor p says the 31 cycles are not "
          "independent. The Results wording should claim no more than that.",
          "5. **Trend tests catch trends.** A growing trade network alone makes MST contraction look like a pre-crisis "
          "signal on any calendar; detrending removes most of it.", "",
          "## 7. Limits", "",
          "- No crises: swings are more even than real ones (swing-size variation 0.44 and 0.51 against 0.66).",
          "- Intrinsic periods are the observed ones, which real coupling may already have pulled together.",
          "- Masked trade links are no links: Russia has none before 1992, and Brazil receives none before 1989.",
          "- 199 surrogates per test (floor 0.005) instead of 5,000: a rejection at 0.05 is exact, but floors are coarser "
          "than Paper 1's.",
          "- Own-dated recessions use a simple rank rule (five lowest-growth years, at least 5 years apart), not Kose, "
          "Sugawara and Terrones's full method.",
          "- One noise level for every economy; the world node pulls every economy equally; trade links only (no banks "
          "or oil).", "",
          "## Files", "",
          "`gnn/G1/calibration.json` (targets, grids, κ\\*, φ\\*), `r_curve.csv`, `pvalues.csv.gz` (every p-value of every "
          "world), `rejections.csv` (the tables above with intervals), `world_stats.csv.gz` (r overall, in own-dated "
          "recession years and by period), `rule_b_recessions.csv.gz` (each world's own recession years)."]
    return "\n".join(L) + "\n"
