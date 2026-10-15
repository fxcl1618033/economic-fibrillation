## 1 Introduction

Global recessions arrive everywhere at once. In 2009 25 of the 31 economies studied
here contracted, and in 2020 28; in the recessions of 1982 and 1991 the number was
9 and 9. A standard argument says this should
be rare. If disturbances to economies are independent, they cancel in the aggregate, and world output should vary
far less than any one economy; the argument is usually traced to Lucas (1977), and it implies that aggregate
volatility shrinks like one over the square root of the number of units. Two well-known results show when it fails.
Gabaix (2011) shows that it fails when units are unequal in size: if a few firms are very large, their own shocks do
not average out. Acemoglu et al. (2012) show that it fails when units are unequal in network position: if a few sectors
supply many others, their shocks spread instead of cancelling.

This paper studies a third way the argument fails: when the units are aligned in time. National business cycles are
oscillations. A disturbance common to all economies pushes an economy near the top of its cycle and one near the bottom
in opposite directions, so when cycles are spread out a common shock largely cancels in world output, and when they are
aligned it adds up. The world's diversification then depends not only on how many economies there are, or how large
or central they are, but on how synchronized their cycles happen to be. We ask whether that synchronization rises in
and before global recessions, and whether recessions look like the approach to a tipping point.

We treat each economy's 2–9 year cycle in real GDP per capita as a phase oscillator and measure how aligned the 31
economies are each year with the Kuramoto order parameter $r(t)$ (Kuramoto 1984; Pikovsky, Rosenblum and Kurths
2001). The economies produce about 81% of world
output over 1970–2022. Global recessions are the five dated by Kose and co-authors from world output: 1975, 1982, 1991,
2009 and 2020 (Kose and Terrones 2015; Kose, Sugawara and Terrones 2020). The question differs from that of the world
business-cycle factor (Kose, Otrok and Whiteman 2003), which measures how much economies move together on average;
we ask when they do. To ask whether recessions are tipping points we use the taxonomy of Ashwin et al. (2012):
bifurcation-induced tipping announces itself through critical slowing down (Scheffer et al. 2009), while noise-induced
tipping does not.

We find five things. (1) Synchronization and the size of the swings move together (detrended correlation
+0.646). (2) In recessions the world economy loses diversification: co-movement
supplies 84.3% of the extra variance of world output, with
correlation and swing size contributing about equally — amplification transmitted by alignment. In the language of the
effective number of independent economies, the 31 behave like about 3.5
on average and like about 1.1 in 2020. (3) The correlation network
of the business cycles has tightened about 1.6× since the 1980s. (4) Synchronization rises in the year
before global recessions, even with phases built from past data only (+0.379,
$p =$ 0.038), but this rests on two events, 2009 and 2020. (5) There is no critical
slowing down: the variance of synchronization rises before recessions while its autocorrelation does not, which, as an
interpretation, is what noise-induced rather than bifurcation-induced tipping would show.

We are as explicit about what we do not find. No lag of the lead–lag profile survives a correction for multiple
testing; the fall in synchronization after recessions is fragile and not claimed; the share of the recession excess
due to alignment changes with the sample. Simulated worlds with known coupling show that dating recessions from world
output builds some synchronization into them, which is why the lead claim rests on phases from past data only, and
that a synchrony-driven escape mechanism can leave a lead of this kind but rarely one as large as the real one (§5.4).
The paper makes no forecast. Every test, its direction and its sample were written down and committed before it was
run, and every result, null or not, is reported.

Section 2 describes the data and §3 the methods, including the size of every test on simulated worlds. Section 4 gives
the five results, §5 discusses what they mean, with the arithmetic of loss of diversification in Box 1, and §6–7 give
the limitations and the work that remains.
