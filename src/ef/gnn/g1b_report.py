"""gnn/G1b_report.md and gnn/G1_closing.md from the files in gnn/G1b/ and gnn/G1/. Every number is read from those files."""
import json
import os

import numpy as np
import pandas as pd

from ef import config
from ef.gnn import g1, g1b

ROOT = config.repo_root()
SETTING = {'network': 'trade-coupled (κ\\*)', 'null': 'no coupling', 'forcing': 'common forcing only (φ\\*)'}
SHORT = {'primary': 'primary', 'per_economy': 'one state per economy', 'weighted': 'noise from Ā·R_A', 'mu0.1': 'μ = 0.1',
         'mu0.3': 'μ = 0.3', 'refractory0': 'no refractory period', 'refractory4': 'refractory 4 years', 'tau0.5': '1 unit = 0.5 years',
         'tau2': '1 unit = 2 years'}
VARIANT = {'primary': 'Primary: world-level state, unweighted r, μ = 0.2, refractory 2 years, 1 unit = 1 year',
           'per_economy': 'One state per economy (recession when ≥ 50% escape)', 'weighted': 'Noise from Ā·R_A instead of r',
           'mu0.1': 'μ = 0.1', 'mu0.3': 'μ = 0.3', 'refractory0': 'No refractory period', 'refractory4': 'Refractory 4 years',
           'tau0.5': '1 model unit = 0.5 years', 'tau2': '1 model unit = 2 years'}
LAG = {'lead2': 'lead-2', 'lead1': 'lead-1', 'crisis': 'crisis year', 'after1': 'after-1', 'after2': 'after-2'}
KIND = {'layer': 'escape layer', 'constant': 'constant noise', 'shuffled': 'shuffled synchrony'}


def pct(x, d=1): return f"{100 * x:.{d}f}%"


def pts(x): return f"{100 * x:+.2f}".replace('-', '−')


def sg(x, d=3): return f"{x:+.{d}f}".replace('-', '−')


def load():
    rd = lambda f, **k: g1b._read(os.path.join(g1b.OUT, f), **k)
    return {'rej': rd('rejections.csv'), 'ver': json.load(open(os.path.join(g1b.OUT, 'verdicts.json'))),
            'cal': rd('calibration.csv'), 'pd': rd('p_distribution.csv'), 'cnt': rd('counts.csv'), 'desc': rd('describe.csv'),
            'ident': json.load(open(os.path.join(g1b.OUT, 'g1_identity.json'))), 'real': g1b.real_values(),
            'g1': pd.read_csv(os.path.join(g1.OUT, 'rejections.csv'), keep_default_na=False, na_values=['']),
            'design': json.load(open(os.path.join(g1b.OUT, 'design.json')))}


def verdict(d, setting='network', variant='primary'):
    return next(v for v in d['ver'] if v['setting'] == setting and v['variant'] == variant)


def rate(d, setting, variant, kind, conv, lag):
    R = d['rej']; return R[(R.setting == setting) & (R.variant == variant) & (R.kind == kind) & (R.convention == conv) & (R.lag == lag)].iloc[0]


def g1_rule_b(d, cell, test='arc_C.lead1'):
    G = d['g1']; return G[(G.model == 'kuramoto') & (G.cell == cell) & (G.rule == 'B') & (G.test == test)].iloc[0]


