# Proposed edits to the Methods

`docs/methods.md` is not changed. Each edit below quotes the current text, gives the proposed text and the reason.
Part A holds edits Sid has decided (11 October 2026); Part B holds edits that need his wording or a decision; Part C
lists numbers that will change once Phase 3 has run under the pre-registered conventions and are filled in then.

---

## Part A — decided by Sid

### A1. §7.4 Multiplicity: the Bonferroni value

**Current:** "no coefficient survives a Bonferroni correction (lead-1 and lag $-2$: $p_{\mathrm{adj}} = 0.095$; lead-2: $0.189$)."

**Proposed:** "no coefficient survives a Bonferroni correction (lead-1 and lag $-2$: $p_{\mathrm{adj}} = 0.094$; lead-2: $0.189$)."

**Why:** 5 × 1/53 = 0.0943. The printed 0.095 came from 5 × the rounded 0.019 (open issue 20; `ef.crisis.bonferroni`).
The diagnostics figure caption (panel c) uses the same values and needs no other change.

### A2. §6.5 Network geometry: the window convention and the decade means

**Current:** "Because the 10-year window needs nine years of run-in, $L(t)$ is defined from 1971 onward. Two questions
are asked of $L$: whether it trends secularly — reported as a description via decade means ($0.706$ in the 1970s
against $0.379$ in 2013–2022, a factor of $1.9\times$; the single-year endpoints $0.771$ and $0.250$ are noisy
individual windows and are not the interpreted quantity) — and whether contraction coincides with the pre-crisis
windows."

**Proposed:** "The 10-year windows are kept inside the 1970–2022 analysis window, so that no value of $L$ draws on the
1950–69 run-in; $L(t)$ is therefore defined from 1979. Two questions are asked of $L$: whether it trends secularly —
reported as a description via decade means, $0.677$ in 1979–89 against $0.379$ in 2013–2022, a factor of
$1.8\times$ — and whether contraction coincides with the pre-crisis windows."

**Why:** Sid's decision (open issue 21). The 1970s mean of 0.706 needed windows reaching into the run-in, which the
same paragraph excluded; the endpoint 0.771 matched no stored result (the stored value is 0.781). The new values come
from `ef.network` on S26 (`run_mst` with window 1970–2022). **The headline factor changes from 1.9× to 1.8×.** The
sentence that follows (the pre-crisis test results) is updated from Phase 3 (Part C).

### A3. §7.7 Window-convention sensitivity of the network measure

**Current:** "$L(t)$ is reported on 10-year windows, and its early values depend on whether the window is allowed to
reach back into the 1950–69 run-in. Restricting windows to 1970 onward, $L$ is defined from 1979 and the decade-mean
comparison becomes $0.652$ (1979–89) against $0.379$ (2013–2022). The convention is stated wherever $L$ is quoted."

**Proposed:** "$L(t)$ is reported on 10-year windows kept inside 1970–2022 (§6.5). Allowing the windows to reach back
into the 1950–69 run-in defines $L$ from 1971 but leaves every value from 1979 onward unchanged, so the decade means of
§6.5 do not depend on this choice; it affects only the 1970s, which the stated convention excludes. The convention is
stated wherever $L$ is quoted."

**Why:** with windows inside 1970–2022 the 1979–89 mean is 0.677, not 0.652; 0.652 is $L$ in the single year 1979,
labelled as a decade mean (open issue 21). Windows reaching back to 1962 give exactly the same $L$ from 1979 onward
(checked in code), so the convention affects only years the paper no longer quotes.

### A4. §6.7 Critical slowing down: two indicators plus the coupling test

**Current (first paragraph):** "We test the standard early-warning battery — rising lag-1 autocorrelation, rising
variance, and rising restoring-time — on the pre-crisis windows. All three are reported as null in Results."

