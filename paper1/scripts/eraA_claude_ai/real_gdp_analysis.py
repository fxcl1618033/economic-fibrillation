"""
real_gdp_analysis.py
====================
IDENTICAL pipeline to crisis_analysis.py, but on REAL GDP per capita
(Maddison Project Database 2023: constant international dollars, inflation- and
PPP-adjusted, to 2022). This is the constant-price robustness run.
"""
import json
import numpy as np
import pyreadr
from scipy.signal import butter, filtfilt, hilbert
import matplotlib.pyplot as plt

RNG = np.random.default_rng(7)

# ---------------- load Maddison real GDP per capita ----------------
md = pyreadr.read_r("MaddisonData-main/data/MaddisonData.rda")["MaddisonData"]
md["year"] = md["year"].astype(int)
codes = ['USA','GBR','DEU','FRA','ITA','JPN','CAN','ESP','AUS','KOR','IND','MEX','NLD','SWE',
         'CHE','BEL','ZAF','TUR','NOR','AUT','DNK','FIN','GRC','PRT','IDN','THA']

FS, LO, HI = 1.0, 1/9.0, 0.49
b, a = butter(2, [LO/(FS/2), HI/(FS/2)], btype="band")

phase_by_year = {}
for c in codes:
    d = md[(md.ISO == c) & (md.gdppc.notna())].sort_values("year")
    yrs = d.year.values; g = d.gdppc.values.astype(float)
    # contiguous from first year with data (use 1950+ for filter room where available)
    keep = yrs >= 1950
    yrs, g = yrs[keep], g[keep]
    cyc = filtfilt(b, a, np.log(g) - np.log(g).mean())
    ph = np.angle(hilbert(cyc))
    phase_by_year[c] = {int(y): ph[i] for i, y in enumerate(yrs)}

YEARS = np.arange(1970, 2023)
N = len(codes)
R = np.array([np.abs(np.mean([np.exp(1j*phase_by_year[c][int(y)]) for c in codes])) for y in YEARS])

# ---------------- crisis definitions (identical) ----------------
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
g_years = sorted(sum(GLOBAL.values(), [])); r_years = sorted(sum(REGIONAL.values(), []))
gmask = np.isin(YEARS, g_years); rmask = np.isin(YEARS, r_years); nmask = ~(gmask | rmask)
R_by_year = {int(y): float(R[i]) for i, y in enumerate(YEARS)}
def pct(y): return float((R < R_by_year[y]).mean()*100)
mean_global, mean_regional, mean_normal = float(R[gmask].mean()), float(R[rmask].mean()), float(R[nmask].mean())

true_contrast = float(R[gmask].mean() - R[~gmask].mean())
T = len(YEARS); nperm = 20000
null = np.array([R[np.roll(gmask, RNG.integers(1, T))].mean() - R[~np.roll(gmask, 0)].mean() for _ in range(0)])  # placeholder
null = np.empty(nperm)
for k in range(nperm):
    m = np.roll(gmask, RNG.integers(1, T)); null[k] = R[m].mean() - R[~m].mean()
p_perm = float((1 + (null >= true_contrast).sum()) / (1 + nperm))

def boot_ci(vals, nb=10000):
    vals = np.asarray(vals); bs = [RNG.choice(vals, len(vals), replace=True).mean() for _ in range(nb)]
    return float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
ci_g, ci_r, ci_n = boot_ci(R[gmask]), boot_ci(R[rmask]), boot_ci(R[nmask])

onsets = [1973, 1980, 2007, 2020]; lags = np.arange(-4, 5)
comp = np.array([[R_by_year.get(on+L, np.nan) for L in lags] for on in onsets])
comp_mean, comp_sd = np.nanmean(comp, axis=0), np.nanstd(comp, axis=0)

# ---------------- figures (suffix rfig) ----------------
plt.rcParams.update({"figure.dpi":140,"font.size":10,"axes.spines.top":False,
                     "axes.spines.right":False,"axes.grid":True,"grid.alpha":0.25})
GC, RC = "#2a9d8f", "#e9c46a"
TAG = "REAL GDP (Maddison 2023, constant int-$)"

fig, ax = plt.subplots(figsize=(11, 4.2))
for ys in GLOBAL.values(): ax.axvspan(min(ys)-0.5, max(ys)+0.5, color=GC, alpha=0.25)
for ys in REGIONAL.values(): ax.axvspan(min(ys)-0.5, max(ys)+0.5, color=RC, alpha=0.35)
ax.plot(YEARS, R, color="#1d3557", lw=2.2); ax.axhline(mean_normal, color="grey", ls=":", lw=1)
ax.text(YEARS[1], mean_normal+0.01, "normal-year average", fontsize=8, color="grey")
ax.set_ylim(0,1); ax.set_xlim(YEARS[0], YEARS[-1])
ax.set_title(f"Synchronization r(t) — {TAG}", loc="left")
ax.set_xlabel("year"); ax.set_ylabel("r  (synchronization)")
fig.savefig("rfig1_overview.png", bbox_inches="tight"); fig.savefig("rfig1_overview.pdf", bbox_inches="tight"); plt.close(fig)

