"""results/COMPARISON.md from the Phase 3 results tree (HANDOFF.md Phase 3; docs/preregistration_S30.md section 8).

One row per registry ID with the stored S26 value, S26 and S30 under the pre-registered conventions, a flag where the
sign changes or p crosses 0.05, and the pre-registered criterion; then the sensitivity tables.

    python -m ef.comparison [--results results]
"""
import argparse
import json
import os

import numpy as np

from ef import config

FLOORS = "p-value floors: circular shift 1/53 = 0.019; 5,000 surrogates 1/5001 = 0.0002; channel anatomy 2,000 surrogates 1/2001 = 0.0005"
# the stored S26 values (docs/results_registry.md), for reference
STORED = {'A1': '+0.230 (0.038)', 'A2': '+0.216 (0.019)', 'A3': '+0.149 (0.189)', 'A4': '+0.078 (0.679)', 'A5': '−0.277 (0.019)',
          'A6': '0.70 / 0.35', 'A7': '0.65 / 0.37 / 0.54', 'A8': '0.094 / 0.094 / 0.189', 'A9': '0.047 / 0.047 / 0.063',
          'C1': '+0.608 (0.019; surr. 0.0006, W)', 'C2': '+0.530 (0.019)', 'D1': '82.4%', 'D3': '96.9%',
          'D4': '0.723 vs 0.669 / 0.880 vs 0.818', 'D6': '0.35 / 0.48; 0.0002', 'D7': '35 / 50 / 14%', 'D8': '41 / 46 / 13%',
          'D9': '0.376 → 0.490; ×1.14', 'D10': '< 1e-18', 'D11': '39.3% / 60.7% (0.103 / 0.0002)', 'D12': '+0.942',
          'E1': '0.677 vs 0.379', 'E4': '−0.171 (0.167); det. −0.086 (0.316)', 'E6': '+0.10 (0.306)', 'E7': '0.403 yr (0.0002, W)',
          'E9': '5.85 yr', 'E10': '0.868', 'E11': '+0.18 (0.057) / +0.18 (0.038)', 'F1': '−0.152 (0.757)', 'F2': '+0.295 (0.107)',
          'F4': '+0.098 (0.542)', 'F5': '6.4 / 7.1', 'G1': '+0.266 (0.019)', 'G2': '+0.293 (0.038)', 'G3': '+0.237 (0.019) / −0.332 (0.019)',
          'G4': '0.34–0.64 vs 0.17–0.25 (0.0005)', 'G5': '0.22→0.58, 0.30→0.60, 0.39→0.61, 0.09→0.56', 'G7': '11, 8, 8, 22, 25',
          'G8': '0.46 vs 0.75'}


class Tree:
    def __init__(self, root): self.root = root

    def __call__(self, variant, conv, test):
        p = os.path.join(self.root, variant, conv, f'{test}.json')
        return json.load(open(p))['results'] if os.path.exists(p) else None


def cp(c, p, d=3):
    """'+0.216 (0.019)'"""
    if c is None: return '—'
    s = f"{c:+.{d}f}".replace('-', '−')
    return s if p is None else f"{s} ({p:.4f})" if p < 0.001 else f"{s} ({p:.3f})"


def pct(x): return '—' if x is None else f"{100 * x:.1f}%"


def verdict(ref, new, expect):
    """Pre-registered reading of a (corr, p) result. expect: 'sig' (S26 significant) or 'null'."""
    if ref is None or new is None or None in ref or None in new: return '—'
    if expect == 'sig':
        if np.sign(new[0]) != np.sign(ref[0]): return '**reverses**'
        return 'replicates' if new[1] < 0.05 else '**weakens**'
    return 'stays null' if new[1] >= 0.05 else '**becomes significant**'


def flag(ref, new):
    if ref is None or new is None or None in ref or None in new: return ''
    f = []
    if np.sign(ref[0]) != np.sign(new[0]): f.append('sign change')
    if (ref[1] < 0.05) != (new[1] < 0.05): f.append('crosses 0.05')
    return '; '.join(f)


# ------------------------------------------------------------------ extracting the registry quantities

