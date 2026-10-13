"""Validation report per economy: Maddison coverage and gaps, year-on-year moves above 15%, cycle size, coverage of
the main macro series in the atlas panel, and the atlas data repairs in plain words.

    python -m ef.data.validate [--data build/data]     # writes <data>/VALIDATION.md and docs/data_validation.md
"""
import argparse
import json
import os
import shutil

import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt

from ef import config
from ef.data import maddison

NAMES = {'USA': 'United States', 'GBR': 'United Kingdom', 'DEU': 'Germany', 'FRA': 'France', 'ITA': 'Italy', 'JPN': 'Japan',
         'CAN': 'Canada', 'ESP': 'Spain', 'AUS': 'Australia', 'KOR': 'South Korea', 'IND': 'India', 'MEX': 'Mexico',
         'NLD': 'Netherlands', 'SWE': 'Sweden', 'CHE': 'Switzerland', 'BEL': 'Belgium', 'ZAF': 'South Africa', 'TUR': 'Turkey',
         'NOR': 'Norway', 'AUT': 'Austria', 'DNK': 'Denmark', 'FIN': 'Finland', 'GRC': 'Greece', 'PRT': 'Portugal',
         'IDN': 'Indonesia', 'THA': 'Thailand', 'CHN': 'China', 'BRA': 'Brazil', 'SAU': 'Saudi Arabia', 'IRN': 'Iran',
         'ARE': 'United Arab Emirates', 'RUS': 'Russia'}
# the main macro series a GNN node would carry (atlas panel column: label)
SERIES = {'growth': 'growth', 'c_C': 'demand split', 'govexp_GDP': 'spending', 'govdef_GDP': 'balance',
          'govdebt_GDP': 'debt', 'infl': 'inflation', 'strate': 'short rate', 'ltrate': 'long rate',
          'real_money_growth': 'real money', 'CA_GDP': 'current acct', 'unemp': 'unemployment'}
# events behind large Maddison moves for the added economies (docs/open_issues.md, issue 17)
EVENTS = {('CHN', 1961): 'Great Leap famine', ('SAU', 1973): 'oil price', ('SAU', 1983): 'oil price',
          ('SAU', 1991): 'oil, Gulf war', ('IRN', 1978): 'revolution', ('IRN', 1979): 'revolution', ('IRN', 1980): 'revolution, war'}
BIG = 15.0


