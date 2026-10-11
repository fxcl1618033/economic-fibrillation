"""
crisis_analysis.py
==================
MAIN JOB: measure business-cycle synchronization r(t) for every year, then ask
how it behaves around the four TRULY GLOBAL crises, and whether it is genuinely
elevated in those windows vs normal years (and vs regional crises).

Pipeline (all classical measurement, no ML):
  ln GDP -> Butterworth band-pass -> Hilbert phase -> Kuramoto order parameter r(t)
Data: World Bank GDP, current US$, 26 economies. Filter run on the long window
(1960-2023 where available) so the 1973-75 window is clean; analysis 1970-2022.
"""
import csv, json
import numpy as np
from collections import defaultdict
from scipy.signal import butter, filtfilt, hilbert
import matplotlib.pyplot as plt

RNG = np.random.default_rng(7)

# ---------------- load ----------------
data = defaultdict(dict)
for row in csv.DictReader(open("gdp.csv")):
    c = row["Country Code"]
    try: y = int(row["Year"]); v = float(row["Value"])
    except: continue
    data[c][y] = v
codes = ['USA','GBR','DEU','FRA','ITA','JPN','CAN','ESP','AUS','KOR','IND','MEX','NLD','SWE',
         'CHE','BEL','ZAF','TUR','NOR','AUT','DNK','FIN','GRC','PRT','IDN','THA']
label = {'USA':'United States','GBR':'United Kingdom','DEU':'Germany','FRA':'France','ITA':'Italy',
 'JPN':'Japan','CAN':'Canada','ESP':'Spain','AUS':'Australia','KOR':'South Korea','IND':'India',
 'MEX':'Mexico','NLD':'Netherlands','SWE':'Sweden','CHE':'Switzerland','BEL':'Belgium','ZAF':'South Africa',
 'TUR':'Turkey','NOR':'Norway','AUT':'Austria','DNK':'Denmark','FIN':'Finland','GRC':'Greece',
 'PRT':'Portugal','IDN':'Indonesia','THA':'Thailand'}

FS, LO, HI = 1.0, 1/9.0, 0.49
b, a = butter(2, [LO/(FS/2), HI/(FS/2)], btype="band")

# per-country: band-pass + Hilbert on the longest available window, then index phase by year
phase_by_year = {}          # code -> {year: phase}
for c in codes:
    yrs = [y for y in range(1960, 2024) if y in data[c]]
    yrs = list(range(min(yrs), max(yrs)+1))         # contiguous
    g = np.array([data[c][y] for y in yrs], float)
    cyc = filtfilt(b, a, np.log(g) - np.log(g).mean())
    ph = np.angle(hilbert(cyc))
    phase_by_year[c] = {y: ph[i] for i, y in enumerate(yrs)}

# ---------------- order parameter r(t) on 1970-2022 ----------------
YEARS = np.arange(1970, 2023)
N = len(codes)
R = np.array([np.abs(np.mean([np.exp(1j*phase_by_year[c][y]) for c in codes])) for y in YEARS])

# ---------------- crisis definitions ----------------
GLOBAL = {
 "Oil shock I (1973-75)":            [1973, 1974, 1975],
 "Oil shock II / Volcker (1980-82)": [1980, 1981, 1982],
 "Global Financial Crisis (2007-09)":[2007, 2008, 2009],
 "COVID-19 (2020)":                  [2020],
}
REGIONAL = {
 "Asian financial crisis (1997-98)": [1997, 1998],
 "Euro debt crisis (2011-12)":       [2011, 2012],
}
g_years = sorted(sum(GLOBAL.values(), []))
r_years = sorted(sum(REGIONAL.values(), []))
def ridx(yrs): return np.array([np.where(YEARS==y)[0][0] for y in yrs])
gmask = np.isin(YEARS, g_years)
rmask = np.isin(YEARS, r_years)
nmask = ~(gmask | rmask)

R_by_year = {int(y): float(R[i]) for i, y in enumerate(YEARS)}
def pct(y): return float((R < R_by_year[y]).mean()*100)   # percentile of that year's r

mean_global = float(R[gmask].mean())
mean_regional = float(R[rmask].mean())
mean_normal = float(R[nmask].mean())

