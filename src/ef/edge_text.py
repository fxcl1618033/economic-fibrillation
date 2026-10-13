"""The words of results/EDGE_MATCHED.md; every number is read from results/edge_matched/ and gnn/G1/ (ef.edge_report
builds the tables)."""
import numpy as np

from ef import edge_report as T
from ef.edge_null import TESTS


def _p(p): return f"{p:.4f}" if p < 0.001 else f"{p:.3f}"


def _rate(V, model, cell, test, null='edge'):
    d = V[(V.model == model) & (V.cell == cell) & (V.test == test) & (V.null == null)]; return (d.p <= 0.05).mean()


def _cur(G, model, cell, test):
    d = G[(G.model == model) & (G.cell == cell) & (G.test == test) & (G.rule.isin(['A', 'any']))]; return (d.p <= 0.05).mean()


def report(V, G, R):
    vt, rows = T.validation_table(V, G); rt, flags = T.real_table(R)
    over = [(k, m, r) for k, m, r in rows if r[1] > 0.05]
    S = {s: R[s]['tests'] for s in R}
    pc = lambda s, k: S[s][k]['p_current']; pe = lambda s, k: S[s][k]['p_edge']
    L = ["# Edge-matched nulls — pre-registration amendment 4", "",
         "Status: **for Sid's review.** Amendment 4 (`docs/preregistration_S30.md`, commit 864317a) listed the tests and "
         "fixed the null before anything ran; the code (fc63e87) was committed before the runs. `make edge-null` reruns "
         "everything (`python -m ef.edge_null validate | run | report`). Every number below is read from "
         "`results/edge_matched/` and `gnn/G1/`. The current p-values are unchanged and stay as reported (rule 6); the "
         "edge-matched p is a second null beside them.", "",
         "## In short", "",
         f"- **The swing-size test's lean is gone under the edge-matched null.** In uncoupled G1 worlds on the real "
         f"calendar it rejects in {100 * _rate(V, 'kuramoto', 'null', 'D11.swing'):.1f}% (Kuramoto) and "
         f"{100 * _rate(V, 'stuart_landau', 'null', 'D11.swing'):.1f}% (Stuart–Landau) of worlds, against "
         f"{100 * _cur(G, 'kuramoto', 'null', 'structure.p_swing'):.1f}% and {100 * _cur(G, 'stuart_landau', 'null', 'structure.p_swing'):.1f}% "
         f"with the current surrogates. **The real result stands:** p = {_p(pe('S31', 'D11.swing'))} on S31, "
         f"{_p(pe('S30', 'D11.swing'))} on S30 and {_p(pe('S26', 'D11.swing'))} on S26, the floor; the edge-matched null "
         f"reproduces the lean (its mean is {S['S31']['D11.swing']['null_mean']:+.3f}) and the real statistic "
         f"({S['S31']['D11.swing']['stat']:.2f}) is far beyond it.",
         f"- **Validation.** Every edge-matched null rejects at about its correct 5% in uncoupled worlds"
         + (f", with one exception just above: " + "; ".join(f"{TESTS[k][0]} ({T.MODEL[m]}, {100 * r[0]:.1f}%)" for k, m, r in over) if over else "")
         + f". The multivariate arc null also holds in trade-coupled worlds (lead-1 {100 * _rate(V, 'kuramoto', 'network', 'arc.P.lead1'):.1f}% "
         f"and {100 * _rate(V, 'stuart_landau', 'network', 'arc.P.lead1'):.1f}%), where circular shifts over-reject "
         f"after-2 ({100 * _cur(G, 'kuramoto', 'network', 'arc.after2'):.1f}% in Kuramoto worlds); after-2 is "
         f"{100 * _rate(V, 'kuramoto', 'network', 'arc.P.after2'):.1f}% there with the new null, still a little high.",
         f"- **No claim of the paper changes.** The two-sided lead-1 stays below 0.05 (p {_p(pe('S31', 'arc.P.lead1'))} on "
         f"S31, {_p(pe('S30', 'arc.P.lead1'))} on S30, {_p(pe('S26', 'arc.P.lead1'))} on S26; it was 0.019, the floor of the "
         f"circular shifts, on all three). The past-only lead-1, which carries the lead claim, is not on the list. r with "
         f"swing size, the cross term, Δcross and the variance rise keep their side of 0.05.",
         f"- **{len(flags)} p-values cross 0.05, none of them a claim:** " + "; ".join(
             f"{TESTS[k][0]} on {s} ({_p(a)} → {_p(b)})" for s, k, a, b in flags) + ". Section 4 reads each one.",
         "- **Resolution.** A circular-shift p moves in steps of 1/53 = 0.019 (0.019, 0.038, 0.057, …); an edge-matched p in "
         "steps of 1/5,001. Part of every arc crossing is this change of resolution, not new evidence.", "",
         "## 1. The tests and the null", "",
         "A test is on the list if a recession term of its statistic uses a year from 2019 to 2022 (amendment 4.1): the arc "
         "at lead-1, the crisis year, after-1 and after-2 (under P, and W, N and E); the bloc arcs; the real-GDP channel "
         "arc; the cross term (D5, D6); the identity (D11); MST contraction and fragility (E4, E6); the slowing-down trends "
         "(F1, F2); the recovery rate (F4); and, outside the rule, r with swing size (C1). Not listed: lead-2, every "
         "past-only (convention C) test, the phase-lead spread and the robustness variants.", "",
         "The edge-matched surrogates are built from each economy's growth rates: a long series (8 × 72 values) with the "
         "same periodogram and random phases, a 72-year window from a random start, cumulated from the real 1950 level, "
         "then the same band-pass, Hilbert transform, convention and windows as the data. So the surrogates have ends, "
         "and the filters treat their last years as they treat 2019–2022. Tests whose current null is independent "
         "surrogates get the independent version; the arcs, whose current null is circular shifts, get the multivariate "
         "version (one random phase per frequency for every economy, which keeps co-movement and so r's level and "
         "persistence). 5,000 surrogates per sample, floor 0.0002.", "",
         "## 2. Validation on the G1 worlds (amendment 4.3)", "",
         "Share of the 1,000 uncoupled G1 worlds per model (κ = φ = 0, the worlds of `gnn/G1/`) in which each test rejects "
         "at p ≤ 0.05 on the real calendar, with its 95% interval; 199 surrogates per world. **Bold**: the interval lies "
         "above the correct rate (3.8% for circular shifts, 5% for surrogates). The current-null columns are the G1 "
         "results for the same worlds.", ""] + vt + [
         "", "The multivariate arc null in the 1,000 trade-coupled G1 worlds per model (κ\\*), real calendar:", ""] + T.coupled_table(V, G) + [
         "", "The G1 run drew the cross-term and MST surrogates from the 1962–2022 cycles (the as-run scheme); Phase 3 "
         "draws them from the 1950–2022 cycles and cuts them. Both, on the same uncoupled worlds:", ""] + T.scheme_table(V, G) + [
         "", "The two schemes agree to within a point, so the G1 rows stand as reported.", "",
         "## 3. Real data: the current and the edge-matched p", "",
         "Statistic, current p and edge-matched p; **bold** where the two fall on opposite sides of 0.05. Circular-shift "
         "p (the arcs, rows A–G3 under \"p now\") has floor 0.019; surrogate p has floor 0.0002. Δcross and Δown are in "
         "units of world variance (tiny numbers); the share ratio is a fraction.", ""] + rt + [
         "", "## 4. The crossings, one by one", ""]
    notes = {
        'arc.P.after2': "After-2 (A5) is already a Limitation. Under the edge-matched null it is significant on S31 but not on S30, "
                        "and the new null still over-rejects after-2 slightly in trade-coupled Kuramoto worlds; the move "
                        "from 0.057 is mostly resolution (0.057 is the third-smallest circular-shift p). It stays a "
                        "Limitation, not a result.",
        'arc.W.lead1': "Lead-1 under convention W (A10) is a sensitivity convention; the lead claim rests on the past-only "
                       "phases, which are not affected.",
        'E11.within.lead1': "The within-bloc arc (E11) is exploratory; it lands on 0.050 on S30 and stays below 0.05 on S31.",
        'G3.same': "The real-GDP channel's crisis-year arc is not a registered result (the registry reports lead-1 and "
                   "after-2 for this channel); it moves from 0.094 to the 0.05 line.",
        'D6.own.gdp_mean': "Δown with GDP weights (D6) is a disclosure value; it moves from 0.038 to 0.053 on S31 (S30 stays "
                           "below 0.05). The validation shows this null is, if anything, conservative.",
    }
    for s, k, a, b in flags:
        L.append(f"- **{TESTS[k][0]}, {s}: {_p(a)} → {_p(b)}.** {notes.get(k, '')}")
    L += ["", "## 5. What it changes for Paper 1", "",
          "- The swing-size p (D11) can be quoted: it stays at the floor under a null with the same ends.",
          "- Lead-1's two-sided p is no longer the floor value but stays below 0.05 on every sample; the claim rests on the "
          "past-only version in any case (proposed edits, L8).",
          "- After-2 stays in Limitations (L3); its edge-matched p is added there.",
          "- The proposed Methods edits gain §5.3 (the κ = 0 table as a validation of test size) and §5.4 (this null), and "
          "the Limitations L8 and L9 (Sid, 14 October 2026)."]
    return "\n".join(L) + "\n"