def extract(T, v, conv='P'):
    """Registry quantities for one sample or variant: {id: (display, (stat, p) or None, extra)}."""
    q = {}
    arc = T(v, conv, 'arc'); amp = T(v, conv, 'amplitude'); div = T(v, conv, 'diversification'); cs = T(v, conv, 'cross_split')
    st = T(v, conv, 'structure'); ms = T(v, conv, 'mst'); pl = T(v, conv, 'phase_lags'); csd = T(v, conv, 'csd')
    bf = T(v, conv, 'bifurcation'); ch = T(v, conv, 'channels')
    if arc:
        for i, k in zip(('A1', 'A2', 'A3', 'A4', 'A5'), ('lead2', 'lead1', 'crisis', 'after1', 'after2')):
            a = arc['arc'][k]; q[i] = (cp(a['corr'], a['p']), (a['corr'], a['p']))
        q['A6'] = (f"{arc['epoch_peak']:.2f} / {arc['epoch_after2']:.2f}", None)
        m = arc['mean_ci']; q['A7'] = (f"{m['recession'][0]:.2f} / {m['downturn'][0]:.2f} / {m['normal'][0]:.2f}", (m['recession'][0] - m['normal'][0], None))
        b, h = arc['bonferroni'], arc['benjamini_hochberg']
        q['A8'] = (f"{b['lead1']:.3f} / {b['after2']:.3f} / {b['lead2']:.3f}", None); q['A9'] = (f"{h['lead1']:.3f} / {h['after2']:.3f} / {h['lead2']:.3f}", None)
    if amp:
        q['C1'] = (f"{cp(amp['corr_detrended'], amp['p_shift'])}; surr. {amp['p_surrogate']:.4f}", (amp['corr_detrended'], amp['p_shift']))
        q['C2'] = (cp(*amp['corr_raw']), tuple(amp['corr_raw']))
    if div:
        g, e = div.get('gdp_mean'), div.get('equal')
        if g: q['D1'] = (pct(g['cross_fraction_of_excess']), (g['cross_fraction_of_excess'] - 0.5, None), g['recession_windows'])
        if e: q['D3'] = (pct(e['cross_fraction_of_excess']), (e['cross_fraction_of_excess'] - 0.5, None))
        if g and e:
            q['D4'] = (f"{g['cross_share_crisis']:.3f} vs {g['cross_share_normal']:.3f} / {e['cross_share_crisis']:.3f} vs {e['cross_share_normal']:.3f}",
                       (min(g['cross_share_crisis'] - g['cross_share_normal'], e['cross_share_crisis'] - e['cross_share_normal']), None))
            if 'd6' in g:
                q['D6'] = (f"{g['d6']['p_ratio_nominal']:.2f} / {e['d6']['p_ratio_nominal']:.2f}; Δcross {g['d6']['p_excess_cross']:.4f}, Δown {g['d6']['p_excess_own']:.4f}", None)
    if cs:
        for i, k in (('D7', 'gdp_mean'), ('D8', 'equal')):
            c = cs.get(k)
            if c: q[i] = (f"{100 * c['from_correlation']:.0f} / {100 * c['from_swing_size']:.0f} / {100 * c['interaction']:.0f}%", (min(c['from_correlation'], c['from_swing_size']), None))
        c = cs.get('gdp_mean') or cs.get('gdp_end')
        if c: q['D9'] = (f"{c['corr_normal']:.3f} → {c['corr_crisis']:.3f}; ×{c['sd_crisis'] / c['sd_normal']:.2f}", (min(c['corr_crisis'] - c['corr_normal'], c['sd_crisis'] - c['sd_normal']), None))
    if st:
        q['D10'] = (f"{st['identity_err']:.0e}", (1e-12 - st['identity_err'], None))
        q['D11'] = (f"{100 * st['align_share']:.1f}% / {100 * st['swing_share']:.1f}% ({st['p_align']:.3f} / {st['p_swing']:.4f})", (st['dA'], st['p_swing']))
        q['D12'] = (f"{st['corr_RA_r']:+.3f}", (st['corr_RA_r'], None))
        q['E10'] = (f"{st['lambda2']:.3f}; bloc A {len(st['blocA'])}, B {len(st['blocB'])}", None)
        h = st['hier']; q['E11'] = (f"{cp(h['r_within']['lead1']['corr'], h['r_within']['lead1']['p'], 2)} / {cp(h['r_between']['lead1']['corr'], h['r_between']['lead1']['p'], 2)}", None)
    if ms:
        d = ms['L_decade_means']; a, b = d.get('1979-1989'), d.get('2013-2022')
        q['E1'] = (f"{a:.3f} vs {b:.3f} ({a / b:.2f}×)", (a - b, None))
        det = f"; det. {cp(ms['tau_L_detrended'], ms['p_contraction_detrended'])}" if ms.get('tau_L_detrended') is not None else ''
        q['E4'] = (cp(ms['tau_L'], ms['p_contraction']) + det, (ms['tau_L'], ms['p_contraction']), ms.get('pre_crisis_events'))
        q['E6'] = (cp(ms['tau_lambdamax'], ms['p_fragility']), (ms['tau_lambdamax'], ms['p_fragility']))
    if pl:
        q['E7'] = (f"{pl['sd']:.3f} yr ({pl['p_spread_lower']:.4f}; null mean {pl['null_mean']:.3f})", (-1.0, pl['p_spread_lower']))
        q['E9'] = (f"{pl['period_years']:.2f} yr", None)
    if csd:
        q['F1'] = (cp(csd['tau_ar1'], csd['p_ar1']), (csd['tau_ar1'], csd['p_ar1']), csd.get('pre_crisis_events'))
        q['F2'] = (cp(csd['tau_var'], csd['p_var']), (csd['tau_var'], csd['p_var']), csd.get('pre_crisis_events'))
    if bf:
        q['F4'] = (cp(bf['stat_real'], bf['p_slowing_post']), (bf['stat_real'], bf['p_slowing_post']), bf.get('post_crisis_events'))
        e = bf['epoch_KKc_mean_t-3..t+3']; q['F5'] = (f"{e[2]:.1f} / {e[3]:.1f}", None)
    if ch:
        s = ch['sync']
        for i, c, k in (('G1', 'strate', 'lead2'), ('G2', 'inv', 'lead2')):
            q[i] = (f"{cp(*s[c]['tests'][k])} [{s[c]['n']}]", tuple(s[c]['tests'][k]))
        q['G3'] = (f"{cp(*s['GDP']['tests']['lead1'])} / {cp(*s['GDP']['tests']['after2'])} [{s['GDP']['n']}]", tuple(s['GDP']['tests']['lead1']))
        q['G3b'] = (None, tuple(s['GDP']['tests']['after2']))
        an = ch.get('anatomy')
        if an:
            mr = [an[c]['mean_r'] for c in an]; nr = [an[c]['null_r'] for c in an]; ps = max(an[c]['p_sync'] for c in an)
            q['G4'] = (f"{min(mr):.2f}–{max(mr):.2f} vs {min(nr):.2f}–{max(nr):.2f} (max p {ps:.4f})", (1.0, ps))
            q['G5'] = (', '.join(f"{an[c]['paircorr_pre90']:.2f}→{an[c]['paircorr_post90']:.2f}" for c in ('GDP', 'exports', 'imports', 'balance')),
                       (min(an[c]['paircorr_post90'] - an[c]['paircorr_pre90'] for c in ('GDP', 'exports', 'imports', 'balance')), None))
        if 'contracting' in ch: q['G7'] = (', '.join(str(v) for v in ch['contracting'].values()), None)
        if 'coupling' in ch: q['G8'] = (f"{ch['coupling']['1970-1989']:.2f} vs {ch['coupling']['1990-2022']:.2f}", None)
    return q