# ---------------- relative test: circular-shift permutation ----------------
true_contrast = float(R[gmask].mean() - R[~gmask].mean())
T = len(YEARS); nperm = 20000
null = np.empty(nperm)
for k in range(nperm):
    m = np.roll(gmask, RNG.integers(1, T))
    null[k] = R[m].mean() - R[~m].mean()
p_perm = float((1 + (null >= true_contrast).sum()) / (1 + nperm))

# bootstrap CIs for the three group means (resample years within group)
def boot_ci(vals, nb=10000):
    vals = np.asarray(vals)
    bs = [RNG.choice(vals, len(vals), replace=True).mean() for _ in range(nb)]
    return float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
ci_g = boot_ci(R[gmask]); ci_r = boot_ci(R[rmask]); ci_n = boot_ci(R[nmask])

# ---------------- superposed epoch (composite around onset) ----------------
onsets = [1973, 1980, 2007, 2020]; lags = np.arange(-4, 5)
comp = []
for on in onsets:
    row = []
    for L in lags:
        y = on + L
        row.append(R_by_year.get(y, np.nan))
    comp.append(row)
comp = np.array(comp)
comp_mean = np.nanmean(comp, axis=0); comp_sd = np.nanstd(comp, axis=0)

# ================= FIGURES =================
plt.rcParams.update({"figure.dpi":140,"font.size":10,"axes.spines.top":False,
                     "axes.spines.right":False,"axes.grid":True,"grid.alpha":0.25})
GC, RC = "#2a9d8f", "#e9c46a"

# fig 1: overview
fig, ax = plt.subplots(figsize=(11, 4.2))
for lab, ys in GLOBAL.items():
    ax.axvspan(min(ys)-0.5, max(ys)+0.5, color=GC, alpha=0.25)
for lab, ys in REGIONAL.items():
    ax.axvspan(min(ys)-0.5, max(ys)+0.5, color=RC, alpha=0.35)
ax.plot(YEARS, R, color="#1d3557", lw=2.2)
ax.axhline(mean_normal, color="grey", ls=":", lw=1)
ax.text(YEARS[1], mean_normal+0.01, "normal-year average", fontsize=8, color="grey")
ax.set_ylim(0,1); ax.set_xlim(YEARS[0], YEARS[-1])
ax.set_title("Synchronization r(t) with global (green) and regional (yellow) crisis windows", loc="left")
ax.set_xlabel("year"); ax.set_ylabel("r  (synchronization)")
fig.savefig("cfig1_overview.png", bbox_inches="tight"); fig.savefig("cfig1_overview.pdf", bbox_inches="tight"); plt.close(fig)

# fig 2: per-crisis zoom
fig, axes = plt.subplots(2, 2, figsize=(11, 7)); axes = axes.ravel()
for ax, (lab, ys) in zip(axes, GLOBAL.items()):
    lo, hi = min(ys)-4, max(ys)+4
    yy = np.arange(lo, hi+1)
    rr = [R_by_year.get(int(y), np.nan) for y in yy]
    ax.plot(yy, rr, color="#1d3557", lw=2, marker="o", ms=4)
    ax.axvspan(min(ys)-0.5, max(ys)+0.5, color=GC, alpha=0.25)
    ax.axhline(mean_normal, color="grey", ls=":", lw=1)
    ax.set_title(lab, fontsize=10, loc="left"); ax.set_ylim(0,1)
    ax.set_ylabel("r")
fig.suptitle("Zoom: how synchronization approaches, peaks at, and follows each global crisis", fontsize=12)
fig.tight_layout(); fig.savefig("cfig2_zoom.png", bbox_inches="tight"); fig.savefig("cfig2_zoom.pdf", bbox_inches="tight"); plt.close(fig)

# fig 3: superposed epoch
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.fill_between(lags, comp_mean-comp_sd, comp_mean+comp_sd, color=GC, alpha=0.2, label="±1 sd across crises")
ax.plot(lags, comp_mean, color="#1d3557", lw=2.3, marker="o", label="mean r across 4 crises")
ax.axvline(0, color="#e63946", lw=1.2, ls="--", label="crisis onset")
ax.axhline(mean_normal, color="grey", ls=":", lw=1, label="normal-year average")
ax.set_xlabel("years relative to crisis onset"); ax.set_ylabel("r"); ax.set_ylim(0,1)
ax.set_title("Composite (superposed-epoch) synchronization around global-crisis onsets", loc="left", fontsize=10.5)
ax.legend(fontsize=8, framealpha=0.9)
fig.savefig("cfig3_composite.png", bbox_inches="tight"); fig.savefig("cfig3_composite.pdf", bbox_inches="tight"); plt.close(fig)