def repairs(fx):
    """The atlas repairs for one economy (meta.json 'fixes'), in plain words."""
    out = []
    if 'gdp_from' in fx: out.append(f"GMD GDP used only from {fx['gdp_from']} (earlier levels are spliced estimates)")
    if 'components_from' in fx: out.append(f"expenditure components only from {fx['components_from']} (earlier ones do not add up to GDP)")
    if 'contrib_from' in fx: out.append(f"demand contributions only from {fx['contrib_from']} (deflation unreliable through high inflation)")
    if 'infl_from' in fx: out.append(f"inflation only from {fx['infl_from']} (earlier values are a placeholder)")
    if 'strate_is_policy_rate' in fx: a, b = fx['strate_is_policy_rate']; out.append(f"short rate is the central bank's policy rate, {a}–{b}")
    for y, g, p in fx.get('growth_patch', []): out.append(f"growth in {y} replaced by Penn World Table's ({g}% → {p}%)")
    if 'contrib_blank' in fx: out.append(f"demand contributions blanked in {', '.join(map(str, fx['contrib_blank']))} (C + I + NX miss GDP growth by more than 3 points)")
    v = fx.get('contrib_validation', {})
    out.append(f"contributions deflated by {'consumer prices' if fx.get('contrib_method') == 'cpi' else 'the GDP deflator'} "
               f"(correlation with Penn World Table volumes: C {v.get('C')}, I {v.get('I')}, NX {v.get('NX')})")
    f = fx.get('fiscal', {})
    if f:
        s = f"budget from IMF WEO from {f['weo_from']}"
        if f.get('hist_from'): s += f", extended back to {f['hist_from']} with IMF FPP"
        elif 'hist_gap_too_large' in f: s += (", no earlier history (WEO and FPP disagree by " + f"{f['hist_gap_too_large'][0]} and {f['hist_gap_too_large'][1]} points)" if f['hist_gap_too_large'] else ", no earlier history")
        if f.get('breaks'): s += f"; coverage break in {', '.join(map(str, f['breaks']))}"
        out.append(s)
    d = fx.get('debt', {})
    if d:
        s = f"debt from IMF WEO from {d['weo_from']}"
        if d.get('hdd_ratio'): s += f", extended back with IMF HDD (scaled by {d['hdd_ratio']})"
        elif d.get('hdd_ratio_too_far'): s += f", no earlier history (HDD differs by a factor {d['hdd_ratio_too_far']})"
        out.append(s)
    if 'debt_gapfill' in fx: out.append(f"debt gaps filled from GMD in {', '.join(map(str, fx['debt_gapfill']))}")
    if 'debt_interp' in fx: out.append(f"debt interpolated in {', '.join(map(str, fx['debt_interp']))}")
    if 'money_dropped' in fx: out.append(f"money growth dropped in {', '.join(map(str, fx['money_dropped']))} (definitional breaks)")
    if 'ltrate_dropped' in fx: out.append(f"long rate dropped in {', '.join(map(str, fx['ltrate_dropped']))} (placeholder value)")
    if 'unemp_break' in fx: out.append(f"unemployment break in {fx['unemp_break']} (survey change)")
    if 'alt_growth' in fx:
        g = fx['alt_growth']
        out.append(f"official growth kept: {g['official_mean_1978_2019']}% a year 1978–2019, against {g['pwt_mean_1978_2019']}% in Penn World Table")
    return out


OTHER = {'RUS': 'Russia', 'POL': 'Poland', 'ARG': 'Argentina', 'TWN': 'Taiwan', 'PAK': 'Pakistan', 'EGY': 'Egypt',
         'NGA': 'Nigeria', 'UKR': 'Ukraine', 'VEN': 'Venezuela', 'PHL': 'Philippines', 'IRQ': 'Iraq', 'COL': 'Colombia'}


def world_section(md, samples, years=(1970, 1990, 2022)):
    """Each sample's share of world real GDP, and the largest economies outside S30 (the inclusion rule decides only
    among candidates; this shows which large economies are not candidates)."""
    sh = {s: maddison.world_share(md, isos) for s, isos in samples.items()}
    L = ["## Share of world GDP", "",
         "Real GDP (GDP per capita × population, Maddison's 2011 PPP dollars) as a share of the world total. The world is "
         "every Maddison entity, with the former USSR, Czechoslovakia and Yugoslavia counted as the aggregates Maddison "
         "gives for them, so nothing is counted twice; North Korea has no data before 1990.", "",
         "| Sample | " + " | ".join(map(str, years)) + " | Mean 1970–2022 |", "|---|" + "---|" * (len(years) + 1)]
    for s, w in sh.items():
        L.append(f"| {s} | " + " | ".join(f"{100 * w[y]:.1f}%" for y in years) + f" | {100 * w.loc[1970:2022].mean():.1f}% |")
    main = list(samples)[-1]
    L += ["", f"Largest economies outside {main}, by mean real GDP 1970–2022:", "",
          "| Economy | Mean real GDP 1970–2022 (trillion 2011 PPP dollars) | Maddison 1950–2022 |", "|---|---|---|"]
    for iso, v, ok in maddison.largest_outside(md, samples[main]):
        L.append(f"| {OTHER.get(iso, iso)} | {v / 1e9:.2f} | {'complete' if ok else 'incomplete'} |")
    return L + [""]