ROWS = [  # id, label, how S30 is judged: 'sig', 'null', 'pos' (descriptive: positive), 'info'
    ('A1', 'Arc lead-2', 'sig'), ('A2', 'Arc lead-1', 'sig'), ('A3', 'Arc crisis year', 'null'), ('A4', 'Arc after-1 (lower)', 'null'),
    ('A5', 'Arc after-2 (lower)', 'sig'), ('A6', 'Epoch mean r, t−1 / t+2', 'info'), ('A7', 'Mean r: recessions / downturns / normal', 'pos'),
    ('A8', 'Bonferroni: lead-1 / after-2 / lead-2', 'info'), ('A9', 'Benjamini–Hochberg q: lead-1 / after-2 / lead-2', 'info'),
    ('C1', 'r vs swing size, detrended', 'sig'), ('C2', 'r vs swing size, raw', 'sig'),
    ('D1', 'Cross share of recession excess, GDP weights (window mean)', 'pos'), ('D3', 'Same, equal weights', 'pos'),
    ('D4', 'Cross share recession vs normal: GDP / equal', 'pos'), ('D6', 'Disclosure: nominal p of share ratio GDP / equal; Δ tests', 'info'),
    ('D7', 'Cross-term rise: correlation / swing / interaction, GDP', 'pos'), ('D8', 'Same, equal weights', 'pos'),
    ('D9', 'Mean pairwise corr normal → recession; cycle s.d. ratio', 'pos'), ('D10', 'Fibrillation identity error', 'pos'),
    ('D11', 'Recession excess in world swing²: alignment / swing size (p)', 'sig'), ('D12', 'corr(R_A, r)', 'pos'),
    ('E1', 'MST decade means 1979–89 vs 2013–22', 'pos'), ('E4', 'Pre-crisis MST contraction τ (lower)', 'null'),
    ('E6', 'Pre-crisis largest-eigenvalue trend τ', 'null'), ('E7', 'Phase-lead spread (lower tail)', 'sig'), ('E9', 'Mean cycle period', 'info'),
    ('E10', 'Fiedler λ2; bloc sizes', 'info'), ('E11', 'Arc lead-1 within / between blocs', 'info'),
    ('F1', 'Pre-crisis lag-1 autocorrelation trend τ', 'null'), ('F2', 'Pre-crisis variance trend τ', 'null'),
    ('F4', 'Post-crisis recovery-rate change (lower)', 'null'), ('F5', 'Implied K/Kc around onsets, t−1 / t0', 'info'),
    ('G1', 'Short-rate synchronization, lead-2 [economies]', 'sig'), ('G2', 'Investment synchronization, lead-2', 'sig'),
    ('G3', 'Real GDP (GMD) synchronization, lead-1 / after-2', 'sig'), ('G4', 'Channel synchronization vs surrogates', 'sig'),
    ('G5', 'Pairwise corr pre→post 1990: GDP, exports, imports, balance', 'pos'), ('G7', 'Economies contracting 1975, 1982, 1991, 2009, 2020', 'info'),
    ('G8', 'Coupling to the rest, 1970–89 vs 1990–2022', 'info')]


