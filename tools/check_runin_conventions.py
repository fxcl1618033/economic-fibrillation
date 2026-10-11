"""
Pre-flight check written for the Claude Code handoff (11 Oct 2026).

Question: do the Paper 1 headline numbers depend on WHERE the Hilbert transform is applied?
Three conventions appear in the saved files:

  P  "paper"     band-pass on 1950-2022, Hilbert on the FULL 1950-2022 cycle, then keep 1970-2022.
                 Used by kose_terrones_test.py and robustness.py (the crisis-arc headline).
  W  "windowed"  band-pass on 1950-2022, cut to 1970-2022, THEN Hilbert.
                 Used by amplitude_test.py (+0.51) and by several companion-book figures.
  N  "no run-in" band-pass AND Hilbert on 1970-2022 only.

For each convention it recomputes r(t), the crisis arc (lags +2..-2, circular-shift permutation,
one-sided as in Methods 6.3) and the r-amplitude correlation (Methods 6.2), and checks the
P and W series against the stored results files.

Run from the repository root:
    python3 tools/check_runin_conventions.py --rda <path to MaddisonData.rda>
"""
import argparse, json, os
import numpy as np, pyreadr
from scipy.signal import butter, filtfilt, hilbert
from scipy.ndimage import gaussian_filter1d
from scipy.stats import pearsonr

ap = argparse.ArgumentParser()
ap.add_argument("--rda", default="data/raw/maddisondata/data/MaddisonData.rda")
ap.add_argument("--out", default="paper1/results/runin_convention_check.json")
args = ap.parse_args()

CODES = ['USA','GBR','DEU','FRA','ITA','JPN','CAN','ESP','AUS','KOR','IND','MEX','NLD','SWE',
         'CHE','BEL','ZAF','TUR','NOR','AUT','DNK','FIN','GRC','PRT','IDN','THA']
GLOBAL_REC = [1975, 1982, 1991, 2009, 2020]
YEARS = np.arange(1970, 2023); T = len(YEARS)
b, a = butter(2, [(1/9)/0.5, 0.49/0.5], btype='band')

md = pyreadr.read_r(args.rda)['MaddisonData']; md['year'] = md['year'].astype(int)

def cycles(start):
    out = []
    for c in CODES:
        d = md[(md.ISO == c) & (md.gdppc.notna()) & (md.year >= start)].sort_values('year')
        lg = np.log(d.gdppc.values.astype(float))
        out.append((d.year.values, filtfilt(b, a, lg - lg.mean())))
    return out

def z_convention(conv):
    if conv == "P":
        Z = []
        for yrs, cyc in cycles(1950):
            z = hilbert(cyc); s = dict(zip(yrs, z)); Z.append([s[y] for y in YEARS])
        return np.array(Z)
    if conv == "W":
        X = []
        for yrs, cyc in cycles(1950):
            s = dict(zip(yrs, cyc)); X.append([s[y] for y in YEARS])
        return hilbert(np.array(X), axis=-1)
    if conv == "N":
        X = []
        for yrs, cyc in cycles(1970):
            s = dict(zip(yrs, cyc)); X.append([s[y] for y in YEARS])
        return hilbert(np.array(X), axis=-1)

G = np.isin(YEARS, GLOBAL_REC).astype(float)
def lagcorr(x, g, lag):
    if lag > 0: u, v = x[:-lag], g[lag:]
    elif lag < 0: u, v = x[-lag:], g[:lag]
    else: u, v = x, g
    return pearsonr(u, v)[0]
def perm(x, lag, direction):
    obs = lagcorr(x, G, lag)
    null = np.array([lagcorr(x, np.roll(G, k), lag) for k in range(1, T)])
    p = (1 + np.sum(null >= obs)) / T if direction == 'pos' else (1 + np.sum(null <= obs)) / T
    return float(obs), float(p)
def perm_corr(x, y):
    obs = pearsonr(x, y)[0]
    null = np.array([pearsonr(x, np.roll(y, k))[0] for k in range(1, len(y))])
    return float(obs), float((1 + np.sum(null >= obs)) / (1 + len(null)))

ARC = [("lead2", 2, 'pos'), ("lead1", 1, 'pos'), ("crisis", 0, 'pos'), ("after1", -1, 'neg'), ("after2", -2, 'neg')]
res = {}
for conv in ["P", "W", "N"]:
    Z = z_convention(conv)
    r = np.abs(np.exp(1j * np.angle(Z)).mean(axis=0))
    A = np.abs(Z).mean(axis=0)
    arc = {lab: perm(r, lag, d) for lab, lag, d in ARC}
    amp_raw = perm_corr(r, A)
    amp_det = perm_corr(r - gaussian_filter1d(r, 8.0), A - gaussian_filter1d(A, 8.0))
    ep = np.array([[r[list(YEARS).index(o + k)] if (o + k) in YEARS else np.nan for k in range(-4, 5)] for o in GLOBAL_REC])
    res[conv] = {"arc": arc, "amp_raw": amp_raw, "amp_detrended": amp_det,
                 "epoch_mean_t-4..t+4": [float(v) for v in np.nanmean(ep, axis=0)],
                 "r_by_year": {int(y): float(v) for y, v in zip(YEARS, r)}}

# check against the stored files
def maxdiff(conv, path, key="r_by_year"):
    if not os.path.exists(path): return None
    stored = json.load(open(path))[key]
    return float(max(abs(res[conv]["r_by_year"][int(y)] - v) for y, v in stored.items() if v is not None))
checks = {"P_vs_kose_terrones_results": maxdiff("P", "paper1/results/kose_terrones_results.json"),
          "W_vs_amplitude_results": maxdiff("W", "paper1/results/amplitude_results.json")}

json.dump({"conventions": {"P": "Hilbert on 1950-2022 (paper)", "W": "Hilbert on 1970-2022 window after 1950 filter",
                           "N": "filter and Hilbert on 1970-2022"}, "checks": checks, "results": res},
          open(args.out, "w"), indent=1)
print("reproduction checks (max |diff| in r):", checks)
for conv in ["P", "W", "N"]:
    R = res[conv]
    print(f"\n[{conv}] arc: " + "  ".join(f"{k} {v[0]:+.3f} (p={v[1]:.3f})" for k, v in R['arc'].items()))
    print(f"     r-amplitude: raw {R['amp_raw'][0]:+.3f} (p={R['amp_raw'][1]:.3f})  detrended {R['amp_detrended'][0]:+.3f} (p={R['amp_detrended'][1]:.3f})")
    print("     epoch t-4..t+4: " + " ".join(f"{v:.2f}" for v in R['epoch_mean_t-4..t+4']))
