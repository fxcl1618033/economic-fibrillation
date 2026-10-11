"""
surrogate_test.py
=================
Surrogate data testing via MONTE CARLO RESAMPLING (not machine learning).

QUESTION: the real synchronization curve R(t) spikes around 2008 and 2020.
Is that more than 26 economies happening to line up by chance?

NULL HYPOTHESIS H0: each economy wobbles with its own real dynamics, but there is
                    NO genuine coupling/alignment between them.
ALT  HYPOTHESIS H1: the observed R(t) exceeds what independence produces.

METHOD: build thousands of fake worlds under H0 (each economy keeps its own
amplitude & cycle character, but its timing is scrambled so nothing is aligned),
push each through the IDENTICAL Hilbert->phase->R pipeline, and see where the
real R(t) sits relative to the "chance" distribution.

SURROGATE BLEND (alpha knob, 0..1):
  - with probability alpha : circular time-shift ("phase-shuffle") -- keeps each
    economy's exact waveform, destroys only inter-economy alignment (strict test)
  - with probability 1-alpha: Fourier phase-randomization -- keeps the power
    spectrum, gives the surrogate its own individuality
  alpha = 0.85 primary (phase-shuffle dominant, Fourier-flavoured)
  alpha = 1.00 robustness (pure phase-shuffle, the hardest test to beat)
"""

import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, hilbert
import matplotlib.pyplot as plt

RNG = np.random.default_rng(42)
M = 5000                     # surrogate ensemble size
ALPHA_PRIMARY = 0.85
ALPHA_ROBUST  = 1.00
CRISES = [2009, 2020]        # a-priori years of interest (GFC trough, COVID)

# ---------------------------------------------------------------- real pipeline
df = pd.read_csv("gdp_panel_long_1970_2023.csv")
panel = df.pivot(index="Year", columns="Country", values="GDP_current_USD")
years_full = panel.index.values
countries = list(panel.columns); N = len(countries)

FS, LO, HI = 1.0, 1/9.0, 0.49
b, a = butter(2, [LO/(FS/2), HI/(FS/2)], btype="band")
def cyclical(g):
    lg = np.log(g); return filtfilt(b, a, lg - lg.mean())
Xfull = np.array([cyclical(panel[c].values) for c in countries])

# trim filter-edge years
mask = (years_full >= 1974) & (years_full <= 2021)
years = years_full[mask].astype(int)
X = Xfull[:, mask]                      # (N, T) real cyclical components
T = X.shape[1]

def order_parameter(cyc):
    ph = np.angle(hilbert(cyc, axis=1))
    return np.abs(np.exp(1j*ph).mean(axis=0))
R_real = order_parameter(X)

# ---------------------------------------------------------------- surrogates
def phase_shuffle(x):
    shifts = RNG.integers(1, x.shape[1], size=x.shape[0])
    return np.array([np.roll(x[i], shifts[i]) for i in range(x.shape[0])])

def fourier_surrogate(x):
    Xf = np.fft.rfft(x, axis=1)
    amp = np.abs(Xf)
    rp = RNG.uniform(0, 2*np.pi, Xf.shape)
    rp[:, 0] = 0.0                       # keep DC real
    if x.shape[1] % 2 == 0:
        rp[:, -1] = 0.0                  # keep Nyquist real
    return np.fft.irfft(amp*np.exp(1j*rp), n=x.shape[1], axis=1)

def surrogate_world(x, alpha):
    ps, fs = phase_shuffle(x), fourier_surrogate(x)
    pick = RNG.random(x.shape[0]) < alpha
    out = np.where(pick[:, None], ps, fs)
    return out

def run_ensemble(alpha, m):
    Rs = np.empty((m, T))
    for k in range(m):
        Rs[k] = order_parameter(surrogate_world(X, alpha))
    return Rs

print(f"running {M} surrogates at alpha={ALPHA_PRIMARY} ...")
R_surr = run_ensemble(ALPHA_PRIMARY, M)
print(f"running {M} surrogates at alpha={ALPHA_ROBUST} (robustness) ...")
R_surr_rob = run_ensemble(ALPHA_ROBUST, M)

# ---------------------------------------------------------------- statistics
def pvals(Rs):
    return (1 + (Rs >= R_real).sum(axis=0)) / (1 + Rs.shape[0])   # pointwise, +1 corrected
p_point = pvals(R_surr)
band_lo, band_hi = np.percentile(R_surr, [2.5, 97.5], axis=0)
p95 = np.percentile(R_surr, 95, axis=0)
p99 = np.percentile(R_surr, 99, axis=0)

def year_p(Rs, yr):
    i = int(np.where(years == yr)[0][0])
    c = (Rs[:, i] >= R_real[i]).sum()
    return (1 + c) / (1 + Rs.shape[0])

