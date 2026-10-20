"""
Re-run every as-run Paper 1 and atlas script exactly as it was written, against the pinned data,
and compare what it produces with the stored results. This is the regression baseline: any
refactor must keep reproducing these numbers (or explain, in docs/open_issues.md, why not).

    python3 tools/fetch_data.py          # first
    python3 tools/rerun_asrun.py         # writes build/asrun/ and build/asrun/REPORT.md

The as-run scripts use relative paths from the July–October sandboxes
(MaddisonData-main/..., ext/gmd/..., internal/..., /home/claude/...). This harness recreates that
layout with symbolic links inside build/asrun instead of editing the scripts; the two atlas
scripts with an absolute /home/claude path are run from patched copies.

Each row is EXACT, MATCH (differs only by floating-point rounding, no p-value changed; allowed only for outputs
built from the float32 GMD files: panel26 and the atlas) or DIFFERS;
atlas/panel.csv and atlas/global.csv are Global Macro Database series, whose terms do not allow re-hosting, so the
public repository does not hold them: they are checked against the sha256 pinned in data/sources.yaml (EXACT), or
against a stored copy given with --reference; without either they are NOT COMPARED (the derived stats.json and
sync.json, built from them, are still compared);
the rules are in src/ef/repro.py. The script exits with an error if any row is DIFFERS or FAILED.
Scripts that only print are compared line by line with paper1/results/printed/.
"""
import argparse, glob, os, shutil, subprocess, sys, hashlib
import yaml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from ef.repro import compare

ap = argparse.ArgumentParser()
ap.add_argument("--raw", default="data/raw")
ap.add_argument("--out", default="build/asrun")
ap.add_argument("--timeout", type=int, default=1800)
ap.add_argument("--reference", help="folder with stored copies of atlas files that are not distributed (panel.csv, global.csv)")
args = ap.parse_args()
ROOT = os.getcwd(); RAW = os.path.abspath(args.raw); OUT = os.path.abspath(args.out)
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(f"{OUT}/internal")
os.symlink(f"{RAW}/maddisondata", f"{OUT}/MaddisonData-main")
os.symlink(RAW, f"{OUT}/ext")
for p in glob.glob("paper1/scripts/eraA_claude_ai/*.py") + glob.glob("paper1/scripts/eraB_claude_code/*.py"):
    shutil.copy(p, OUT)
shutil.copy("paper1/data/gdp_panel_long_1970_2023.csv", OUT)
if os.path.exists(f"{RAW}/wbgdp/data/gdp.csv"): shutil.copy(f"{RAW}/wbgdp/data/gdp.csv", OUT)

# script -> stored result it must reproduce
PAPER1 = [("kose_terrones_test", "kose_terrones_results.json"), ("amplitude_test", "amplitude_results.json"),
          ("robustness", "robustness_results.json"), ("real_gdp_analysis", "crisis_results_real.json"),
          ("structure_tests", "structure_results.json"), ("crossterm_split", None),
          ("panel26", "internal/panel26_results.json"), ("usjp", None), ("phase_lags", "phase_lag_results.json"),
          ("csd_surrogate", "csd_surrogate_results.json"), ("kuramoto_bifurcation", "kuramoto_bifurcation_results.json"),
          ("diversification", "diversification_results.json"), ("diversification_equal", "diversification_equal_results.json"),
          ("mst_network", "mst_results.json"), ("crisis_analysis", "crisis_results.json"),
          ("hilbert_oscillators", "hilbert_output.csv"), ("surrogate_test", "surrogate_results.csv")]
NOT_RUN = {"crisis_dating_test": "needs jst.xlsx (not pinned)", "build_coupling_matrix": "needs the BIS LBS file (never downloaded)",
           "prepare_data": "fetches from the network; its output is paper1/data/gdp_panel_*.csv"}
FLOAT32 = {"panel26"}   # built from GMD (float32); MATCH allowed. Everything else must be EXACT
NOISE = ("Matplotlib is building the font cache", "RuntimeWarning: invalid value encountered in log")


def stored(name):
    base = os.path.basename(name)
    for d in ("paper1/results", "paper1/data"):
        if os.path.exists(f"{d}/{base}"): return f"{d}/{base}"


def printed_check(script):
    """Compare a script's printout with the stored one, ignoring warning paths and font-cache notices."""
    ref = f"paper1/results/printed/{script}_output.txt"
    if not os.path.exists(ref): return None
    clean = lambda p: [l.rstrip() for l in open(p) if not any(n in l for n in NOISE) and l.strip() != "warnings.warn("]
    new, old = clean(f"{OUT}/log_{script}.txt"), clean(ref)
    diff = [(a, b) for a, b in zip(new, old) if a != b] + ([("length", f"{len(new)} vs {len(old)} lines")] if len(new) != len(old) else [])
    return diff