# fig 4: permutation null
fig, ax = plt.subplots(figsize=(7.5, 4))
ax.hist(null, bins=60, color="#adb5bd", edgecolor="white")
ax.axvline(true_contrast, color="#e63946", lw=2.4, label=f"real contrast = {true_contrast:+.3f}")
ax.set_title(f"Relative test: global-crisis synchronization vs randomly placed windows (p = {p_perm:.3f})", loc="left", fontsize=10)
ax.set_xlabel("mean r(crisis) − mean r(rest), under random window placement"); ax.set_yticks([])
ax.legend(fontsize=9)
fig.savefig("cfig4_permutation.png", bbox_inches="tight"); fig.savefig("cfig4_permutation.pdf", bbox_inches="tight"); plt.close(fig)

# fig 5: group means with CIs
fig, ax = plt.subplots(figsize=(6.5, 4))
groups = ["Global\ncrises", "Regional\ncrises", "Normal\nyears"]
means = [mean_global, mean_regional, mean_normal]
cis = [ci_g, ci_r, ci_n]
errs = [[m-lo for m,(lo,hi) in zip(means,cis)],[hi-m for m,(lo,hi) in zip(means,cis)]]
ax.bar(groups, means, color=[GC, RC, "#adb5bd"], yerr=errs, capsize=6, edgecolor="white")
for i,m in enumerate(means): ax.text(i, m+0.02, f"{m:.2f}", ha="center", fontsize=10)
ax.set_ylim(0,1); ax.set_ylabel("mean r"); ax.set_title("Average synchronization by period type (95% bootstrap CI)", loc="left", fontsize=10.5)
fig.savefig("cfig5_groups.png", bbox_inches="tight"); fig.savefig("cfig5_groups.pdf", bbox_inches="tight"); plt.close(fig)

# ================= SAVE RESULTS =================
results = {
 "N": N, "analysis_window": [int(YEARS[0]), int(YEARS[-1])],
 "band_years": [round(1/HI,1), round(1/LO,1)], "filter_order": 2,
 "r_by_year": R_by_year,
 "GLOBAL": GLOBAL, "REGIONAL": REGIONAL,
 "mean_global": mean_global, "mean_regional": mean_regional, "mean_normal": mean_normal,
 "ci_global": ci_g, "ci_regional": ci_r, "ci_normal": ci_n,
 "true_contrast": true_contrast, "p_perm": p_perm, "nperm": nperm,
 "crisis_percentiles": {int(y): round(pct(y),1) for y in g_years},
 "regional_percentiles": {int(y): round(pct(y),1) for y in r_years},
 "composite_lags": lags.tolist(), "composite_mean": comp_mean.tolist(), "composite_sd": comp_sd.tolist(),
 "peak_year": int(YEARS[R.argmax()]), "peak_R": float(R.max()),
 "trough_year": int(YEARS[R.argmin()]), "trough_R": float(R.min()),
}
json.dump(results, open("crisis_results.json","w"), indent=2)

# console summary
print("=== r by year (global-crisis years in []) ===")
for y in YEARS:
    tag = " [GLOBAL]" if y in g_years else (" (regional)" if y in r_years else "")
    print(f"  {y}: {R_by_year[int(y)]:.2f}{tag}")
print(f"\nmean r  global={mean_global:.3f}  regional={mean_regional:.3f}  normal={mean_normal:.3f}")
print(f"relative test (global vs rest): contrast={true_contrast:+.3f}, p={p_perm:.4f}")
print(f"peak r={results['peak_R']:.2f} ({results['peak_year']}); trough r={results['trough_R']:.2f} ({results['trough_year']})")
print("crisis-year percentiles:", results["crisis_percentiles"])
print("regional-year percentiles:", results["regional_percentiles"])
print("saved figures cfig1..cfig5 and crisis_results.json")