def report(data_dir):
    cfg = config.load(); y0, y1 = cfg['years']
    md = maddison.load()
    meta = json.load(open(os.path.join(data_dir, 'atlas_s31', 'meta.json'))); fixes = meta['fixes']
    P = pd.read_csv(os.path.join(data_dir, 'atlas_s31', 'panel.csv'))      # the atlas panel with Russia (amendment 3)
    s26, s30, s31 = config.sample('S26'), config.sample('S30'), config.sample('S31'); added = [i for i in s31 if i not in s26]
    allx = s31 + list(cfg['excluded'])
    b, a = butter(2, [(1/9)/0.5, 0.49/0.5], btype='band')

    info = {}
    for iso in allx:
        g = maddison.gaps(md, iso)
        d = md[(md.ISO == iso) & md.year.between(y0, y1)].set_index('year').gdppc.reindex(range(y0, y1 + 1))
        ch = 100 * d.pct_change()
        moves = [(int(y), float(v)) for y, v in ch.items() if abs(v) > BIG]
        sd = None
        if not any(g.values()):
            x = np.log(d.values); c = filtfilt(b, a, x - x.mean()); sd = 100 * float(np.std(c[(d.index >= 1970)]))
        w = P[(P.iso == iso) & P.year.between(1970, 2022)].set_index('year')
        cov = {lab: (float(w[col].notna().mean()), int(w[col].first_valid_index()) if w[col].notna().any() else None) for col, lab in SERIES.items()}
        info[iso] = dict(gaps=g, moves=moves, sd=sd, cov=cov, ok=not any(g.values()))
    med26 = float(np.median([info[i]['sd'] for i in s26]))

    L = [f"# Data validation — S31 main sample (S30 + Russia; pre-registration amendment 3)", "",
         f"Generated by `make data` (`python -m ef.data.validate`) from the pinned sources in `data/sources.yaml`. "
         f"Maddison 2023 for the cycles (Paper 1); the atlas panel (Global Macro Database, repaired) for the macro series.", "",
         "## Inclusion rule", "",
         f"An economy enters if its Maddison GDP per capita and population are complete for every year {y0}–{y1}, with no "
         "interpolation and no splices (open issue 17; S30 confirmed by Sid on 11 October 2026; Russia added on 13 October 2026).", ""]
    for iso in allx:
        if not info[iso]['ok']:
            L.append(f"- **{NAMES[iso]} fails**: Maddison GDP per capita is missing in {', '.join(map(str, info[iso]['gaps']['gdppc']))}"
                     f"{' and population in ' + ', '.join(map(str, info[iso]['gaps']['pop'])) if info[iso]['gaps']['pop'] else ''}. Excluded; no S31 run.")
    n_ok = sum(info[i]['ok'] for i in s31)
    L += [f"- All {n_ok} of the {len(s31)} S31 economies pass.", ""]
    L += world_section(md, {'S26': s26, 'S30': s30, 'S31': s31})
    L += ["## The five added economies", "",
          f"Cycle size is the standard deviation of the 2–9 year cycle in log GDP per capita, 1970–2022, in percent; the median of the 26 is {med26:.2f}%.", ""]
    for iso in added:
        x = info[iso]
        L += [f"### {NAMES[iso]}", "",
              f"- **Maddison:** complete {y0}–{y1}. Cycle size {x['sd']:.2f}% ({x['sd'] / med26:.1f}× the median of the 26).",
              "- **Moves above 15% in a year:** " + ("; ".join(f"{y} {v:+.1f}%" + (f" ({EVENTS[(iso, y)]})" if (iso, y) in EVENTS else "") for y, v in x['moves']) or "none") + ".",
              "- **Macro series, 1970–2022 (share of years filled, first year):** " + "; ".join(f"{lab} {s:.0%}" + (f" from {f}" if f and f > 1970 else "") for lab, (s, f) in x['cov'].items()) + ".",
              "- **Atlas repairs:** " + "; ".join(repairs(fixes[iso])) + ".", ""]
        if iso == 'CHN':
            dd = md[(md.ISO == 'CHN') & md.year.between(1977, 2019)].set_index('year').gdppc
            pp = md[(md.ISO == 'CHN') & md.year.between(1977, 2019)].set_index('year')['pop']
            mg = 100 * float(np.exp(np.mean(np.diff(np.log((dd * pp).values)))) - 1)
            L += [f"  China's growth differs by source. Maddison's real GDP (per capita × population) grows {mg:.1f}% a year in 1978–2019, "
                  f"against the official {fixes['CHN']['alt_growth']['official_mean_1978_2019']}% in the atlas and "
                  f"{fixes['CHN']['alt_growth']['pwt_mean_1978_2019']}% in Penn World Table. Paper 1's cycles use Maddison; the atlas "
                  "uses the official series.", ""]
        if iso == 'RUS':
            G = maddison.gdp_by_year(md, (1950, 2022)); g = 100 * G[['RUS', 'SUN']].pct_change(); sh = G.RUS / G.SUN
            dg = (g.RUS - g.SUN).loc[1951:1990].abs().max()
            gm = P[P.iso == 'RUS'].set_index('year').growth; mg = 100 * G.RUS.pct_change()
            dis = [int(y) for y in range(1951, 2023) if abs(gm.get(y, np.nan) - mg.get(y, np.nan)) > 2]
            L += ["  Russia's values before 1991 are not market national accounts: they are back-cast estimates for the Russian "
                  "part of the Soviet planned economy. How they were made is not documented in the Maddison sources we found "
                  "(Bolt and van Zanden 2024), and they are not a fixed share of Maddison's own USSR series: Russia's share of USSR GDP in Maddison "
                  f"rises from {100 * sh[1950]:.0f}% in 1950 to {100 * sh[1980]:.0f}% in 1980, and the two growth rates differ "
                  f"by up to {dg:.1f} points a year in 1951–1990. Maddison gives the other Soviet republics only for 1973 before "
                  "1990. The pre-registered sensitivity run computes Russia's phases from 1992 only, so these "
                  "years cannot drive the result.", "",
                  f"  The Global Macro Database (the atlas panel) and Maddison disagree on Russia's growth by more than 2 points "
                  f"in {len(dis)} years ({', '.join(map(str, dis))}); Penn World Table, the third source used to settle such "
                  "disagreements, starts in 1990 and from 1991 matches the database. No growth patch is made (the rule needs "
                  "two sources against one). Soviet-era inflation in the database is near zero (administered prices), "
                  "and money (M2) is missing.", ""]
    L += ["## Every economy", "",
          "| Economy | Sample | Maddison 1950–2022 | Moves above 15% | Cycle size | " + " | ".join(SERIES.values()) + " |",
          "|---|---|---|---|---|" + "---|" * len(SERIES)]
    for iso in allx:
        x = info[iso]
        smp = 'S26' if iso in s26 else ('added' if iso in s30 else 'excluded')
        mad = 'complete' if x['ok'] else 'missing ' + ', '.join(map(str, x['gaps']['gdppc']))
        mv = ', '.join(str(y) for y, _ in x['moves']) or '—'
        sd = f"{x['sd']:.2f}%" if x['sd'] is not None else '—'
        L.append(f"| {NAMES[iso]} | {smp} | {mad} | {mv} | {sd} | " + " | ".join(f"{s:.0%}" for s, _ in x['cov'].values()) + " |")
    L += ["", "## Atlas repairs, the 26", ""]
    for iso in s26:
        L.append(f"- **{NAMES[iso]}:** " + "; ".join(repairs(fixes[iso])) + ".")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('--data', default=os.path.join(config.load()['paths']['build'], 'data'))
    args = ap.parse_args(argv)
    text = report(args.data)
    out = os.path.join(args.data, 'VALIDATION.md'); open(out, 'w').write(text)
    shutil.copy(out, os.path.join(config.repo_root(), 'docs', 'data_validation.md'))
    print(f"wrote {out} and docs/data_validation.md")


if __name__ == '__main__':
    main()