# global max-statistic test (controls family-wise error)
p_global = (1 + (R_surr.max(axis=1) >= R_real.max()).sum()) / (1 + M)

print("\n================ RESULTS (primary, alpha=0.85) ================")
print(f"{'year':>6} {'R_real':>7} {'null 95%':>9} {'p-value':>9} {'sig?':>5}")
for yr in years:
    i = int(np.where(years == yr)[0][0])
    star = "***" if p_point[i] < 0.01 else ("**" if p_point[i] < 0.05 else "")
    if yr in CRISES or p_point[i] < 0.05:
        print(f"{yr:>6} {R_real[i]:>7.2f} {p95[i]:>9.2f} {p_point[i]:>9.4f} {star:>5}")
print(f"\nA-priori crisis tests:")
for yr in CRISES:
    print(f"  {yr}: p = {year_p(R_surr, yr):.4f} (primary)   p = {year_p(R_surr_rob, yr):.4f} (pure phase-shuffle)")
print(f"Global max-R test (family-wise): p = {p_global:.4f}")
print(f"Peak real R = {R_real.max():.2f} in {years[R_real.argmax()]}")

# ---------------------------------------------------------------- convergence
fig, ax = plt.subplots(figsize=(9, 4))
for yr, col in zip(CRISES, ["#d00000", "#0077b6"]):
    i = int(np.where(years == yr)[0][0])
    exceed = (R_surr[:, i] >= R_real[i]).astype(float)
    running = (1 + np.cumsum(exceed)) / (1 + np.arange(1, M+1))
    ax.plot(np.arange(1, M+1), running, color=col, lw=1.6, label=f"{yr}  (final p={running[-1]:.4f})")
ax.axhline(0.05, color="grey", ls="--", lw=1, label="p = 0.05")
ax.set_xscale("log"); ax.set_xlabel("number of surrogate worlds (log scale)")
ax.set_ylabel("running p-value"); ax.set_ylim(0, max(0.2, ax.get_ylim()[1]))
ax.set_title("Monte Carlo convergence — the p-value settles as the ensemble grows (Law of Large Numbers)", fontsize=10.5, loc="left")
ax.legend(fontsize=8, framealpha=0.9); ax.grid(alpha=0.25)
fig.savefig("fig_convergence.pdf", bbox_inches="tight"); fig.savefig("fig_convergence.png", bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- band figure
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(11, 4.4))
ax.fill_between(years, band_lo, band_hi, color="#adb5bd", alpha=0.35, label="surrogate 95% band (chance)")
ax.plot(years, p95, color="#6c757d", lw=1, ls=":", label="surrogate 95th pct")
ax.plot(years, R_real, color="#d00000", lw=2.4, label="real R(t)")
sig = p_point < 0.05
ax.scatter(years[sig], R_real[sig], color="#d00000", s=42, zorder=5,
           edgecolor="white", linewidth=0.8, label="real > chance (p<0.05)")
for cy in CRISES: ax.axvline(cy, color="grey", lw=1, ls="--", alpha=0.6)
ax.set_ylim(0, 1); ax.set_xlim(years[0], years[-1])
ax.set_title("Real synchronization vs. what chance produces (5,000 surrogates, alpha=0.85)", loc="left")
ax.set_xlabel("year"); ax.set_ylabel("R  (synchronization)")
ax.legend(fontsize=8, ncol=2, framealpha=0.9, loc="upper left")
fig.savefig("fig_surrogate_band.pdf", bbox_inches="tight"); fig.savefig("fig_surrogate_band.png", bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- null histogram (teaching)
fig, axes = plt.subplots(1, len(CRISES), figsize=(10, 3.6))
for ax, yr in zip(np.atleast_1d(axes), CRISES):
    i = int(np.where(years == yr)[0][0])
    ax.hist(R_surr[:, i], bins=40, color="#adb5bd", edgecolor="white")
    ax.axvline(R_real[i], color="#d00000", lw=2.4)
    ax.set_title(f"{yr}:  real R={R_real[i]:.2f},  p={year_p(R_surr, yr):.4f}", fontsize=10)
    ax.set_xlabel("R under H0 (chance)"); ax.set_yticks([])
fig.suptitle("Where the real R sits inside the 'chance' distribution", fontsize=11)
fig.tight_layout()
fig.savefig("fig_null_hist.pdf", bbox_inches="tight"); fig.savefig("fig_null_hist.png", bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- save results
res = pd.DataFrame({"Year": years, "R_real": R_real,
                    "null_median": np.median(R_surr, axis=0),
                    "null_p95": p95, "null_p99": p99, "p_value": p_point})
res.to_csv("surrogate_results.csv", index=False)
print("\nsaved: fig_surrogate_band, fig_convergence, fig_null_hist (.pdf/.png), surrogate_results.csv")