def judge(rid, kind, ref, new):
    a = ref[1] if ref and len(ref) > 1 else None
    b = new[1] if new and len(new) > 1 else None
    if kind == 'info' or b is None: return '', ''
    if kind == 'pos':
        return '', ('holds' if b[0] is not None and b[0] > 0 else '**does not hold**')
    if kind == 'null':
        if a is not None and a[1] < 0.05 and b[1] < 0.05:
            return flag(a, b), '**significant on S26 and S30 under P** (the registry null came from another convention)'
        return flag(a, b), verdict(a, b, 'null')
    if rid == 'E7': return flag(a, b), ('replicates' if b[1] < 0.05 else '**weakens**')
    if rid == 'D11': return flag(a, b), ('replicates' if b[0] > 0 and b[1] < 0.05 else '**weakens**')
    if rid == 'G4': return '', ('replicates' if b[1] < 0.05 else '**weakens**')
    if a is not None and a[1] >= 0.05: return flag(a, b), verdict(a, b, 'null') + ' (S26 under P not significant)'
    return flag(a, b), verdict(a, b, 'sig')


def past_only(T, sample):
    """A1, A2 (arc) and G1 (short rates) under convention C: (corr, p)."""
    c, ch = T(sample, 'P', 'conventions'), T(sample, 'C', 'channels'); out = {}
    if c: out['A1'], out['A2'] = ((c['C']['arc'][k]['corr'], c['C']['arc'][k]['p']) for k in ('lead2', 'lead1'))
    if ch: out['G1'] = tuple(ch['sync']['strate']['tests']['lead2'])
    return out


def main_table(T):
    s26, s30 = extract(T, 'S26'), extract(T, 'S30'); c30 = past_only(T, 'S30')
    L = ["| ID | Quantity | Registry (S26 as stored) | S26 (P) | S30 (P) | Flag S26 → S30 | Pre-registered reading for S30 |", "|---|---|---|---|---|---|---|"]
    for rid, label, kind in ROWS:
        a, b = s26.get(rid), s30.get(rid)
        f, v = judge(rid, kind, a, b)
        if rid == 'G3':
            f2, v2 = judge('G3b', kind, s26.get('G3b'), s30.get('G3b')); f = '; '.join(x for x in (f, f2) if x); v = f"{v} / {v2}"
        if rid in c30:
            x = c30[rid]; v += f"; past data only (C): {cp(*x)} — " + ('holds' if x[0] > 0 and x[1] < 0.05 else '**fails**')
        L.append(f"| {rid} | {label} | {STORED.get(rid, '')} | {a[0] if a else '—'} | {b[0] if b else '—'} | {f} | {v} |")
    return L