fig, axes = plt.subplots(2, 2, figsize=(11, 7)); axes = axes.ravel()
for ax, (lab, ys) in zip(axes, GLOBAL.items()):
    yy = np.arange(min(ys)-4, max(ys)+5)
    ax.plot(yy, [R_by_year.get(int(y), np.nan) for y in yy], color="#1d3557", lw=2, marker="o", ms=4)
    ax.axvspan(min(ys)-0.5, max(ys)+0.5, color=GC, alpha=0.25); ax.axhline(mean_normal, color="grey", ls=":", lw=1)
    ax.set_title(lab, fontsize=10, loc="left"); ax.set_ylim(0,1); ax.set_ylabel("r")
fig.suptitle(f"Zoom around each global crisis — {TAG}", fontsize=12); fig.tight_layout()
fig.savefig("rfig2_zoom.png", bbox_inches="tight"); fig.savefig("rfig2_zoom.pdf", bbox_inches="tight"); plt.close(fig)

fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.fill_between(lags, comp_mean-comp_sd, comp_mean+comp_sd, color=GC, alpha=0.2, label="±1 sd across crises")
ax.plot(lags, comp_mean, color="#1d3557", lw=2.3, marker="o", label="mean r across 4 crises")
ax.axvline(0, color="#e63946", lw=1.2, ls="--", label="crisis onset"); ax.axhline(mean_normal, color="grey", ls=":", lw=1, label="normal-year average")
ax.set_xlabel("years relative to crisis onset"); ax.set_ylabel("r"); ax.set_ylim(0,1)
ax.set_title(f"Composite synchronization around crises — {TAG}", loc="left", fontsize=10)
ax.legend(fontsize=8, framealpha=0.9)
fig.savefig("rfig3_composite.png", bbox_inches="tight"); fig.savefig("rfig3_composite.pdf", bbox_inches="tight"); plt.close(fig)

fig, ax = plt.subplots(figsize=(7.5, 4))
ax.hist(null, bins=60, color="#adb5bd", edgecolor="white")
ax.axvline(true_contrast, color="#e63946", lw=2.4, label=f"real contrast = {true_contrast:+.3f}")
ax.set_title(f"Relative test (p = {p_perm:.3f}) — {TAG}", loc="left", fontsize=10)
ax.set_xlabel("mean r(crisis) - mean r(rest), random window placement"); ax.set_yticks([]); ax.legend(fontsize=9)
fig.savefig("rfig4_permutation.png", bbox_inches="tight"); fig.savefig("rfig4_permutation.pdf", bbox_inches="tight"); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.5, 4))
groups=["Global\ncrises","Regional\ncrises","Normal\nyears"]; means=[mean_global,mean_regional,mean_normal]; cis=[ci_g,ci_r,ci_n]
errs=[[m-lo for m,(lo,hi) in zip(means,cis)],[hi-m for m,(lo,hi) in zip(means,cis)]]
ax.bar(groups, means, color=[GC,RC,"#adb5bd"], yerr=errs, capsize=6, edgecolor="white")
for i,m in enumerate(means): ax.text(i, m+0.02, f"{m:.2f}", ha="center", fontsize=10)
ax.set_ylim(0,1); ax.set_ylabel("mean r"); ax.set_title(f"Mean r by period type — {TAG}", loc="left", fontsize=10)
fig.savefig("rfig5_groups.png", bbox_inches="tight"); fig.savefig("rfig5_groups.pdf", bbox_inches="tight"); plt.close(fig)

results = {
 "N": N, "analysis_window":[int(YEARS[0]),int(YEARS[-1])], "band_years":[round(1/HI,1),round(1/LO,1)],
 "filter_order":2, "data":"Maddison Project Database 2023, real GDP per capita (constant int-$)",
 "r_by_year": R_by_year, "GLOBAL":GLOBAL, "REGIONAL":REGIONAL,
 "mean_global":mean_global,"mean_regional":mean_regional,"mean_normal":mean_normal,
 "ci_global":ci_g,"ci_regional":ci_r,"ci_normal":ci_n,
 "true_contrast":true_contrast,"p_perm":p_perm,"nperm":nperm,
 "crisis_percentiles":{int(y):round(pct(y),1) for y in g_years},
 "regional_percentiles":{int(y):round(pct(y),1) for y in r_years},
 "peak_year":int(YEARS[R.argmax()]),"peak_R":float(R.max()),
 "trough_year":int(YEARS[R.argmin()]),"trough_R":float(R.min()),
}
json.dump(results, open("crisis_results_real.json","w"), indent=2)

print("=== REAL GDP r by year ===")
for y in YEARS:
    tag=" [GLOBAL]" if y in g_years else (" (regional)" if y in r_years else "")
    print(f"  {y}: {R_by_year[int(y)]:.2f}{tag}")
print(f"\nmean r  global={mean_global:.3f} regional={mean_regional:.3f} normal={mean_normal:.3f}")
print(f"relative test contrast={true_contrast:+.3f}, p={p_perm:.4f}")
print(f"peak r={results['peak_R']:.2f} ({results['peak_year']}); trough={results['trough_R']:.2f} ({results['trough_year']})")
print("crisis percentiles:", results["crisis_percentiles"])
print("regional percentiles:", results["regional_percentiles"])
