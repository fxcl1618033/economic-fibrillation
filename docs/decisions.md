# Decision log

Newest last. Each entry: date, decision, reason, alternative rejected. Append; do not rewrite history.

| Date | Decision | Why | Rejected alternative |
|---|---|---|---|
| Jul–Aug 2026 | Use Maddison 2023 real GDP per capita | Current-dollar GDP mixes real output with inflation and exchange-rate swings | World Bank current US$ (kept as the superseded first pass) |
| Jul–Aug 2026 | 2–9 year Butterworth band-pass, order 2, forward–backward; run-in from 1950, statistics on 1970–2022 | Conventional business-cycle band, zero phase shift, edge protection for 1970 | Shorter band or no run-in (reported as robustness) |
| Jul–Aug 2026 | Date crises by Kose–Terrones global recessions (1975, 1982, 1991, 2009, 2020) | External, real-activity dating with five events | Hand-picked windows (circular) and JST banking crises (one global event) |
| Jul–Aug 2026 | Significance by circular shift (floor 0.019) and 5,000 spectrum-preserving surrogates | Keeps autocorrelation and spacing; tests coupling against spectrally identical uncoupled worlds | Parametric tests that assume independence |
| Aug 2026 | Report the critical-slowing-down nulls and frame them with the Ashwin et al. (2012) tipping taxonomy | A null that rules out bifurcation-induced tipping is informative | Dropping the nulls |
| Aug–Sep 2026 | Paper 1 closed to new tests | Analysis and Methods complete | — |
| 9 Oct 2026 | Paper 1 reopened: deeper economics mechanism, wider sample | Sid: stronger, more representative evidence | — |
| 10 Oct 2026 | Atlas second edition adds China, Brazil, Saudi Arabia, the UAE and Iran, compared with the 26 but never pooled into their averages | Keep the first edition's numbers unchanged | Re-basing all averages on 31 |
| 10 Oct 2026 | Working main sample S30 (UAE out), S26 frozen reference, S31 sensitivity — **pending Sid's confirmation** | Representation without an unbalanced panel; the UAE's Maddison series misses 1991–1992 | Pooling all 31 |
| 10 Oct 2026 | Diversification finding reworded to "amplification transmitted by alignment" | The cross-term split shows swing size supplies about half of the cross term's rise | "Correlation events, not volatility events" |
| 11 Oct 2026 | Repository snapshot, pinned sources and as-run reproduction harness; every stored result reproduces exactly | Reproducibility before any rerun | Rebuilding from memory of the scripts |
| 11 Oct 2026 | Phase-convention dependence of the arc recorded as open issue 1; decision on wording left to Sid | Under W and N the lead-1 test is not significant | Silently keeping convention P |
