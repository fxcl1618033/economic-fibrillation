# Literature for DTT (diversification-type tipping)

Added 14 October 2026 for the DTT work package (theory box `docs/paper1_dtt_box_draft.md`; the G1b
pre-registration). Each reference was checked on 14 October 2026 against the publisher's listing or a bibliographic
database (sources under each entry). "Verified" means the authors, title, journal, volume, issue and pages were
confirmed; what is said about the content is from the abstract or from how other papers cite it, as stated.

## The four references

**Ashwin, P., Wieczorek, S., Vitolo, R. and Cox, P. (2012).** Tipping points in open systems: bifurcation,
noise-induced and rate-dependent examples in the climate system. *Philosophical Transactions of the Royal Society A*
370(1962), 1166–1184. doi:10.1098/rsta.2011.0306. An erratum appeared in 2013 (doi:10.1098/rsta.2013.0098).
**Verified** from the arXiv version (1103.0169), the erratum's record (which gives the article's DOI) and published
reference lists; the journal page itself was not opened. The issue is given as 1962 in most records and 1743 in one
reference list. Content (arXiv abstract): distinguishes bifurcation-induced, noise-induced and rate-induced tipping.
That noise-induced tipping gives no slowing-down warning is our reasoning from its definition — the attractor and its
stability do not change, the noise moves the state out of the basin — and is used in the box only as interpretation.

**Lucas, R. E., Jr. (1977).** Understanding business cycles. *Carnegie-Rochester Conference Series on Public Policy*
5, 7–29 (also in K. Brunner and A. Meltzer, eds., *Stabilization of the Domestic and International Economy*,
North-Holland). **Verified** (RePEc listing; Lucas's CV). The original text was not read: that it is the source of the
argument that independent sector- or firm-level shocks average out in the aggregate is **verified through secondary
sources** — Gabaix (2011) and later papers cite it for exactly this.

**Gabaix, X. (2011).** The granular origins of aggregate fluctuations. *Econometrica* 79(3), 733–772.
doi:10.3982/ECTA8769. **Verified** (Econometric Society listing; NBER w15286). Content (abstract): with fat-tailed firm
sizes the diversification argument fails — aggregate volatility decays like 1/ln N rather than 1/√N — and the
idiosyncratic shocks of the 100 largest US firms explain about a third of output-growth variation.

**Acemoglu, D., Carvalho, V. M., Ozdaglar, A. and Tahbaz-Salehi, A. (2012).** The network origins of aggregate
fluctuations. *Econometrica* 80(5), 1977–2016. doi:10.3982/ECTA9623. **Verified** (Econometric Society listing; MIT
DSpace). Content (abstract): with input–output linkages, sectoral shocks can produce aggregate fluctuations; sizable
aggregate volatility requires significant asymmetry in sectors' roles as suppliers ("cascade effects").

## Positioning

All four start from the same benchmark: shocks that are independent across units cancel in the aggregate, so
aggregate volatility shrinks like 1/√N (Lucas). Gabaix and Acemoglu et al. show that cancellation fails when the units
are unequal — in size (a few granular firms) or in network position (a few central suppliers). DTT says it also fails
when the units are aligned in time: the shock is common, and what cancels or not is the economies' *responses*, which
depend on where each is in its cycle. Spread-out phases cancel a common shock; aligned phases pass it through. The
generalized variance law holds both: its independent term (1 − ρ) Σ wᵢ²Aᵢ²/2 is a Herfindahl-type concentration (the
granular channel, with GDP weights), and its common term ρ|Σ wᵢ Aᵢ e^{iθᵢ}|²/2 is the alignment channel, which is
Paper 1's fibrillation identity. The two are complements, not rivals; the box says so in one sentence.

What DTT does **not** borrow from them: neither paper is about synchronization of cycles or about tipping. The tipping
reading comes from Ashwin et al. alone, and in Paper 1 it is interpretation, not a test.

## Sources checked

- [arXiv 1103.0169 (Ashwin et al.)](https://arxiv.org/pdf/1103.0169); [erratum record, University College Cork](https://research.ucc.ie/en/publications/erratum-tipping-points-in-open-systems-bifurcation-noise-included/)
- [Lucas's CV, University of Chicago](https://bpb-us-w2.wpmucdn.com/voices.uchicago.edu/dist/b/3069/files/2021/03/CV-Lucas-w-additions-Feb-2021-1.pdf); secondary use: [NBER w15286 (Gabaix)](https://nber.org/papers/w15286)
- [Econometrica listing, Gabaix (2011)](https://econometricsociety.org/publications/econometrica/2011/05/01/granular-origins-aggregate-fluctuations)
- [Econometrica listing, Acemoglu et al. (2012)](https://econometricsociety.org/publications/econometrica/browse/2012/09/01/network-origins-aggregate-fluctuations); [MIT DSpace](https://dspace.mit.edu/handle/1721.1/72578)