rows = []
env = dict(os.environ, MPLBACKEND="Agg")
for script, result in PAPER1:
    r = subprocess.run([sys.executable, f"{script}.py"], cwd=OUT, env=env, capture_output=True, text=True, timeout=args.timeout)
    open(f"{OUT}/log_{script}.txt", "w").write(r.stdout + r.stderr)
    if r.returncode: rows.append((script, "FAILED", r.stderr.strip().splitlines()[-1][:120] if r.stderr else "")); continue
    pd_ = printed_check(script)
    pnote = "" if not pd_ else f"printout differs in {len(pd_)} line(s), e.g. {pd_[0][0].strip()!r} vs {pd_[0][1].strip()!r}"
    if result is None:
        rows.append((script, "EXACT" if pd_ == [] else ("ran" if pd_ is None else "DIFFERS"), pnote or "printout identical")); continue
    t = compare(f"{OUT}/{result}", stored(result))
    rows.append((script, t.status(allow_match=script in FLOAT32), "; ".join(x for x in (t.note(), pnote) if x)))

# atlas chain: data.py -> stats.py -> sync.py, from patched copies (absolute paths)
A = f"{OUT}/atlas"; os.makedirs(A)   # data.py reads {ROOT}/internal/panel26_results.json, written by panel26.py above
for s in ("data.py", "stats.py", "sync.py"):
    src = open(f"atlas/{s}").read().replace("ROOT='/home/claude'", f"ROOT='{OUT}'").replace("/home/claude/ext/", f"{OUT}/ext/")
    open(f"{A}/{s}", "w").write(src)
for s in ("data.py", "stats.py", "sync.py"):
    r = subprocess.run([sys.executable, s], cwd=A, env=env, capture_output=True, text=True, timeout=args.timeout)
    if r.returncode: rows.append((f"atlas/{s}", "FAILED", r.stderr.strip().splitlines()[-1][:120])); break
else:
    sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
    pinned = yaml.safe_load(open("data/sources.yaml"))["derived_checksums"]
    for f in ("panel.csv", "global.csv", "meta.json", "stats.json", "sync.json"):
        ref = f"atlas/{f}" if os.path.exists(f"atlas/{f}") else None
        if ref is None and args.reference and os.path.exists(os.path.join(args.reference, f)): ref = os.path.join(args.reference, f)
        if ref is None:                                       # not distributed (GMD terms): the pinned checksum only
            if sha(f"{A}/{f}") == pinned.get(f"atlas/{f}"): rows.append((f"atlas/{f}", "EXACT", "byte-for-byte with the sha256 pinned in data/sources.yaml"))
            else: rows.append((f"atlas/{f}", "NOT COMPARED", "not distributed (GMD terms); its sha256 differs from the one pinned on Linux x86; "
                                                             "compare with --reference <folder with a stored copy>"))
            continue
        if sha(f"{A}/{f}") == sha(ref): rows.append((f"atlas/{f}", "EXACT", "byte-for-byte" + ("" if ref.startswith("atlas/") else f" (reference {ref})"))); continue
        t = compare(f"{A}/{f}", ref)
        rows.append((f"atlas/{f}", t.status(), "not byte-identical; " + t.note() + ("" if ref.startswith("atlas/") else f" (reference {ref})")))

rep = ["# As-run reproduction report", "",
       "EXACT: every number within 1e-9 (relative). MATCH: differs only by floating-point rounding (within 1e-3, phases",
       "within 0.005 rad), no p-value changed; allowed only for outputs built from the float32 GMD files (panel26, atlas).",
       "DIFFERS: anything else. NOT COMPARED: a file the public repository does not hold (GMD terms) whose checksum",
       "differs from the pinned one and for which no --reference copy was given. Rules in `src/ef/repro.py`.", "",
       "| Script or file | Result | Note |", "|---|---|---|"]
rep += [f"| {a} | {b} | {c} |" for a, b, c in rows]
rep += ["", "Not run: " + "; ".join(f"{k} ({v})" for k, v in NOT_RUN.items())]
open(f"{OUT}/REPORT.md", "w").write("\n".join(rep) + "\n")
print("\n".join(rep))
bad = [a for a, b, _ in rows if b in ("DIFFERS", "FAILED")]
if bad: sys.exit(f"\n{len(bad)} row(s) not reproduced: {', '.join(bad)}")
