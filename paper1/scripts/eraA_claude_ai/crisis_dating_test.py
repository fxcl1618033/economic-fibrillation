"""
crisis_dating_test.py
=====================
Replaces hand-picked crisis years with an EXTERNAL, independently-dated crisis
chronology (Jorda-Schularick-Taylor banking-crisis dummy, the advanced-economy
standard aligned with Laeven-Valencia).

C(t) = fraction of the 17 JST economies in a systemic banking crisis in year t.
r(t) = Kuramoto synchronization of the same 17 economies (from real GDP).

Because banking crises are dated from bank runs / failures / policy response --
NOT from GDP -- C(t) is independent of r(t), which breaks the circularity in
the earlier hand-picked-window design.

Tests:
  1. Contemporaneous:  corr(r(t),   C(t))
  2. LEAD:             corr(r(t-1), C(t)),  corr(r(t-2), C(t))
     -> does synchronization RISE BEFORE crises? definitional co-movement cannot
        produce a lead, so a positive lead is the key non-circular result.
  Significance: exact circular-shift permutation (preserves autocorrelation).
"""
import numpy as np, pandas as pd, json
from scipy.signal import butter, filtfilt, hilbert
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

ISO17 = ['AUS','BEL','CAN','CHE','DEU','DNK','ESP','FIN','FRA','GBR','ITA','JPN',
         'NLD','NOR','PRT','SWE','USA']
Y0, Y1 = 1970, 2016

df = pd.read_excel('jst.xlsx', sheet_name='Data')
df = df[df.iso.isin(ISO17)]

# ---------------- r(t): same pipeline, JST real GDP per capita ----------------
FS, LO, HI = 1.0, 1/9.0, 0.49
b, a = butter(2, [LO/(FS/2), HI/(FS/2)], btype='band')
phase = {}
for c in ISO17:
    d = df[(df.iso==c) & (df.year.between(1950, 2016))].sort_values('year')
    g = d.rgdppc.values.astype(float); yrs = d.year.values.astype(int)
    cyc = filtfilt(b, a, np.log(g) - np.log(g).mean())
    ph = np.angle(hilbert(cyc))
    phase[c] = dict(zip(yrs, ph))

YEARS = np.arange(Y0, Y1+1)
r = np.array([np.abs(np.mean([np.exp(1j*phase[c][y]) for c in ISO17])) for y in YEARS])

# ---------------- C(t): banking-crisis intensity ----------------
C = df[df.year.between(Y0, Y1)].groupby('year')['crisisJST'].mean().reindex(YEARS).fillna(0).values

# ---------------- correlations + exact circular-shift permutation ----------------
def lag_corr(r, C, lag):
    """corr(r(t-lag), C(t)); lag>0 => r leads C."""
    if lag > 0:   x, y = r[:-lag], C[lag:]
    elif lag < 0: x, y = r[-lag:], C[:lag]
    else:         x, y = r, C
    return pearsonr(x, y)[0]

def perm_p(r, C, lag, obs):
    T = len(C)
    null = [lag_corr(r, np.roll(C, k), lag) for k in range(1, T)]  # exact, all shifts
    null = np.array(null)
    return (1 + np.sum(null >= obs)) / (1 + len(null)), null

lags = list(range(-4, 5))
rho = {L: lag_corr(r, C, L) for L in lags}
res = {}
for L in [0, 1, 2]:
    p, _ = perm_p(r, C, L, rho[L])
    res[L] = (rho[L], p)

# ---------------- subsample robustness: r_17 vs earlier r_26 (Maddison) ----------------
sub_txt = "n/a"
try:
    r26 = json.load(open('crisis_results_real.json'))['r_by_year']
    common = [y for y in YEARS if str(y) in r26]
    a17 = np.array([r[list(YEARS).index(y)] for y in common])
    a26 = np.array([r26[str(y)] for y in common])
    sub_corr = pearsonr(a17, a26)[0]
    sub_txt = f"{sub_corr:.3f} (over {len(common)} common years)"
except Exception as e:
    sub_corr = None

# ---------------- report to console ----------------
print("year :   r(t)   C(t)")
for i, y in enumerate(YEARS):
    mk = "  <-- crisis" if C[i] > 0 else ""
    if C[i] > 0 or y % 5 == 0:
        print(f"  {y}: {r[i]:.2f}   {C[i]:.2f}{mk}")
