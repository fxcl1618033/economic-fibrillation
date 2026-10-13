# Paper 1 theory box (draft): why aligned cycles stop diversifying

Status: **draft for Sid, 14 October 2026.** Section A of the DTT report only (`dtt/legacy/`, Sid's prior work);
no tipping simulation goes into Paper 1. For the Discussion, next to D1 and D2 in `docs/methods_proposed_edits.md`.
`docs/methods.md` is not changed. Numbers: `dtt/D3_real_data.md` (`dtt/results/d3_neff.json`); the variance law is
checked against Monte Carlo in `tests/test_dtt.py`.

---

**Box 1 | Loss of diversification as arithmetic**

Let economy *i*'s cycle have phase θᵢ and swing size Aᵢ, and let a shock reach every economy according to where it
is in its cycle: economy *i* responds with qᵢ = σ Aᵢ u·vᵢ, where vᵢ = (cos θᵢ, sin θᵢ) and u is a unit direction drawn
at random. Economies at opposite points of their cycles respond with opposite signs, so their responses cancel in
the world average. If only a share ρ of the shock is common and the rest is independent across economies (each with
variance σ²Aᵢ²/2), the variance of the world-average response q̄, given the phases, is

  Var(q̄) = (σ²/2) [ ρ |Z_A|² + (1 − ρ) · mean(A²) / N ],   Z_A = (1/N) Σᵢ Aᵢ e^{iθᵢ}.

The first term is the common shock, the second the independent part. Because |Z_A| = Ā·R_A, the common term is the
square of the fibrillation identity of §6.2: world swing equals swing size times alignment. With equal swing sizes and
a fully common shock, Var(q̄) = σ²R²/2, against σ²/(2N) if the responses were independent. The world then varies like

  N_eff = 1 / R²

independent economies: the number that would give the same world variance if they did not move together. With a
common share ρ, N_eff = 1 / (ρR² + (1 − ρ)/N). Alignment matters only for the common part of shocks; the independent
part is the familiar averaging-out of Lucas (1977), which fails only when a few units are large (Gabaix 2011) or
central in the input–output network (Acemoglu et al. 2012). Here it fails for a third reason: the economies' cycles
line up.

On the 31 economies, N_eff = 1/E[r²] is about 3.5 over 1970–2022, 2.4 in recession years and 2.1 the year before
(1.1 in 2020); 2009 and 2020 pull these down, and the earlier recessions are not low. Averaged over the 10-year
windows of §6.1, the law gives the cross term 84.1% of the extra world variance in recession windows, against the
84.3% measured: the loss of diversification of §6.1 is this arithmetic.

It is arithmetic, not a mechanism. Any year in which cycles happen to line up has a larger world swing, coupled or
not, and recessions dated from world output are such years even in simulated worlds with no coupling (§5.3).

*Interpretation, not a test:* in the taxonomy of Ashwin et al. (2012), a transition caused by larger disturbances
while the restoring forces stay the same is noise-induced tipping, which does not show critical slowing down — and
the autocorrelation of synchronization does not rise before recessions, nor does recovery slow after them (§6.7).

---

## Notes for Sid

1. **What the box claims.** Only section A: an exact variance law and its link to the identity. The two numbers on
   real data are descriptive (no p-values). The last paragraph is labelled as interpretation; nothing in Paper 1
   tests for noise-induced tipping.
2. **Why the arithmetic caveat is in the box.** The G1 simulations showed that recessions dated from world output
   have above-average alignment even without coupling (L8). Section A is exactly that arithmetic, so the box says it
   rather than letting "synchrony amplifies aggregate swings" read as a finding. The candidate claim — synchrony first,
   then escape — is the G1b question, not Paper 1's.
3. **The shock picture.** "A shock in a random direction of the cycle plane" is the report's formulation. A plainer
   gloss for readers: the same disturbance pushes an economy near its peak down and one near its trough up; when the
   cycles are spread out these cancel, when they are aligned they add.
4. **Granular reading of the second term.** With GDP weights wᵢ the independent term becomes (1 − ρ) Σ wᵢ² Aᵢ² / 2, a
   Herfindahl-type concentration of (wᵢ Aᵢ) — Gabaix's channel. One sentence (as drafted) is enough; more would need
   a check that the analogy survives his definitions.
5. **Exactness.** The law is exact for the stated shock (checked against Monte Carlo); the link to the decomposition is
   exact instantaneously (cross share = 1 − N_eff/N with equal weights and swing sizes) and close, not exact, over
   the decomposition's windows (within a point for the 84.3%; `dtt/D3_real_data.md` says when it becomes exact).
6. **References** are verified in `docs/literature_dtt.md`.
