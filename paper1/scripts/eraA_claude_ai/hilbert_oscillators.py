"""
hilbert_oscillators.py
======================
FAMILY B — turning real GDP into oscillators, then reading each economy's
business-cycle PHASE with the Hilbert transform. Runs on the real 26-economy
panel (World Bank GDP, 1970-2023) we assembled.

THE MATH (see hilbert_method.md for the plain-language version)
---------------------------------------------------------------
1. Trend removal. Raw GDP G(t) rises, so it is not an oscillator. We work in
   logs and keep only the business-cycle band (periods ~2-9 years) with a
   Butterworth band-pass filter B[.]:
       x(t) = B[ log G(t) - mean(log G) ]          # the cyclical component (the wobble)

2. Analytic signal via the Hilbert transform H[.]:
       z(t) = x(t) + i * H[x(t)] = A(t) * exp( i * phi(t) )
   The Hilbert transform shifts every frequency by -90 degrees, so H[x] is the
   "quadrature" partner of x (like sin is to cos).

3. Instantaneous amplitude, phase, frequency:
       A(t)    = |z(t)|             = sqrt( x^2 + H[x]^2 )      # how big the swing is
       phi(t)  = arg(z(t))          = atan2( H[x], x )         # the clock-hand angle
       omega(t)= d phi / dt                                     # local cycle speed

4. Kuramoto order parameter (global synchronization of the N economies):
       R(t) * exp( i*Psi(t) ) = (1/N) * sum_j exp( i * phi_j(t) )
   R ~ 0  -> economies scattered around their cycles (desynchronized)
   R ~ 1  -> economies locked in the same phase (synchronized = fragile)

You can change: the band (LO, HI), the filter order, or swap log-GDP for the
growth rate. Each choice is a knob discussed in the .md.
"""

import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, hilbert
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# ---------------------------------------------------------------- load real data
df = pd.read_csv("gdp_panel_long_1970_2023.csv")
panel = df.pivot(index="Year", columns="Country", values="GDP_current_USD")
years = panel.index.values.astype(float)
countries = list(panel.columns)
N = len(countries)

# ---------------------------------------------------------------- the pipeline
FS = 1.0            # one sample per year
LO, HI = 1/9.0, 0.49   # business-cycle band (periods ~2 to 9 years)
b, a = butter(2, [LO/(FS/2), HI/(FS/2)], btype="band")

def cyclical(g):
    """log-GDP, demeaned, band-passed -> the business-cycle oscillation."""
    lg = np.log(g)
    return filtfilt(b, a, lg - lg.mean())

X   = {c: cyclical(panel[c].values) for c in countries}   # real part  x(t)
Z   = {c: hilbert(X[c])            for c in countries}     # analytic signal z(t)
PHI = {c: np.angle(Z[c])          for c in countries}      # phase  phi(t)
AMP = {c: np.abs(Z[c])            for c in countries}      # amplitude A(t)

# order parameter R(t)
phase_mat = np.array([PHI[c] for c in countries])         # (N, T)
Zbar = np.exp(1j*phase_mat).mean(axis=0)
R    = np.abs(Zbar)
PSI  = np.angle(Zbar)

# save the computed oscillator data (for Claude Design / re-use)
out = pd.DataFrame({"Year": years.astype(int)})
for c in countries:
    out[f"{c}__cyclical"] = X[c]
    out[f"{c}__phase"]    = PHI[c]
out["order_parameter_R"] = R
out.to_csv("hilbert_output.csv", index=False)

# ================================================================ FIGURES
plt.rcParams.update({
    "figure.dpi": 130, "font.size": 10, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25,
    "font.family": "DejaVu Sans",
})
CRISES = [2008, 2020]

# ---------- FIGURE 1: how ONE economy becomes an oscillator (teaching) --------
demo = "Japan"          # a visibly cyclical economy
g   = panel[demo].values
lg  = np.log(g)
x   = X[demo]; hx = np.imag(Z[demo]); ph = PHI[demo]

fig = plt.figure(figsize=(12, 7))
gs  = fig.add_gridspec(3, 2, width_ratios=[1.35, 1], hspace=0.55, wspace=0.28)

ax0 = fig.add_subplot(gs[0, 0])
ax0.plot(years, g/1e9, color="#1b263b", lw=2)
ax0.set_title(f"1 · Raw GDP of {demo} — it just rises (not an oscillator)", loc="left", fontsize=10.5)
ax0.set_ylabel("GDP (billion US$)")

ax1 = fig.add_subplot(gs[1, 0])
ax1.axhline(0, color="k", lw=0.6)
ax1.plot(years, x, color="#0077b6", lw=2, label="cyclical part  x(t)")
ax1.plot(years, hx, color="#e07a5f", lw=1.6, ls="--", label="Hilbert partner  H[x](t)")
for cy in CRISES: ax1.axvline(cy, color="grey", lw=0.8, alpha=0.5)
ax1.set_title("2 · Strip the trend → the business-cycle wobble, and its 90°-shifted partner", loc="left", fontsize=10.5)
ax1.set_ylabel("log-GDP cycle")
ax1.legend(fontsize=8, loc="upper left", framealpha=0.9)