print("\n--- correlations of synchronization with crisis intensity ---")
print(f"  contemporaneous  corr(r(t),   C(t)) = {res[0][0]:+.3f}   p = {res[0][1]:.3f}")
print(f"  lead 1 year      corr(r(t-1), C(t)) = {res[1][0]:+.3f}   p = {res[1][1]:.3f}")
print(f"  lead 2 years     corr(r(t-2), C(t)) = {res[2][0]:+.3f}   p = {res[2][1]:.3f}")
print("\n  full lead-lag profile (lag>0 = synchronization leads):")
for L in lags:
    print(f"    lag {L:+d}: rho = {rho[L]:+.3f}")
print(f"\n  subsample robustness r_17 vs r_26: corr = {sub_txt}")

# ================= FIGURES =================
plt.rcParams.update({"figure.dpi":140,"font.size":10,"axes.spines.top":False,"axes.grid":True,"grid.alpha":0.25})

# fig 1: r(t) and C(t) together
fig, ax1 = plt.subplots(figsize=(11,4.3))
ax1.plot(YEARS, r, color="#1d3557", lw=2.3, label="synchronization r(t)")
ax1.set_ylabel("r(t)  (synchronization)", color="#1d3557"); ax1.set_ylim(0,1)
ax1.set_xlabel("year")
ax2 = ax1.twinx(); ax2.spines['top'].set_visible(False)
ax2.bar(YEARS, C, color="#e63946", alpha=0.35, width=0.8, label="banking-crisis intensity C(t)")
ax2.set_ylabel("C(t)  (fraction of 17 in crisis)", color="#e63946"); ax2.set_ylim(0,1)
ax1.set_title("Synchronization r(t) vs. independently-dated banking-crisis intensity C(t)", loc="left")
ax1.set_zorder(2); ax1.patch.set_visible(False)
fig.savefig("dfig1_r_vs_C.png", bbox_inches="tight"); fig.savefig("dfig1_r_vs_C.pdf", bbox_inches="tight"); plt.close(fig)

# fig 2: lead-lag cross-correlation with permutation band
null_band = []
T = len(C)
for L in lags:
    _, nd = perm_p(r, C, L, rho[L]); null_band.append(np.percentile(nd, 95))
fig, ax = plt.subplots(figsize=(8,4.3))
cols = ["#2a9d8f" if L>0 else ("#adb5bd" if L<0 else "#1d3557") for L in lags]
ax.bar(lags, [rho[L] for L in lags], color=cols, edgecolor="white")
ax.plot(lags, null_band, "k--", lw=1, label="95% chance level (permutation)")
ax.axhline(0, color="k", lw=0.6); ax.axvline(0, color="grey", lw=0.8, ls=":")
ax.set_xlabel("lag  (positive = synchronization leads crises)")
ax.set_ylabel("correlation with C(t)")
ax.set_title("Does synchronization lead banking crises?  cross-correlation profile", loc="left", fontsize=10.5)
ax.legend(fontsize=8)
fig.savefig("dfig2_leadlag.png", bbox_inches="tight"); fig.savefig("dfig2_leadlag.pdf", bbox_inches="tight"); plt.close(fig)

# fig 3: superposed epoch around the two crisis clusters (1991, 2007)
onsets = [1991, 2007]; L = np.arange(-4,5)
comp = np.array([[r[list(YEARS).index(o+k)] if (o+k) in YEARS else np.nan for k in L] for o in onsets])
fig, ax = plt.subplots(figsize=(7.5,4.2))
for o,row in zip(onsets,comp): ax.plot(L,row,marker="o",lw=1.5,alpha=0.6,label=f"{o} onset")
ax.plot(L, np.nanmean(comp,axis=0), color="#1d3557", lw=2.6, marker="o", label="mean")
ax.axvline(0,color="#e63946",ls="--",lw=1.2,label="crisis onset"); ax.set_ylim(0,1)
ax.set_xlabel("years relative to crisis onset"); ax.set_ylabel("r(t)")
ax.set_title("Synchronization around banking-crisis onsets (superposed epoch)", loc="left", fontsize=10.5)
ax.legend(fontsize=8)
fig.savefig("dfig3_epoch.png", bbox_inches="tight"); fig.savefig("dfig3_epoch.pdf", bbox_inches="tight"); plt.close(fig)

json.dump({
 "window":[Y0,Y1], "n_economies":17,
 "corr_contemp":res[0], "corr_lead1":res[1], "corr_lead2":res[2],
 "leadlag":{int(L):float(rho[L]) for L in lags},
 "subsample_corr": (float(sub_corr) if sub_corr is not None else None),
 "r_by_year":{int(y):float(r[i]) for i,y in enumerate(YEARS)},
 "C_by_year":{int(y):float(C[i]) for i,y in enumerate(YEARS)},
}, open("crisis_dating_results.json","w"), indent=2)
print("\nsaved dfig1-3 and crisis_dating_results.json")