# ------------------------------------------------------------------ sensitivity tables

def conventions_table(T):
    L = ["| Sample | Convention | A1 lead-2 | A2 lead-1 | A3 crisis | A5 after-2 | C1 r–swing (det.) |", "|---|---|---|---|---|---|---|"]
    for s in ('S26', 'S30'):
        c = T(s, 'P', 'conventions')
        if not c: continue
        for conv in ('P', 'W', 'N', 'E', 'C'):
            if conv not in c: continue
            a = c[conv]['arc']
            L.append(f"| {s} | {conv} | {cp(a['lead2']['corr'], a['lead2']['p'])} | {cp(a['lead1']['corr'], a['lead1']['p'])} | "
                     f"{cp(a['crisis']['corr'], a['crisis']['p'])} | {cp(a['after2']['corr'], a['after2']['p'])} | {cp(*c[conv]['amp_detrended'])} |")
    return L


def surrogate_conventions_table(T):
    ids = ['C1', 'D11', 'E7', 'F1', 'F2', 'F4']
    L = ["| Sample | Convention | " + " | ".join(ids) + " |", "|---" * (len(ids) + 2) + "|"]
    for s in ('S26', 'S30'):
        for conv in ('P', 'W', 'N', 'E'):
            q = extract(T, s, conv)
            if not q: continue
            L.append(f"| {s} | {conv} | " + " | ".join(q[i][0] if i in q else '—' for i in ids) + " |")
    L += ["", "Band-pass-only tests under N (band-pass on 1970–2022 only; amendment 1.1):", "",
          "| Sample | D1 | D3 | E1 | E4 |", "|---|---|---|---|---|"]
    for s in ('S26', 'S30'):
        q = extract(T, s, 'N')
        if q: L.append(f"| {s} | " + " | ".join(q[i][0] if i in q else '—' for i in ('D1', 'D3', 'E1', 'E4')) + " |")
    return L


def variant_table(T, rows, variants, ids, note=None):
    L = ["| Variant | " + " | ".join(ids) + " |", "|---" * (len(ids) + 1) + "|"]
    for label, v in variants:
        q = extract(T, v)
        if q: L.append(f"| {label} | " + " | ".join(q[i][0] if i in q else '—' for i in ids) + " |")
    return L


def dependence_table(T):
    """Leave-one-added-economy-out on S30: which results depend on one economy (sign reverses or p crosses 0.05)."""
    ids = ['A1', 'A2', 'A3', 'A5', 'C1', 'D11', 'E4', 'E7', 'F1', 'F2', 'F4', 'G1', 'G2', 'G3']
    base = extract(T, 'S30'); L = ["| Without | " + " | ".join(ids) + " |", "|---" * (len(ids) + 1) + "|"]
    for iso in ('CHN', 'BRA', 'SAU', 'IRN'):
        q = extract(T, f'S30_minus_{iso}')
        if not q: continue
        cells = []
        for i in ids:
            if i not in q: cells.append('—'); continue
            f = flag(base[i][1], q[i][1]) if i in base and base[i][1] and q[i][1] else ''
            cells.append(q[i][0] + (f" **{f}**" if f else ''))
        L.append(f"| {iso} | " + " | ".join(cells) + " |")
    L += ["", "Descriptive quantities without each added economy:", "", "| Without | D1 | D3 | D7 | E1 |", "|---|---|---|---|---|"]
    for iso in ('CHN', 'BRA', 'SAU', 'IRN'):
        q = extract(T, f'S30_minus_{iso}')
        if q: L.append(f"| {iso} | " + " | ".join(q[i][0] if i in q else '—' for i in ('D1', 'D3', 'D7', 'E1')) + " |")
    return L


def robustness_table(T):
    a, b = T('S26', 'P', 'robustness'), T('S30', 'P', 'robustness')
    if not (a and b): return []
    L = ["| Check | S26 lead-1 | S30 lead-1 | S26 after-2 | S30 after-2 |", "|---|---|---|---|---|"]
    for k in a:
        if k.startswith('without ') and k[8:] in config.sample('S30') and k[8:] not in ('USA', 'DEU', 'JPN'): continue
        if a[k] is None or k not in b or b[k] is None: continue
        L.append(f"| {k} | {cp(*a[k]['lead1'], 2)} | {cp(*b[k]['lead1'], 2)} | {cp(*a[k]['after2'], 2)} | {cp(*b[k]['after2'], 2)} |")
    return L


