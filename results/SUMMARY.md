## Summary in plain words

Written by Claude after the pre-registered run, for Sid's review. Every number below is in the tables that follow. "S26
(P)" is the original sample rerun under the pre-registered conventions; S30 is read against it.

**What carries over to the 30 economies**

- **Synchronization rises before global recessions.** Lead-2 is +0.226 (p 0.038) and lead-1 +0.217 (p 0.019, the
  floor) on S30, almost the same as S26. Lead-1 is the robust part: it holds under P and the edge-robust E, with any one
  of the 30 economies left out (p ≤ 0.038), and with phases built from past data only (+0.369, p 0.038). Lead-2 does not
  survive past-only phases (−0.021) or convention W. It still rests on 2009 and 2020: without 2020, lead-1 is +0.10
  (p 0.32).
- **When the world synchronizes it swings harder.** The detrended correlation is +0.641 on S30 (shift p 0.019; surrogate
  p 0.0002), stronger than S26's +0.608, and holds under every convention, without any one added economy and without Iran
  and Saudi Arabia together (+0.620).
- **Co-movement supplies most of the extra world variance in recessions**: 83.3% (GDP weights) and 96.8% (equal) on
  S30, against 80.2% and 96.5% on S26 under the new window rule (the stored 82.4% used four recessions; the strict
  version reproduces it).
- **The network of cycles has tightened**, but less on S30: 1.62× (0.680 in 1979–89 against 0.421 in 2013–22),
  against 1.79× on S26. The added economies are less tightly tied to the rest in the last decade.
- **The economies still move nearly together**: the spread of phase leads is 0.535 years on S30 (lower tail p 0.0004).
- **Every channel is synchronized above chance** on both samples (p at the 0.0005 floor).

**What weakens or fails**

- **The collapse after recessions weakens.** After-2 is −0.236 (p 0.057) on S30, against −0.277 (p 0.019) on S26. It
  is also not significant under W, N, E or past-only phases, or without 2020. The post-crisis half of the arc is the
  fragile half. On S30 no lag survives Benjamini–Hochberg (q 0.094 for lead-1, after-2 and lead-2; on S26 lead-1 and
  after-2 had q 0.047).
- **The two-year short-rate lead does not survive past-only phases.** It replicates under P on S30 (+0.273, p 0.019,
  19 economies), but with past data only it is +0.151 (p 0.17) on S26 and +0.165 (p 0.15) on S30. By rule 7 it cannot be
  claimed as a lead. Investment's lead-2 also fails past-only (−0.085 on S26).
- **The alignment share of the recession excess in world swing falls** from 39% (S26) to 19% (S30), almost all because
  of Iran (33% without Iran; 37% without Iran and Saudi Arabia). The swing-size part stays significant (p 0.0002).
- **Inside the cross term, the balance shifts.** On S30 higher correlation supplies more of the rise than bigger swings
  (44% against 41%, GDP weights; 49% against 38%, equal), the reverse of S26 (33% against 53%). Both parts are positive,
  so "amplification transmitted by alignment" still describes it, but which part dominates depends on the sample.

**One null that is no longer null**

- **The variance of r rises before recessions under the paper's own convention P**: τ +0.438 (p 0.033) on S26 and
  +0.420 (p 0.037) on S30. The registry's null (p 0.107) was computed under W, as first run. It is also significant
  under E (S26 p 0.041) and in the strict inside-1970–2022 version (p 0.019 and 0.005, but on 2009 and 2020 only); not
  under W or N. Lag-1 autocorrelation stays null, and so do the coupling test and the MST contraction. Rising variance
  without rising autocorrelation is not the critical-slowing-down signature, which needs both; larger shocks to r would
  produce it alone. The Methods' "all null" no longer holds as written under P, though it does not bring back a
  bifurcation reading. How to word this is Sid's decision.

**Other checks**

- **Leaving each added economy out** changes little: lead-2 crosses to p 0.057 without China; after-2 becomes significant
  without Brazil (p 0.019); the autocorrelation trend flips sign near zero without Saudi Arabia.
- **Norway, Switzerland and South Africa with GMD growth** (issue 13) barely move anything; lead-2 on S26 goes from
  p 0.038 to 0.057.
- **The repaired budget channels shrink to 9 economies** (from 26 on the raw data): the repaired spending series start
  after 1965 for most economies, so they fail the coverage rule. Budget-channel results now rest on the United States,
  Japan, Canada, South Korea, India, South Africa, Norway, Greece and Thailand.
- **S26 numbers that change under the pre-registered conventions** (old → new; logged in `docs/decisions.md`): D1 82.4%
  → 80.2%; D7 35/50/14% → 33/53/14%; E7 0.403 → 0.445 years; E9 5.85 → 5.98 years; F1 −0.152 (p 0.757) → +0.027
  (p 0.456); F2 +0.295 (p 0.107) → +0.438 (p 0.033); F5 6.4/7.1 → 5.6/6.7; E4 detrended −0.086 (p 0.316) → −0.057 (p 0.356).
