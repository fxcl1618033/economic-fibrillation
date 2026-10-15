## 7 Future work

Paper 1 is closed to new tests. What follows is the programme for a second paper, which has not been started.

**A graph neural network of coupled economies (stages G2–G4).** A first stage built yearly graphs of the 31 economies
with pinned trade, bank-lending and oil links and a world node (G0), and a simulator of coupled economies with known
coupling run through this paper's pipeline (G1, used in §5.4). The next stages are: G2, a recoverability benchmark that
asks which couplings 53 annual points can reveal at all, and by which method; G3, a model of the real network, trained
only after G2 and checked against a twin with no network, shuffled edges, leave-one-recession-out validation, past-only
phases and classical baselines (a trade-weighted global VAR, a Kuramoto regression, a network autoregression); and G4,
explanations of what the model learned, counted only after the same explanation method recovers known links in the
simulator. The aim is to understand which links carry synchronization, not to forecast recessions.

**Channel experiments.** The channels inside each economy (interest rates, investment, trade, budgets) synchronize at
different times around recessions with two-sided phases, but no channel lead survives past-only phases. Testing the
ordering properly needs the channel data to be extended and the past-only design to be fixed in advance for each
channel.

**The remaining DTT modules.** The diversification-type tipping report (Sid, 13 October 2026) has modules this paper
does not use: cascades between economies, asymmetric restoring forces and hysteresis. Each needs its own
pre-registration and a check in the simulator, where the coupling can be raised step by step to test whether loss of
diversification has a threshold. Rate-induced tipping, where the speed of a change rather than its size causes the
transition, is a further hypothesis for that work.

**Data for 2023–2025.** The most recent recession sits two years from the end of the sample, where the filters are least
reliable. Extending the series by three years, when Maddison's next release covers them, is the cleanest test of the
2020 result and of the fall after recessions.

**A quarterly track.** Quarterly national accounts would give four times as many points but start around 1981 and lose
the 1975 recession; a quarterly version is a test of whether the annual results survive finer timing, not a
replacement.

**Banking-crisis dating.** The dates of systemic banking crises (the Jordà–Schularick–Taylor database), tried early in
this project, were not re-verified on pinned data; no claim here depends on them.