**Proposed:** "We test the standard early-warning battery — rising lag-1 autocorrelation and rising variance of the
fluctuations of $r(t)$ — on the pre-crisis windows. A third indicator often added, the restoring time, was considered
and dropped: estimated as $1/(-\ln\varphi)$ from the same lag-1 autocorrelation $\varphi$, it is an increasing function
of $\varphi$, so its trend test repeats the autocorrelation's and adds no independent evidence. We complement the two
indicators with a test that treats coupling as the bifurcation parameter: inverting the mean-field Kuramoto relation
$r = \sqrt{1 - K_c/K}$ gives an implied coupling $K/K_c = 1/(1 - r^2)$, and critical slowing down would show as a fall
in the recovery rate $\lambda = -\ln\varphi$ in the years just after each onset relative to all other years, tested
one-sided against the surrogate ensemble of §5.2. All three tests are reported as null in Results."

**Why:** Sid's decision (open issue 22). The coupling test (registry F4, `kuramoto_bifurcation.py`) is run and
reported in the registry but is not described anywhere in the current Methods; this paragraph adds it. The rest of
§6.7 (the Ashwin et al. taxonomy) stands.

---

## Part B — need Sid's wording or decision

### B1. §7.2 or §1: the arc depends on the phase convention (open issue 1; HANDOFF §8 decision 2)

The Methods disclose that the run-in moves the amplitude coefficient but not that it moves the arc. Two options:

- **Short:** "The run-in convention also matters for the lead–lag profile of §6.3: computing phases on the 1970–2022
  window alone, lead-1 is $+0.178$ ($p = 0.094$) and lag $-2$ is $-0.144$ to $-0.197$ ($p = 0.094$–$0.170$), so the
  pre- and post-crisis results are significant under the run-in-protected convention only. We report the protected
  convention for the reason given in §1, and the alternatives in full in the robustness tables."
- **Fuller:** the same, plus one sentence on why (the Hilbert transform's edge errors reach a few years inward, and
  the run-in gives the 1970s two decades of protection) and the edge-robust variant's result once Phase 3 has it.

### B2. §8: the earlier amplitude convention is now known (open issue 3)

**Current:** "We were unable to recover the exact amplitude convention behind the earlier figures;"

**Proposed:** "The earlier figure of $+0.51$ applied the Hilbert transform to the 1970–2022 window only, after a
1950–2022 band-pass (it reproduces exactly under that convention);"

### B3. §6.1: the cross-term split (open issue 5)

**Proposed addition after the cross-share sentence:** "The cross term is not the same thing as correlation: it rises
when economies move together and when they swing harder. Splitting its recession rise, higher correlation supplies
35% (equal weights 41%), larger swings 50% (46%) and their interaction 14% (13%). The recession excess is therefore
best described as amplification transmitted by alignment." (Values from `crossterm_split.py`, reproduced by
`ef.decomposition.cross_split`; the GDP-weighted split uses end-of-window weights and will be recomputed with the
Methods' within-window mean weights in Phase 3.)

### B4. §8: data citation (open issue 15)

**Current:** "distributed in the `MaddisonData` R package (v1.1.0)."

**Proposed:** "distributed in the `MaddisonData` R package (repository `sbgraves237/maddisondata`, commit `3ed424b6`;
the data file `MaddisonData.rda`, sha256 `63a3cff9…`, is unchanged since October 2025)."

### B5. §6.5: the detrended pre-crisis MST test (open issue 23)

"$\tau = -0.086$, $p = 0.316$ detrended" does not reproduce: Gaussian detrending with σ = 5, 8 or 10 years on the
as-run windows gives τ between −0.043 and −0.057 and p between 0.36 and 0.42. The conclusion (null) is the same. The
pre-registration fixes σ = 8; the sentence is rewritten with the Phase 3 values.

---

## Part C — numbers to fill in from Phase 3

Under the pre-registered conventions (P throughout; rolling windows inside 1970–2022) these Methods numbers will be
recomputed and the text updated, with old and new values logged in `docs/decisions.md`:

- §6.5: the pre-crisis MST trend (raw and detrended), now over 1991, 2009 and 2020.
- §6.6: the phase-lead spread (0.403 years) and its surrogate statistics, computed so far under convention W.
- §6.7: the early-warning results, now over 2009 and 2020 (autocorrelation, variance) and 1982–2020 (coupling test).
- §6.1: the GDP-weighted cross-term split with within-window mean weights.
- §8: the reproduction statements, extended to the 30 economies.
- The diagnostics figure caption: panel a shows windows inside 1970–2022, the decade means 0.677 and 0.379 (1.8×),
  and no single-year endpoints.