def loo_table(T):
    b = T('S30', 'P', 'robustness')
    if not b: return []
    L = ["| Without | lead-2 | lead-1 | crisis | after-2 |", "|---|---|---|---|---|"]
    for iso in config.sample('S30'):
        k = f'without {iso}'
        if k in b and b[k]: L.append(f"| {iso} | " + " | ".join(cp(*b[k][x], 2) for x in ('lead2', 'lead1', 'crisis', 'after2')) + " |")
    return L


def edge_table(T):
    L = ["| Sample | Convention | Full arc lead-1 | Full arc after-2 | Without 2020 lead-1 | Without 2020 after-2 |", "|---|---|---|---|---|---|"]
    for s in ('S26', 'S30'):
        for conv in ('P', 'E'):
            r = T(s, conv, 'robustness')
            if r: L.append(f"| {s} | {conv} | {cp(*r['baseline']['lead1'])} | {cp(*r['baseline']['after2'])} | {cp(*r['without 2020']['lead1'])} | {cp(*r['without 2020']['after2'])} |")
    return L


def past_only_table(T):
    L = ["| Sample | Test | P | C (past data only) |", "|---|---|---|---|"]
    for s in ('S26', 'S30'):
        c = T(s, 'P', 'conventions'); chP, chC = T(s, 'P', 'channels'), T(s, 'C', 'channels')
        if c:
            for k, lab in (('lead2', 'A1 arc lead-2'), ('lead1', 'A2 arc lead-1')):
                L.append(f"| {s} | {lab} | {cp(c['P']['arc'][k]['corr'], c['P']['arc'][k]['p'])} | {cp(c['C']['arc'][k]['corr'], c['C']['arc'][k]['p'])} |")
        if chP and chC:
            for ch_, k, lab in (('strate', 'lead2', 'G1 short rates, lead-2'), ('inv', 'lead2', 'G2 investment, lead-2'),
                                ('GDP', 'lead1', 'G3 real GDP, lead-1'), ('GDP', 'after2', 'G3 real GDP, after-2')):
                L.append(f"| {s} | {lab} | {cp(*chP['sync'][ch_]['tests'][k])} | {cp(*chC['sync'][ch_]['tests'][k])} |")
    return L


def anatomy_table(T):
    L = ["| Channel | S26 n | S26 mean r (null) | S26 pairwise corr pre→post 1990 | S26 lead-2 | S30 n | S30 mean r (null) | S30 pairwise corr | S30 lead-2 |",
         "|---|---|---|---|---|---|---|---|---|"]
    a, b = T('S26', 'P', 'channels'), T('S30', 'P', 'channels')
    if not (a and b): return []
    for ch in a['anatomy']:
        x, y = a['anatomy'][ch], b['anatomy'][ch]
        L.append(f"| {ch} | {x['n']} | {x['mean_r']:.2f} ({x['null_r']:.2f}) | {x['paircorr_pre90']:.2f}→{x['paircorr_post90']:.2f} | {cp(*x['lead2'], 2)} | "
                 f"{y['n']} | {y['mean_r']:.2f} ({y['null_r']:.2f}) | {y['paircorr_pre90']:.2f}→{y['paircorr_post90']:.2f} | {cp(*y['lead2'], 2)} |")
    return L


def _ev(x):
    if x is None: return '—'
    if isinstance(x, dict): return ', '.join(f"{k}" + ('' if v.split('/')[0] == v.split('/')[1] else f" ({v} years defined)") for k, v in x.items())
    return ', '.join(str(i) for i in x)


def events_note(T):
    out = []
    for s in ('S26', 'S30'):
        for v, lab in ((s, 'primary (windows from 1962)'), (f'{s}_strict', 'strict inside 1970–2022')):
            q = extract(T, v)
            if not q: continue
            g = lambda q_, i: q_[i][2] if q_ and i in q_ and len(q_[i]) > 2 else None
            out.append(f"- **{s}, {lab}**: decomposition recession windows {_ev(g(q, 'D1'))}; MST pre-crisis {_ev(g(q, 'E4'))}; "
                       f"autocorrelation and variance pre-crisis {_ev(g(q, 'F1'))}; coupling post-crisis {_ev(g(q, 'F4'))}")
    return out