ax2 = fig.add_subplot(gs[2, 0])
ax2.plot(years, ph, color="#5a189a", lw=2)
for cy in CRISES: ax2.axvline(cy, color="grey", lw=0.8, alpha=0.5)
ax2.set_title("3 · Instantaneous phase φ(t) — the clock-hand angle (−π→π sawtooth)", loc="left", fontsize=10.5)
ax2.set_ylabel("phase (rad)"); ax2.set_xlabel("year")
ax2.set_yticks([-np.pi, 0, np.pi]); ax2.set_yticklabels(["−π", "0", "π"])

# right: the analytic signal as a rotating phasor in the complex plane
axP = fig.add_subplot(gs[:, 1])
pts = np.array([x, hx]).T.reshape(-1, 1, 2)
segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
lc = LineCollection(segs, cmap="viridis", linewidth=2)
lc.set_array(years[:-1]); axP.add_collection(lc)
axP.scatter([0],[0], color="k", s=14, zorder=5)
lim = 1.05*max(np.abs(x).max(), np.abs(hx).max())
axP.set_xlim(-lim, lim); axP.set_ylim(-lim, lim); axP.set_aspect("equal")
axP.axhline(0, color="k", lw=0.5); axP.axvline(0, color="k", lw=0.5)
axP.set_title("4 · The economy as a rotating clock hand\n z(t)=x+iH[x] traced over time (colour = year)", loc="left", fontsize=10.5)
axP.set_xlabel("x(t)"); axP.set_ylabel("H[x](t)")
cb = fig.colorbar(lc, ax=axP, fraction=0.046, pad=0.04); cb.set_label("year")
fig.suptitle("FAMILY B — turning one economy's GDP into a business-cycle oscillator (Hilbert transform)",
             fontsize=12.5, y=0.98)
fig.savefig("fig1_pipeline.pdf", bbox_inches="tight")
fig.savefig("fig1_pipeline.png", bbox_inches="tight")
plt.close(fig)

# ---------- FIGURE 2: all 26 economies + phase heatmap ------------------------
fig, (axA, axB) = plt.subplots(2, 1, figsize=(12, 8.5),
                               gridspec_kw={"height_ratios":[1, 1.25], "hspace":0.32})
for c in countries:
    axA.plot(years, X[c], color="#457b9d", lw=0.9, alpha=0.45)
axA.axhline(0, color="k", lw=0.6)
for cy in CRISES: axA.axvline(cy, color="#e63946", lw=1.2, alpha=0.7)
axA.set_title("All 26 economies as business-cycle oscillators (cyclical component of log-GDP)", loc="left")
axA.set_ylabel("log-GDP cycle"); axA.set_xlim(years[0], years[-1])
axA.text(2008, axA.get_ylim()[1]*0.9, " 2008", color="#e63946", fontsize=8)
axA.text(2020, axA.get_ylim()[1]*0.9, " 2020", color="#e63946", fontsize=8)

order = np.argsort([np.mean(PHI[c]) for c in countries])
mat = phase_mat[order]
im = axB.imshow(mat, aspect="auto", cmap="twilight",
                extent=[years[0], years[-1], N-0.5, -0.5], interpolation="nearest",
                vmin=-np.pi, vmax=np.pi)
axB.set_yticks(range(N)); axB.set_yticklabels([countries[i] for i in order], fontsize=7)
axB.set_title("Phase of every economy over time — vertical colour bands = synchronization", loc="left")
axB.set_xlabel("year")
for cy in CRISES: axB.axvline(cy, color="white", lw=1.0, alpha=0.6)
cb = fig.colorbar(im, ax=axB, fraction=0.025, pad=0.02, ticks=[-np.pi,0,np.pi])
cb.ax.set_yticklabels(["−π","0","π"]); cb.set_label("phase (cycle position)")
fig.savefig("fig2_all_economies.pdf", bbox_inches="tight")
fig.savefig("fig2_all_economies.png", bbox_inches="tight")
plt.close(fig)

# ---------- FIGURE 3: the payoff — order parameter R(t) ----------------------
fig, ax = plt.subplots(figsize=(11, 3.6))
ax.plot(years, R, color="#d00000", lw=2.2)
ax.fill_between(years, 0, R, color="#d00000", alpha=0.08)
for cy in CRISES: ax.axvline(cy, color="grey", lw=1, ls="--")
ax.set_ylim(0, 1); ax.set_xlim(years[0], years[-1])
ax.set_title("Global synchronization R(t) — the Kuramoto order parameter of the 26 economies", loc="left")
ax.set_ylabel("R  (0=scattered, 1=locked)"); ax.set_xlabel("year")
ax.annotate("2008", (2008, R[np.where(years==2008)][0]), textcoords="offset points",
            xytext=(4,6), color="grey", fontsize=8)
ax.annotate("2020", (2020, R[np.where(years==2020)][0]), textcoords="offset points",
            xytext=(4,6), color="grey", fontsize=8)
fig.savefig("fig3_order_parameter.pdf", bbox_inches="tight")
fig.savefig("fig3_order_parameter.png", bbox_inches="tight")
plt.close(fig)

print("done. figures: fig1_pipeline, fig2_all_economies, fig3_order_parameter (.pdf/.png)")
print("data: hilbert_output.csv   |  N =", N, " years", int(years[0]), "-", int(years[-1]))
print("peak-sync years:", [int(years[i]) for i in np.argsort(-R)[:5]])