def verdict_table(d):
    L = ["| Setting | Layer | Past-only lead-1 rejects (95% interval) | (a) lower bound > 3.8% | Minus constant noise (95% interval), points | Minus shuffled synchrony (95% interval), points | (b) | Worlds at p ≤ 0.038 | (c) ≥ 20% | Verdict |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    yn = lambda b: 'pass' if b else 'fail'
    for v in d['ver']:
        dc, ds = v['diff_constant'], v['diff_shuffled']
        L.append(f"| {SETTING[v['setting']]} | {VARIANT[v['variant']].split(':')[0]} | {pct(v['rate'])} ({pct(v['lo'])}–{pct(v['hi'])}) | {yn(v['a'])} | "
                 f"{pts(dc[0])} ({pts(dc[1])} to {pts(dc[2])}) | {pts(ds[0])} ({pts(ds[1])} to {pts(ds[2])}) | {yn(v['b'])} | "
                 f"{pct(v['share_at_real_p'])} | {yn(v['c'])} | **{v['verdict']}** |")
    return L


def lags_table(d, setting='network', variant='primary'):
    L = ["| Phases | Layer | " + " | ".join(LAG.values()) + " |", "|---|---|" + "---|" * len(LAG)]
    for conv, name in (('P', 'two-sided (P)'), ('C', 'past-only (C)')):
        for k in g1b.KINDS:
            cells = []
            for l in LAG:
                x = rate(d, setting, variant, k, conv, l); s = f"{pct(x.rate)} ({pct(x.lo)}–{pct(x.hi)})"
                cells.append(f"**{s}**" if x.lo > g1b.P_REAL else s)
            L.append(f"| {name} | {KIND[k]} | " + " | ".join(cells) + " |")
    return L


def pdist_table(d, setting='network', variant='primary'):
    D = d['pd'][(d['pd'].setting == setting) & (d['pd'].variant == variant)]
    bins = [('0.019 (1/53, the floor)', 1, 1), ('0.038 (2/53, the real p)', 2, 2), ('0.057', 3, 3), ('0.075', 4, 4), ('0.094–0.189', 5, 10),
            ('0.208–0.491', 11, 26), ('0.509–1', 27, 53)]
    L = ["| Past-only lead-1 p | " + " | ".join(KIND.values()) + " |", "|---|---|---|---|"]
    for name, a, b in bins:
        L.append(f"| {name} | " + " | ".join(str(int(D[(D.kind == k) & D.k.between(a, b)].worlds.sum())) for k in g1b.KINDS) + " |")
    L.append("| All worlds | " + " | ".join(str(int(D[D.kind == k].worlds.sum())) for k in g1b.KINDS) + " |")
    return L


def sens_lags_table(d):
    L = ["| Layer variant (trade-coupled) | Two-sided lead-1 | Two-sided crisis | Past-only lead-2 | Past-only lead-1 | Past-only crisis |",
         "|---|---|---|---|---|---|"]
    for v in g1b.VARIANTS:
        c = [rate(d, 'network', v, 'layer', cv, l) for cv, l in (('P', 'lead1'), ('P', 'crisis'), ('C', 'lead2'), ('C', 'lead1'), ('C', 'crisis'))]
        L.append(f"| {VARIANT[v].split(':')[0]} | " + " | ".join(pct(x.rate) for x in c) + " |")
    return L


def calib_table(d):
    C = d['cal']; L = ["| Setting | Layer variant | Escape layer σ | Constant noise σ | Shuffled synchrony σ |", "|---|---|---|---|---|"]
    for (s, v), g in C.groupby(['setting', 'variant'], sort=False):
        f = lambda k: (lambda x: f"{x.sigma:.3g} ({x.mean_recessions:.3g})" + ('' if x.bracketed else ' not reached'))(g[g.kind == k].iloc[0])
        L.append(f"| {SETTING[s]} | {VARIANT[v].split(':')[0]} | {f('layer')} | {f('constant')} | {f('shuffled')} |")
    return L


def counts_line(d, setting='network', variant='primary', kind='layer'):
    c = d['cnt'][(d['cnt'].setting == setting) & (d['cnt'].variant == variant) & (d['cnt'].kind == kind)]
    n = c.worlds.sum(); m = (c.n * c.worlds).sum() / n; lo = c[c.n.between(4, 6)].worlds.sum()
    return n, m, lo, int(c[c.n == 0].worlds.sum())


def describe_table(d, setting='network', variant='primary'):
    D = d['desc'][(d['desc'].setting == setting) & (d['desc'].variant == variant)]
    L = ["| Layer | r measured as | Recession years | Year before | Other years |", "|---|---|---|---|---|"]
    for x in D.itertuples():
        L.append(f"| {KIND[x.kind]} | {x.measure} | {x.recession:.3f} | {x.year_before:.3f} | {x.other:.3f} |")
    return L


def report(d):
    v = verdict(d); real = d['real']['C']['lead1']; realP = d['real']['P']['lead1']
    x = rate(d, 'network', 'primary', 'layer', 'C', 'lead1'); xc = rate(d, 'network', 'primary', 'layer', 'P', 'crisis')
    xP = rate(d, 'network', 'primary', 'layer', 'P', 'lead1'); xCc = rate(d, 'network', 'primary', 'layer', 'C', 'crisis')
    xl2 = rate(d, 'network', 'primary', 'layer', 'C', 'lead2')
    vn, vf = verdict(d, 'null'), verdict(d, 'forcing')
    gb = {c: g1_rule_b(d, c) for c in ('network', 'null', 'forcing')}
    n, m, n46, n0 = counts_line(d)
    ident = d['ident']; same = all(i['rule_b_dates_identical'] == i['worlds'] for i in ident.values())
    partly = [k for k in g1b.VARIANTS if verdict(d, 'network', k)['verdict'] == 'partly']
    notrep = [k for k in g1b.VARIANTS if verdict(d, 'network', k)['verdict'] == 'not reproduced']
    D = d['desc']; td = D[(D.setting == 'network') & (D.variant == 'primary') & (D.kind == 'layer') & (D.measure == 'true r')].iloc[0]
    L = [
        "# G1b — does a synchrony-driven escape layer reproduce the past-only lead?",
        "",
        "Pre-registered in `docs/preregistration_G1b_dtt.md` (draft 14 October 2026, Sid's choices as amendment 1 of "
        "15 October 2026, committed before any run); code `src/ef/gnn/g1b.py`; results in `gnn/G1b/`. Generated by "
        "`python -m ef.gnn.g1b report`; every number below is read from those files. **G1b is the last test Paper 1 takes.**",
        "",
        "## The verdict",
        "",
        f"**Partly reproduced** on the pre-registered primary setting (trade-coupled worlds at κ\\*, world-level state, noise "
        f"σ·r(t) from the true phases, μ = 0.2, refractory 2 years, 1 model unit = 1 year)." if v['verdict'] == 'partly' else
        f"**{v['verdict'].capitalize()}** on the pre-registered primary setting.",
        "",
        f"- **(a) passes.** The past-only lead-1 rejects in {pct(v['rate'])} of 1,000 worlds (95% interval "
        f"{pct(v['lo'])}–{pct(v['hi'])}); the lower bound is above 3.8% (2/53)." if v['a'] else
        f"- **(a) fails.** The past-only lead-1 rejects in {pct(v['rate'])} of worlds ({pct(v['lo'])}–{pct(v['hi'])}).",
        f"- **(b) {'passes' if v['b'] else 'fails'}.** Against constant noise the rate is {pts(v['diff_constant'][0])} points higher "
        f"({pts(v['diff_constant'][1])} to {pts(v['diff_constant'][2])}); against shuffled synchrony {pts(v['diff_shuffled'][0])} "
        f"({pts(v['diff_shuffled'][1])} to {pts(v['diff_shuffled'][2])}). Same worlds and same escape noise in each pair.",
        f"- **(c) {'passes' if v['c'] else 'fails'}.** {pct(v['share_at_real_p'])} of worlds reach p ≤ 0.038, the real p; the "
        f"threshold was 20%. With 53 circular shifts p ≤ 0.05 and p ≤ 0.038 are the same event, so (c) asks that the rejection "
        f"rate itself be at least 20%. Only {pct(x.corr_at_least_real)} of worlds reach the real correlation "
        f"({sg(real['corr'])}); the mean past-only lead-1 correlation over worlds is {sg(x.mean_corr)}.",
        "",
        "In plain words: the escape layer makes recessions likelier when synchrony is high, so it does leave a past-only "
        "lead that the Paper 1 pipeline can see, more often than chance and more often than the same layer with the timing "
        "of synchrony removed. But the lead it leaves is small and rarely significant. A result the size of the real one "
        f"(+0.379, p = 0.038) is an unusual outcome of the layer, about one world in {int(round(1 / max(v['share_at_real_p'], 1e-9)))} at that p "
        f"and about one in {int(round(1 / max(x.corr_at_least_real, 1e-9)))} at that correlation.",
        "",
        f"**Some lead was expected by construction** (stated in the pre-registration): the layer raises the chance of a "
        f"recession when the true r is high. It does: in the primary worlds the true r averages {td.recession:.3f} in "
        f"recession years and {td.year_before:.3f} the year before, against {td.other:.3f} in other years. What the test adds is "
        "how much of that survives annual sampling, 53 points, a handful of events and phases estimated from past data: "
        "little.",
        "",
        f"**Coupling matters.** Without coupling the same layer, calibrated the same way, does not reproduce the lead: the "
        f"past-only lead-1 rejects in {pct(vn['rate'])} ({pct(vn['lo'])}–{pct(vn['hi'])}) of uncoupled worlds and "
        f"{pct(vf['rate'])} ({pct(vf['lo'])}–{pct(vf['hi'])}) with common forcing only; the verdicts are *{vn['verdict']}* and "
        f"*{vf['verdict']}*. Only trade-coupled worlds give a past-only lead above chance.",
        "",
        "## What was run",
        "",
        "- **Worlds.** The G1 Kuramoto worlds themselves: 1,000 per setting, the same seeds and chunks, so world k here is "
        "world k of G1. Checked: each world's own recession dates (G1's rule B, from its simulated world GDP) equal the "
        f"dates G1 stored in {'every' if same else 'not every'} world of every setting "
        f"({', '.join(f'{s}: {i['rule_b_dates_identical']}/{i['worlds']}' for s, i in ident.items())}).",
        "- **The layer.** dx = (μ + x − x³) dt/τ + σ r(t) dW/√τ, integrated beside the oscillators every 0.01 years from 1950 "
        "with its own noise; r(t) from the model's true phases. An escape (x reaches 0) resets x to the lower equilibrium "
        "and marks a recession year unless one was counted in the previous two years; only 1970–2022 count.",
        "- **Calibration.** σ set so that the mean number of recession years in 1970–2022 is 5, on 500 separate "
        "calibration worlds per setting. Only the count is used, never the years. Every layer and control was "
        "recalibrated the same way (table below).",
        "- **Tests.** Each world's pipeline r(t) under convention P (the two-sided arc) and C (past-only), computed once "
        "from its simulated GDP exactly as for the real data; the arc at every lag against 53 circular shifts, one-sided in "
        "the pre-registered directions.",
        "- **Controls.** Constant noise (g = σ_c in every world and year) and shuffled synchrony (each world's r(t) with "
        "its one-year blocks permuted), both recalibrated; the plain G1 world with recessions dated from world output "
        "(rule B) as a reference.",
        "",
        "## Every setting and sensitivity, as pre-registered",
        "",
        "Past-only lead-1 (convention C), 1,000 worlds each. Differences are in percentage points, paired by world.",
        "",
        *verdict_table(d),
        "",
        f"Of the eight sensitivities on the trade-coupled worlds, {len(partly) - (1 if 'primary' in partly else 0)} give the same "
        f"verdict as the primary (*partly*: {'; '.join(SHORT[k] for k in partly if k != 'primary')}) and "
        f"{len(notrep)} do not reproduce the lead ({'; '.join(SHORT[k] for k in notrep)}). None reaches (c).",
        "",
        "## Every lag, primary setting",
        "",
        "Share of worlds rejecting at p ≤ 0.05 (95% interval). **Bold**: the lower bound is above 3.8%, the exact rate with "
        "nothing there. Two-sided arc: convention P; past-only: convention C. Lead lags are tested upward, after-lags "
        "downward, as in Paper 1.",
        "",
        *lags_table(d),
        "",
        f"The two-sided arc shows the layer's built-in link most strongly in the crisis year ({pct(xc.rate)}) and at lead-1 "
        f"({pct(xP.rate)}); with past-only phases these fall to {pct(xCc.rate)} and {pct(x.rate)}. Past-only lead-2 rejects "
        f"in {pct(xl2.rate)}. The after-lags, tested for a fall, reject less often than chance in the layer worlds: recessions "
        "come when synchrony is high, and synchrony is persistent, so it is still high after them.",
        "",
        "Other settings, same layout:",
        "",
        "**No coupling**", "", *lags_table(d, 'null'), "",
        "**Common forcing only**", "", *lags_table(d, 'forcing'), "",
        "**Sensitivities (trade-coupled, escape layer only)**", "", *sens_lags_table(d), "",
        "## The full p-value distribution, past-only lead-1, primary setting",
        "",
        "Number of worlds at each p (out of 1,000). With 53 circular shifts p takes the values k/53. Every world's p for every "
        "lag is in `gnn/G1b/pvalues.csv.gz`; the full distribution by k in `gnn/G1b/p_distribution.csv`.",
        "",
        *pdist_table(d),
        "",
        "## The plain G1 world (reference)",
        "",
        "In the same worlds with recessions dated from world output (G1 rule B, `gnn/G1/rejections.csv`), the past-only "
        f"lead-1 rejected in {pct(gb['network'].rate)} of trade-coupled worlds, {pct(gb['null'].rate)} of uncoupled ones and "
        f"{pct(gb['forcing'].rate)} with forcing. The escape layer raises the trade-coupled rate from {pct(gb['network'].rate)} "
        f"to {pct(v['rate'])}.",
        "",
        "## Calibration",
        "",
        "σ of each layer and control, with the mean number of recession years it reached in 1970–2022 on the calibration "
        "worlds (target 5). The Ā·R_A sensitivity was rerun once with its bracket scaled, because Ā·R_A is in units of log "
        "GDP; the first run stopped at the top of the unscaled bracket (`docs/decisions.md`, 15 October 2026). Its constant "
        "control is the primary one.",
        "",
        *calib_table(d),
        "",
        f"On the test worlds the escape layer gave {m:.2f} recession years per world on average; {n46} of {n} worlds have "
        f"4–6, and {n0} have none (`gnn/G1b/counts.csv`). The rejection rates among the worlds with 4–6 recession years are in "
        "`gnn/G1b/rejections.csv` (`rate_4_6`); for the primary past-only lead-1 it is "
        f"{pct(x.rate_4_6)}. A world whose lag has no recession among the years it uses cannot reject and is counted as not "
        "rejecting (column `undefined`).",
        "",
        "## Synchronization around the layer's recessions (description)",
        "",
        "Mean r over worlds, primary setting. True r: the model's phases averaged over each year; pipeline r: from the "
        "simulated GDP.",
        "",
        *describe_table(d),
        "",
        "## Limits of this test",
        "",
        "- One mechanism, one family of worlds (Kuramoto on the saved G1 trade network). The Stuart–Landau worlds were not "
        "used (Sid: the calibrated G1 Kuramoto world).",
        "- The layer does not feed back on the oscillators: an escape does not change any economy's cycle. In the real "
        "world a recession is part of the cycles it is measured from.",
        "- The calibration fixes only how often recessions happen. The worlds' synchrony is calibrated to the real mean r, "
        "not to its variance or persistence, which is what a lead depends on.",
        "- A *partly* verdict does not say that the real lead is produced this way; it says that this mechanism can leave a "
        "past-only lead the pipeline detects, but rarely one as large as the real one.",
        "",
    ]
    return "\n".join(L)


def closing(d):
    v = verdict(d); vn, vf = verdict(d, 'null'), verdict(d, 'forcing')
    G = d['g1']; k0 = lambda t, rule, model: G[(G.model == model) & (G.cell == 'null') & (G.rule == rule) & (G.test == t)].iloc[0].rate
    gb = {c: g1_rule_b(d, c) for c in ('network', 'null', 'forcing')}
    swing = [k0('structure.p_swing', 'A', m) for m in ('kuramoto', 'stuart_landau')]
    crisisB = [k0('arc.crisis', 'B', m) for m in ('kuramoto', 'stuart_landau')]; leadB = [k0('arc.lead1', 'B', m) for m in ('kuramoto', 'stuart_landau')]
    pastB = [k0('arc_C.lead1', 'B', m) for m in ('kuramoto', 'stuart_landau')]
    cross = G[(G.model == 'kuramoto') & (G.cell == 'network') & (G.rule == 'A') & (G.test == 'diversification.gdp_mean')].iloc[0].rate
    x = rate(d, 'network', 'primary', 'layer', 'C', 'lead1')
    A0 = G[(G.cell == 'null') & (G.rule == 'A') & ~G.test.str.startswith('family.')]
    ok = {m: int((A0[A0.model == m].verdict != 'over').sum()) for m in ('kuramoto', 'stuart_landau')}; nt = A0[A0.model == 'kuramoto'].test.nunique()
    L = [
        "# Closing G1 and G1b — what the simulations say about Paper 1",
        "",
        "Written 15 October 2026 from `gnn/G1_report.md` and `gnn/G1b_report.md` (numbers from `gnn/G1/` and `gnn/G1b/`, "
        "generated by `python -m ef.gnn.g1b report`). After G1b Paper 1 is locked: no new tests; anything new is Paper 2.",
        "",
        "## What G1 found",
        "",
        "G1 built worlds of 31 simulated economies with known coupling — phase oscillators (Kuramoto) and phase-and-size "
        "oscillators (Stuart–Landau) on the real trade network — calibrated to the real cycles, and ran every Paper 1 test "
        "on them.",
        "",
        f"1. **The tests have the right size.** With no coupling at all, "
        f"{(str(ok['kuramoto']) + ' of ' + str(nt) + ' tests in each kind of world') if ok['kuramoto'] == ok['stuart_landau'] else (str(ok['kuramoto']) + ' (Kuramoto) and ' + str(ok['stuart_landau']) + ' (Stuart–Landau) of ' + str(nt) + ' tests')} "
        f"reject at or below their correct rate. "
        f"The exception that mattered, the swing-size term of the identity ({pct(swing[0])} and {pct(swing[1])}), was an edge "
        "effect; the edge-matched null of amendment 4 fixed it and the real result stayed at the floor.",
        f"2. **Dating recessions from world output builds in some synchronization.** In uncoupled worlds that date their own "
        f"recessions, the two-sided crisis-year and lead-1 arcs reject in {pct(min(crisisB))}–{pct(max(crisisB))} and "
        f"{pct(min(leadB))}–{pct(max(leadB))} of worlds, about twice the correct 3.8%. The past-only lead-1 does not "
        f"({pct(min(pastB))}–{pct(max(pastB))}). This is why the paper's lead claim rests on the past-only version (L8).",
        f"3. **The cross-term test detects co-movement, not co-movement at recessions.** It rejects in {pct(cross)} of "
        "trade-coupled Kuramoto worlds even with the real recession dates, which have nothing to do with those worlds (L9).",
        f"4. **No G1 world produced the past-only lead.** With recessions dated from each world's output it rejected in "
        f"{pct(gb['network'].rate)} of trade-coupled, {pct(gb['null'].rate)} of uncoupled and {pct(gb['forcing'].rate)} of "
        "forced Kuramoto worlds — never above chance.",
        "",
        "## What G1b found",
        "",
        "G1b added one mechanism to the same worlds: a recession is an escape from a stable state, and the shocks that cause "
        "escapes grow with synchrony (DTT, diversification-type tipping, Sid's report of 13 October 2026). Its verdict, "
        f"exactly as pre-registered: **{v['verdict']}**.",
        "",
        f"- In trade-coupled worlds the past-only lead-1 rejects in {pct(v['rate'])} of worlds ({pct(v['lo'])}–{pct(v['hi'])}), "
        "above chance and above both controls (constant noise; synchrony shuffled in time).",
        f"- But only {pct(v['share_at_real_p'])} of worlds reach the real p = 0.038, against the 20% required, and "
        f"{pct(x.corr_at_least_real)} reach the real correlation of +0.379.",
        f"- Without trade coupling the layer leaves no past-only lead ({pct(vn['rate'])} uncoupled, {pct(vf['rate'])} with "
        "common forcing).",
        "",
        "## What it means for Paper 1",
        "",
        "- **The tests can be trusted to have their stated size**, with the two exceptions now handled (the edge-matched "
        "null; the past-only lead as the lead claim). The κ = 0 table goes into the Methods as a validation (§5.3).",
        "- **The lead claim rests on the past-only lead-1**, because the two-sided arc is inflated by how recessions are "
        "dated (L8).",
        "- **The loss-of-diversification arithmetic is arithmetic.** Years when cycles happen to line up have larger world "
        "swings, coupled or not; recessions dated from world output are such years even without coupling. The theory box "
        "says so.",
        "- **The mechanism check is suggestive, not confirmatory.** A synchrony-driven escape layer on coupled worlds can "
        "leave a past-only lead the pipeline detects, and coupling is needed for it; but a lead as large as the real one is "
        "rare under it. The real result is either an unusual draw, or the real mechanism is stronger or different from the "
        "one simulated (for example feedback from recessions to the cycles, which G1b leaves out). Paper 1 reports this "
        "exactly and claims no mechanism from it.",
        "- **The real lead still rests on two events (2009 and 2020).** Nothing in G1 or G1b changes that.",
        "",
    ]
    return "\n".join(L)


def main():
    d = load()
    open(os.path.join(ROOT, 'gnn', 'G1b_report.md'), 'w').write(report(d))
    open(os.path.join(ROOT, 'gnn', 'G1_closing.md'), 'w').write(closing(d))


if __name__ == '__main__':
    main()