def write(root):
    T = Tree(root); meta = None
    for v in ('S30', 'S26'):
        p = os.path.join(root, v, 'P', 'arc.json')
        if os.path.exists(p): meta = json.load(open(p)); break
    L = ["# Phase 3 comparison — S26 and S30", "",
         f"Generated by `python -m ef.comparison` from `results/` (code {meta['code_version'] if meta else '?'}). Everything follows "
         "`docs/preregistration_S30.md` (signed 11 October 2026) and its amendments: convention P, rolling windows from 1962, "
         "the as-run seeds. Each S30 result is read against S26 under the same conventions (the S26 (P) column); the stored "
         "column shows the registry's S26 values (as stored, with Sid's corrections of 11 October), for reference.", "",
         "**How to read the flags.** *Sign change* or *crosses 0.05* compares S26 (P) with S30 (P). The last column applies "
         "the pre-registered criterion: *replicates*, *weakens* (same sign, p ≥ 0.05), *reverses*, *stays null* or *becomes "
         "significant*; descriptive quantities *hold* or *do not hold*. " + FLOORS + ". The lead rests on 2009 and 2020 "
         "(n ≈ 2): read A1 and A2 as a property of the modern economy, not a fifty-year law.", "",
         ] + ([open(os.path.join(root, 'SUMMARY.md')).read().strip(), ""] if os.path.exists(os.path.join(root, 'SUMMARY.md')) else []) + [
         "## 1. Every registry quantity", ""] + main_table(T)
    L += ["", "Recessions each rolling test actually uses (with defined years of each pre-crisis window):", ""] + events_note(T)
    L += ["", "## 2. Phase conventions: the arc and the r–swing-size link (circular shift)", ""] + conventions_table(T)
    L += ["", "## 3. Phase conventions: the surrogate tests", ""] + surrogate_conventions_table(T)
    L += ["", "## 4. The arc without 2020, under P and the edge-robust E (open issue 2)", ""] + edge_table(T)
    L += ["", "## 5. Past data only (convention C; open issue 14, rule 7)", ""] + past_only_table(T)
    L += ["", "## 6. Leaving each added economy out (S30; mandatory)", "",
          "A flag marks a result that reverses sign or crosses p = 0.05 when the economy is dropped (compared with S30).", ""] + dependence_table(T)
    ids = ['C1', 'C2', 'D1', 'D3', 'D4', 'D7', 'D8', 'D11']
    L += ["", "## 7. Iran and Saudi Arabia in the swing-size tests (S30; mandatory)", ""] + variant_table(
        T, None, [('S30', 'S30'), ('without Iran', 'S30_minus_IRN'), ('without Saudi Arabia', 'S30_minus_SAU'), ('without both', 'S30_minus_IRN_SAU')], ids)
    ids = ['D1', 'D3', 'D4', 'D7', 'D8', 'D9', 'E1', 'E4', 'E6', 'F1', 'F2', 'F4']
    L += ["", "## 8. Rolling windows: primary (from 1962) and strict inside 1970–2022", ""] + variant_table(
        T, None, [('S26 primary', 'S26'), ('S26 strict', 'S26_strict'), ('S30 primary', 'S30'), ('S30 strict', 'S30_strict')], ids)
    ids = ['A1', 'A2', 'A3', 'A5', 'C1', 'D1', 'D3']
    L += ["", "## 9. Norway, Switzerland and South Africa with GMD growth for 1991–2011 (open issue 13)", ""] + variant_table(
        T, None, [('S26', 'S26'), ('S26, GMD growth', 'S26_gmd_growth'), ('S30', 'S30'), ('S30, GMD growth', 'S30_gmd_growth')], ids)
    L += ["", "## 10. Robustness rows (registry B1–B15), S26 and S30 under P", ""] + robustness_table(T)
    L += ["", "## 11. Leave each of the 30 economies out (S30, arc)", ""] + loo_table(T)
    L += ["", "## 12. Channel anatomy on the repaired panel (open issue 12)", ""] + anatomy_table(T)
    out = os.path.join(root, 'COMPARISON.md'); open(out, 'w').write("\n".join(L) + "\n"); return out


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('--results', default=os.path.join(config.repo_root(), 'results'))
    print(f"wrote {write(ap.parse_args(argv).results)}")


if __name__ == '__main__':
    main()
