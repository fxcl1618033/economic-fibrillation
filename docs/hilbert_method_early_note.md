# Family B — GDP as an Oscillator via the Hilbert Transform
### The math, the meaning, the knobs, and a Claude Design animation spec

This document explains exactly what `hilbert_oscillators.py` does to the real
26-economy GDP panel, so you understand the mathematics and can change it.
Everything below runs on the actual data (World Bank GDP, 1970–2023); the
computed oscillator values are saved in `hilbert_output.csv`.

---

## 1. The core problem, in one line
Raw GDP **rises** — it is not an oscillator. So we split GDP into a rising
**trend** plus a wobble **around** the trend (the business cycle). The wobble is
the oscillator, and we read its *phase* (where each economy sits in its cycle).

---

## 2. The equations (the whole method)

**Step 1 — the cyclical component.** Work in logs, remove the mean, and keep only
the business-cycle band (periods ≈ 2–9 years) with a band-pass filter `B[·]`:

$$ x(t) \;=\; B\big[\, \ln G(t) - \overline{\ln G}\, \big] $$

- `G(t)` = GDP of one economy in year `t`.
- `x(t)` = the cyclical wobble, oscillating around zero.
- Why logs? So a swing means the same *percentage* deviation for a big and a
  small economy.
- Why band-pass? Two reasons: it removes the slow trend (growth, inflation, FX),
  **and** the Hilbert transform only gives a meaningful phase for a *narrowband*
  signal — one dominant cycle length. Band-pass first is therefore required, not
  optional.

**Step 2 — the analytic signal (the Hilbert transform).** The Hilbert transform
`H[·]` shifts every frequency component by −90°. Applied to `x(t)` it produces the
"quadrature" partner (what sine is to cosine). Stack them as a complex number:

$$ z(t) \;=\; x(t) \;+\; i\,H[x(t)] \;=\; A(t)\,e^{\,i\varphi(t)} $$

where the Hilbert transform itself is

$$ H[x](t) \;=\; \frac{1}{\pi}\,\text{P.V.}\!\int_{-\infty}^{\infty}
\frac{x(\tau)}{t-\tau}\,d\tau . $$

**Step 3 — instantaneous amplitude, phase, frequency.** From `z(t)`:

$$ A(t) = |z(t)| = \sqrt{x^2 + H[x]^2}, \qquad
   \varphi(t) = \arg z(t) = \operatorname{atan2}\big(H[x],\,x\big), \qquad
   \omega(t) = \frac{d\varphi}{dt}. $$

- `A(t)` — how big the boom/bust swing is right now.
- `φ(t)` — the **clock-hand angle**: peak ≈ 0, downturn ≈ +π/2, trough ≈ ±π,
  recovery ≈ −π/2. This is the number the whole paper hangs on.
- `ω(t)` — the local cycle speed (how fast this economy is moving through its cycle).

**Step 4 — the Kuramoto order parameter (global synchronization).** With `N`
economies each carrying a phase `φⱼ(t)`:

$$ R(t)\,e^{\,i\Psi(t)} \;=\; \frac{1}{N}\sum_{j=1}^{N} e^{\,i\varphi_j(t)} . $$

- `R(t) ∈ [0,1]` — **the synchronization index**. `R≈0`: economies scattered
  around their cycles (diversified). `R≈1`: all in the same phase (locked → fragile).
- `Ψ(t)` — the average phase (where the "world cycle" points).

`R(t)` is the quantity that (in your thesis) rises into synchronized global
crises and marks systemic fragility.

---

## 3. What the figures show
- **fig1_pipeline** — one economy (Japan) taken through all four steps: rising GDP
  → cyclical wobble + its Hilbert partner → phase sawtooth → the analytic signal
  traced as a **rotating clock hand** in the complex plane (colour = year).
- **fig2_all_economies** — top: all 26 cyclical components together; bottom: a
  **phase heatmap** (each row an economy, colour = phase). Vertical bands of one
  colour = moments when economies share a phase = synchronization.
- **fig3_order_parameter** — `R(t)`, the global synchronization curve.

---

## 4. The knobs (what you can change, and what happens)
- **The band `LO, HI`** (currently periods ≈ 2–9 yr). Widen it and you let faster
  or slower fluctuations into the "cycle"; narrow it and the phase gets cleaner
  but you may miss real dynamics. This is the single most important choice —
  report a robustness check with a second band.
- **Trend removal method.** Band-pass (used here) vs. simple growth rate
  (`Δ ln G`) vs. an HP filter. Growth rate is the simplest defensible alternative;
  showing your result survives under it strengthens the paper.
- **Filter order** (currently 2). Higher = sharper band but more edge ringing.
- **Edge effects.** The first/last ~3 years are unreliable (the filter rings at
  the boundaries), so for the paper trim to ~1974–2021 even though the figures
  here show the full span.
- **Real vs. current-price GDP.** Swap in Maddison real GDP per capita
  (see `prepare_data.py`) for a constant-price robustness run.

---

## 5. Claude Design animation spec (uses the real data)

Give Claude Design this prompt together with `hilbert_output.csv` (columns:
`Year`, `<country>__cyclical`, `<country>__phase`, `order_parameter_R`).

> Build a clean, vibrant, minimal animation that teaches "GDP as an oscillator,"
> driven by the real values in `hilbert_output.csv` (26 economies, years
> 1970–2023). Play it as a guided sequence, then loop.
>
> **Scene 1 — one economy becomes a clock.** Take Japan. Show its rising GDP as a
> line climbing off the bottom-left. Then animate "peeling off" the straight
> trend so only the up-and-down wobble remains, centred on a zero line — label it
> "the business cycle." Then rotate that wobble into a spinning arrow (phasor) on
> a small circle: the arrow angle is the `Japan__phase` value each year. Peak of
> the cycle points right, trough points left. Caption, minimal: "each economy is a
> clock — the hand shows where it is in its boom-bust cycle."
>
> **Scene 2 — all 26 clocks.** Arrange 26 dots on a ring, one per economy, each
> placed at its `<country>__phase` for the current year, coloured by phase on a
> smooth cyclic colour wheel (same hue = same cycle position). Step the year
> forward 1970 → 2023. Dots drift and, at some years, bunch into one coloured
> clump. Draw a white arrow from the centre whose length is `order_parameter_R`
> (short = scattered, long = synchronized), pointing at the average phase.
>
> **Scene 3 — the payoff trace.** Along the bottom, draw `order_parameter_R` over
> time as a thin line with a moving marker at the current year, and faint labels
> at 2008 and 2020 (where it peaks) and the late-1990s (where it dips).
>
> Readouts: current year (large) and `R` (0–1). Aesthetic: dark near-black
> background, neon phase-coloured dots with soft glow, thin monospace numbers, no
> explanatory paragraphs — motion carries the meaning. The story without words:
> each economy is a clock, and the dangerous years are when all the clocks agree.

---

## 6. One-line summary
`ln G → band-pass → x(t) → Hilbert → z(t)=A e^{iφ} → φ(t) per economy →
R(t)=|mean e^{iφ}|`. Trend becomes nothing; the wobble becomes a phase; the
phases together become synchronization.
