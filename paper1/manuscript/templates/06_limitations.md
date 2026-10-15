<!-- Limitations: L3, L4, L6, L8, L9 of docs/methods_proposed_edits.md, the open issues marked LIMITATIONS in docs/open_issues.md
     (1, 2, 14, 25), and Sid's list of 15 October 2026. -->
## 6 Limitations

**Two events carry the lead and the variance rise.** The pre-recession rise rests on 2009 and 2020 ($n \approx 2$):
without either the two-sided lead-1 is not significant ($p =$ {{S31/P/robustness#without 2009/lead1/1|p}} and
{{S31/P/robustness#without 2020/lead1/1|p}}), the split sample 1970–1995 shows none (lead-1
{{S31/P/robustness#1970-1995 (1975,82,91)/lead1/0|c2}}, $p =$ {{S31/P/robustness#1970-1995 (1975,82,91)/lead1/1|p}}), and
the variance rise of §4.5 has the same dependence. Both are properties of the tightly coupled modern economy observed
twice, not regularities, and with five events in 53 years no test here has more than five degrees of freedom.

**What multiplicity correction can show.** No lag survives a correction for testing five lags. With 53 circular shifts
the smallest $p$ the test can return is 0.019, so a single lag can never pass Bonferroni and passes Benjamini–Hochberg
only alongside another lag at the floor, which happened on the original 26 but not on the 30 or the 31 (Appendix
Table A5). The pre-crisis rise therefore rests on its survival under past-only phases and leave-one-economy-out, not on
corrected significance.

**How global recessions are dated.** Global recessions are dated from world output, and the economies whose
synchronization we measure make up most of it. The years in which world output falls most are years in which many
cycles happen to be falling together, so dating recessions this way builds some synchronization into them even when
economies are not coupled at all. In simulated worlds with no coupling, recession years dated the same way from each
world's own output make the two-sided arc reject at the crisis year in
{{@g1_lo:null,B,arc.crisis|pct1}}–{{@g1_hi:null,B,arc.crisis|pct1}} and at lead-1 in
{{@g1_lo:null,B,arc.lead1|pct1}}–{{@g1_hi:null,B,arc.lead1|pct1}} of worlds, about twice the correct 3.8% (§3.4.3).
Phases built from past data only are free of this ({{@g1_lo:null,B,arc_C.lead1|pct1}}–{{@g1_hi:null,B,arc_C.lead1|pct1}}).
The lead claim therefore rests on the past-only lead-1 ({{S31/P/conventions#C/arc/lead1/corr|c3}},
$p =$ {{S31/P/conventions#C/arc/lead1/p|p}}), not on the two-sided one.

**What the cross-term test shows.** The surrogate test of the cross term (§3.6.6) asks whether the cross term's share of
world variance in recession windows exceeds what independent economies would give. In simulated worlds it rejects in
nearly every coupled world whatever dates are used — {{@g1_lo:network,A,diversification.gdp_mean|pct1}}–{{@g1_hi:network,A,diversification.gdp_mean|pct1}}
of trade-coupled worlds with the real recession dates, which have nothing to do with those worlds — and in about 5% of
uncoupled ones. It detects co-movement in general, not co-movement at recessions. The recession-specific claim — that
co-movement supplies more of world variance in recessions than in normal years — rests on the gap between recession
and normal windows (cross share {{S31/P/diversification#gdp_mean/cross_share_crisis|f3}} against
{{S31/P/diversification#gdp_mean/cross_share_normal|f3}}, GDP-weighted), which is descriptive.

**The end of the sample.** 2020 sits two years from the last observation, and both the forward–backward filter and the
Hilbert transform are least reliable there. Without 2020 the two-sided lead-1 is {{S31/P/robustness#without 2020/lead1/0|c2}}
($p =$ {{S31/P/robustness#without 2020/lead1/1|p}}). Surrogates with ends (§3.4.4) move the two-sided lead-1 from
{{results/edge_matched/S31.json#tests/arc.P.lead1/p_current|p}} to {{results/edge_matched/S31.json#tests/arc.P.lead1/p_edge|p}}
and leave the claimed results on the same side of 0.05, but the most recent event remains the least well measured;
data for 2023–2025 are the cleanest fix.

**The fall after recessions.** Synchronization falls in the two years after a global recession (lag $-2$:
{{S31/P/arc#arc/after2/corr|c3}} on the 31, $p =$ {{S31/P/arc#arc/after2/p|p}}; {{S30/P/arc#arc/after2/corr|c3}},
$p =$ {{S30/P/arc#arc/after2/p|p}} on the 30; {{S26/P/arc#arc/after2/corr|c3}}, $p =$ {{S26/P/arc#arc/after2/p|p}} on the
original 26), but this half of the arc does not hold up. It is not significant on the 31 or the 30; it disappears with
the 3–10 year band and with growth rates (§3.6.1–3.6.2); it is significant under none of the alternative phase
conventions, including phases from past data only; and without 2020 it is {{S31/P/robustness#without 2020/after2/0|c2}}
($p =$ {{S31/P/robustness#without 2020/after2/1|p}}). On the 31 it sits on the threshold: leaving out any of
{{@loo_count_below:S31,after2|int}} of the 31 economies, or computing Russia's phases from 1992, takes it below 0.05. It
also sits where the filters are least reliable: the lag $-2$ test for 2020 uses $r(2022)$, the last observation.
Against surrogates with ends it is $p =$ {{results/edge_matched/S31.json#tests/arc.P.after2/p_edge|p}} on the 31 and
{{results/edge_matched/S30.json#tests/arc.P.after2/p_edge|p}} on the 30; that null still rejects lag $-2$ slightly too
often in simulated coupled worlds ({{@edge_rate:kuramoto,network,arc.P.after2|pct1}}), and most of the move is the finer
resolution of 5,000 surrogates against 53 shifts. We report it and do not claim it.

**Phase conventions.** The arc depends on where the Hilbert transform is applied (Table 2). Lead-1 is significant under
P, W, E and C but not N ($p =$ {{S31/P/conventions#N/arc/lead1/p|p}}), and on the 30 not under W
($p =$ {{S30/P/conventions#W/arc/lead1/p|p}}); the variance rise is significant under P and E but not W or N. The
synchronization–swing-size link holds under all five, with sizes from {{S31/P/conventions#N/amp_detrended/0|c3}} to
{{S31/P/conventions#C/amp_detrended/0|c3}}. We chose P before running anything on the added economies, on the ground
that its run-in protects 1970 from edge transients, not because it gives larger values.

**The dropped rate lead.** With two-sided phases short-term interest rates are most synchronized two years before
global recessions ({{S31/P/channels#sync/strate/tests/lead2/0|c3}}, $p =$ {{S31/P/channels#sync/strate/tests/lead2/1|p}},
{{S31/P/channels#sync/strate/n|int}} economies with continuous rates), but with phases from past data only the rise is gone
({{S31/C/channels#sync/strate/tests/lead2/0|c3}}, $p =$ {{S31/C/channels#sync/strate/tests/lead2/1|p}}). We make no claim
that rates or investment signal recessions in advance; the channel ordering is description only (Appendix Table A10).

**The alignment share is sample-sensitive.** Splitting the recession excess in world swing (the identity of Box 1)
into alignment and swing size gives an alignment share of {{S31/P/structure#align_share|pct0}} on the 31,
{{S30/P/structure#align_share|pct0}} on the 30, {{S30_minus_IRN/P/structure#align_share|pct0}} on the 30 without Iran
and {{S26/P/structure#align_share|pct0}} on the original 26. The swing-size part is significant on every sample
($p =$ {{S31/P/structure#p_swing|p}}, the floor, also against surrogates with ends); the alignment part on none
($p =$ {{S31/P/structure#p_align|p}} on the 31). The share depends on which economies are in the sample, and we draw no
conclusion from it.

**The mechanism check is narrow.** G1b tested one mechanism in one family of simulated worlds (Kuramoto oscillators on
the real 1970–2022 trade network), with recessions that do not feed back on the cycles and a calibration that fixes only how
often recessions happen. Its *partly* verdict says that this mechanism can leave a detectable past-only lead, not that
it produces the real one.

**Data.** Annual data give 53 points; Maddison's PPP series for Russia before 1991 are back-cast Soviet-era estimates
(every test is repeated with Russia's phases from 1992); Maddison's 1991–2011 growth for Norway, Switzerland and South
Africa runs above national accounts (replacing it changes no conclusion; §3.6.8). The five recession dates are those of
Kose, Sugawara and Terrones (2020) for 1975–2009 and of the World Bank (2020) for 2020, under the same definition.
