"""
Write tests/golden_paper1.json: the headline numbers of every Paper 1 test, taken straight from the
stored results files, with a tolerance for each. A refactored pipeline (src/ef/...) run on the 26
economies with convention P must reproduce these before it is trusted on the 30.

Deterministic quantities get tolerance 1e-9. Surrogate p-values depend on the random stream, so a
reimplementation that draws surrogates in a different order gets a Monte Carlo tolerance instead:
3 standard errors of a binomial proportion with 5,000 draws, floored at 0.002.
"""
import json, math, os
R = "paper1/results"
J = lambda f: json.load(open(os.path.join(R, f)))
G = []
def det(key, val, src, note=""): G.append({"key": key, "value": val, "tol": 1e-9, "source": src, "note": note})
def mc(key, p, n, src, note=""):
    G.append({"key": key, "value": p, "tol": max(0.002, 3 * math.sqrt(max(p * (1 - p), 1e-12) / n)), "source": src,
              "note": (note + " " if note else "") + "surrogate p: exact only with the original random stream"})

kt = J("kose_terrones_results.json")
for lab, k in [("2 yr before", "lead2"), ("1 yr before", "lead1"), ("crisis year", "crisis"), ("1 yr after", "after1"), ("2 yr after", "after2")]:
    det(f"arc.P.{k}.corr", kt["arc"][lab]["corr"], "kose_terrones_results.json")
    det(f"arc.P.{k}.p_one_sided", kt["arc"][lab]["p_dir"], "kose_terrones_results.json", "circular shift, floor 1/53")
det("epoch.P.peak_t-1", kt["epoch_peak"], "kose_terrones_results.json")
det("epoch.P.t+2", kt["epoch_after2"], "kose_terrones_results.json")
det("r.P.1970", kt["r_by_year"]["1970"], "kose_terrones_results.json"); det("r.P.2020", kt["r_by_year"]["2020"], "kose_terrones_results.json")

cc = J("runin_convention_check.json")["results"]
for conv in "PWN":
    for k, (c, p) in cc[conv]["arc"].items():
        det(f"arc.{conv}.{k}.corr", c, "runin_convention_check.json"); det(f"arc.{conv}.{k}.p_one_sided", p, "runin_convention_check.json")
    det(f"amplitude.{conv}.detrended", cc[conv]["amp_detrended"][0], "runin_convention_check.json")
    det(f"amplitude.{conv}.raw", cc[conv]["amp_raw"][0], "runin_convention_check.json")

am = J("amplitude_results.json")
mc("amplitude.W.p_surrogate", am["p_surrogate"], 5000, "amplitude_results.json")

for f, w in [("diversification_results.json", "gdp_end_of_window"), ("diversification_equal_results.json", "equal")]:
    d = J(f)
    det(f"diversification.{w}.cross_fraction_of_excess", d["corr_fraction_of_excess"], f)
    det(f"diversification.{w}.cross_share_crisis", d["cross_share_crisis"], f)
    det(f"diversification.{w}.cross_share_normal", d["cross_share_normal"], f)

st = J("structure_results.json")
det("identity.alignment_share_of_crisis_excess", st["align_share"], "structure_results.json")
mc("identity.p_alignment", st["p_align"], 5000, "structure_results.json")
mc("identity.p_swing", st["p_swing"], 5000, "structure_results.json")
det("fiedler.lambda2", st["lambda2"], "structure_results.json")

ms = J("mst_results.json")
det("mst.L_1971", ms["L_by_year"]["1971"], "mst_results.json"); det("mst.L_2022", ms["L_by_year"]["2022"], "mst_results.json")
det("mst.pre_crisis_tau", ms["tau_L"], "mst_results.json"); mc("mst.p_contraction", ms["p_contraction"], 5000, "mst_results.json")

pl = J("phase_lag_results.json")
det("phase.lead_sd_years", pl["sd"], "phase_lag_results.json"); det("phase.mean_period_years", pl["period_years"], "phase_lag_results.json")

cs = J("csd_surrogate_results.json")
det("csd.ar1_tau", cs["tau_ar_real"], "csd_surrogate_results.json"); mc("csd.ar1_p", cs["p_ar"], 5000, "csd_surrogate_results.json")
det("csd.var_tau", cs["tau_va_real"], "csd_surrogate_results.json"); mc("csd.var_p", cs["p_va"], 5000, "csd_surrogate_results.json")

kb = J("kuramoto_bifurcation_results.json")
det("bifurcation.delta_lambda", kb["stat_real"], "kuramoto_bifurcation_results.json")
mc("bifurcation.p_slowing", kb["p_slowing_post"], 5000, "kuramoto_bifurcation_results.json")

rb = J("robustness_results.json")["baseline"]
for k, (c, p) in rb.items(): det(f"robustness.baseline.{k}.corr", c, "robustness_results.json")

sy = json.load(open("atlas/sync.json"))
for ch in ("GDP", "inv", "strate"):
    for k, (c, p) in sy["tests"][ch].items():
        det(f"atlas_sync.{ch}.{k}.corr", c, "atlas/sync.json"); det(f"atlas_sync.{ch}.{k}.p", p, "atlas/sync.json")

os.makedirs("tests", exist_ok=True)
json.dump({"about": "Paper 1 golden numbers, 26 economies, Maddison 2023 at the pinned commit; see tools/make_golden.py",
           "values": G}, open("tests/golden_paper1.json", "w"), indent=1)
print(len(G), "golden values written to tests/golden_paper1.json")
