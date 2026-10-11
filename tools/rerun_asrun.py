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
"""
import argparse, glob, json, math, os, shutil, subprocess, hashlib

ap = argparse.ArgumentParser()
ap.add_argument("--raw", default="data/raw")
ap.add_argument("--out", default="build/asrun")
ap.add_argument("--timeout", type=int, default=1800)
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

def diff(a, b, path=""):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b: out.append(f"{path}/{k}: missing"); continue
            out += diff(a[k], b[k], f"{path}/{k}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): return [f"{path}: length {len(a)} vs {len(b)}"]
        for i, (x, y) in enumerate(zip(a, b)): out += diff(x, y, f"{path}[{i}]")
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        if not (math.isnan(a) and math.isnan(b)) and abs(a - b) > 1e-9 * max(1, abs(b)): out.append(f"{path}: {a} vs {b}")
    elif a != b: out.append(f"{path}: {a!r} vs {b!r}")
    return out

def stored(name):
    base = os.path.basename(name)
    for d in ("paper1/results", "paper1/data"):
        if os.path.exists(f"{d}/{base}"): return f"{d}/{base}"

rows = []
env = dict(os.environ, MPLBACKEND="Agg")
for script, result in PAPER1:
    r = subprocess.run(["python3", f"{script}.py"], cwd=OUT, env=env, capture_output=True, text=True, timeout=args.timeout)
    open(f"{OUT}/log_{script}.txt", "w").write(r.stdout + r.stderr)
    if r.returncode: rows.append((script, "FAILED", r.stderr.strip().splitlines()[-1][:120] if r.stderr else "")); continue
    if result is None: rows.append((script, "ran", "prints only; compare the log by eye")); continue
    new, old = f"{OUT}/{result}", stored(result)
    if result.endswith(".json"):
        d = diff(json.load(open(new)), json.load(open(old)))
    else:
        import pandas as pd, numpy as np
        A, B = pd.read_csv(new), pd.read_csv(old)
        num = A.select_dtypes("number").columns
        d = [] if A.shape == B.shape and float(np.nanmax(np.abs(A[num].values - B[num].values))) == 0 else ["values differ"]
    rows.append((script, "EXACT" if not d else "DIFFERS", "; ".join(d[:3])))

# atlas chain: data.py -> stats.py -> sync.py, from patched copies (absolute paths)
A = f"{OUT}/atlas"; os.makedirs(A)   # data.py reads {ROOT}/internal/panel26_results.json, written by panel26.py above
for s in ("data.py", "stats.py", "sync.py"):
    src = open(f"atlas/{s}").read().replace("ROOT='/home/claude'", f"ROOT='{OUT}'").replace("/home/claude/ext/", f"{OUT}/ext/")
    open(f"{A}/{s}", "w").write(src)
for s in ("data.py", "stats.py", "sync.py"):
    r = subprocess.run(["python3", s], cwd=A, env=env, capture_output=True, text=True, timeout=args.timeout)
    if r.returncode: rows.append((f"atlas/{s}", "FAILED", r.stderr.strip().splitlines()[-1][:120])); break
else:
    for f in ("panel.csv", "global.csv", "meta.json", "stats.json", "sync.json"):
        same = hashlib.sha256(open(f"{A}/{f}", "rb").read()).hexdigest() == hashlib.sha256(open(f"atlas/{f}", "rb").read()).hexdigest()
        rows.append((f"atlas/{f}", "EXACT" if same else "DIFFERS", "byte-for-byte" if same else "checksum differs"))

rep = ["# As-run reproduction report", "", "| Script or file | Result | Note |", "|---|---|---|"]
rep += [f"| {a} | {b} | {c} |" for a, b, c in rows]
rep += ["", "Not run: " + "; ".join(f"{k} ({v})" for k, v in NOT_RUN.items())]
open(f"{OUT}/REPORT.md", "w").write("\n".join(rep) + "\n")
print("\n".join(rep))
