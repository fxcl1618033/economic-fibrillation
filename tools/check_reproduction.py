"""After `make reproduce`: compare every regenerated file with the committed one (git HEAD).

    python3 tools/check_reproduction.py        # writes build/REPRODUCE.md; exits with an error if anything DIFFERS

JSON, CSV (also gzipped) and NPZ files are compared number by number with the rules of src/ef/repro.py (EXACT: within
1e-9; MATCH: floating-point rounding only, no p-value changed, allowed only for outputs built from the float32 Global
Macro Database files), ignoring the fields that record when and from which commit a file was made (run_at,
code_version). Markdown, TeX and text files are compared line by line with commit hashes and timestamps masked.
Figures (PNG, PDF) and zip files are listed but not compared: their bytes carry creation dates.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from ef.repro import compare  # noqa: E402

FOLDERS = ["results", "gnn", "dtt", "paper1/manuscript", "docs/methods.md", "figures"]
IGNORE_KEYS = {"run_at", "code_version"}
GMD = re.compile(r"gmd|channel|atlas|panel26|usjp|followup", re.I)
MASK = [(re.compile(r"\b[0-9a-f]{7,40}\b(\+uncommitted)?"), "<hash>"),
        (re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2})?(\.\d+)?(Z|[+-]\d{2}:?\d{2})?"), "<time>")]


def git(*a): return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout


def head_copy(path, tmp):
    p = os.path.join(tmp, path.replace("/", "__")); open(p, "wb").write(subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, check=True).stdout)
    return p


def strip(x):
    if isinstance(x, dict): return {k: strip(v) for k, v in x.items() if k not in IGNORE_KEYS}
    if isinstance(x, list): return [strip(v) for v in x]
    return x


def check(path, tmp):
    old = head_copy(path, tmp); ext = path.split(".")[-1] if not path.endswith(".gz") else path.split(".")[-2] + ".gz"
    if ext in ("png", "pdf", "zip"): return "NOT COMPARED", "figure or archive (bytes carry creation dates)"
    if ext == "json":
        a, b = os.path.join(tmp, "new.json"), os.path.join(tmp, "old.json")
        json.dump(strip(json.load(open(path))), open(a, "w")); json.dump(strip(json.load(open(old))), open(b, "w"))
        t = compare(a, b); return t.status(allow_match=bool(GMD.search(path))), t.note()
    if ext in ("csv", "csv.gz"):
        t = compare(path, old); return t.status(allow_match=bool(GMD.search(path))), t.note()
    if ext == "npz":
        A, B = np.load(path), np.load(old)
        if sorted(A.files) != sorted(B.files): return "DIFFERS", "different arrays"
        num = [k for k in A.files if A[k].dtype.kind in "fiuc" and A[k].size]
        bad = [k for k in A.files if A[k].shape != B[k].shape]
        if bad: return "DIFFERS", f"{bad[0]}: shape {A[bad[0]].shape} vs {B[bad[0]].shape}"
        worst = max((float(np.nanmax(np.abs(A[k] - B[k]))) for k in num), default=0.0)
        if any(not np.array_equal(A[k], B[k]) for k in A.files if k not in num): return "DIFFERS", "non-numeric arrays differ"
        return ("EXACT", "") if worst <= 1e-9 else ("DIFFERS", f"largest difference {worst:.2g}")
    norm = lambda s: [re.sub(MASK[1][0], MASK[1][1], re.sub(MASK[0][0], MASK[0][1], l)) for l in s.splitlines()]
    a, b = norm(open(path, encoding="utf-8", errors="replace").read()), norm(open(old, encoding="utf-8", errors="replace").read())
    if a == b: return "EXACT", "text identical apart from commit hashes and timestamps"
    i = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    return "DIFFERS", f"line {i + 1}: {(a[i] if i < len(a) else '<end>')[:90]!r} vs {(b[i] if i < len(b) else '<end>')[:90]!r}"


def main():
    changed = [p for p in git("diff", "--name-only", "HEAD", "--", *FOLDERS).split() if os.path.exists(p)]
    new = [l[3:] for l in git("status", "--porcelain", "--untracked-files=all", "--", *FOLDERS).splitlines() if l.startswith("??")]
    tracked = git("ls-files", "--", *FOLDERS).split(); rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for p in changed: rows.append((p, *check(p, tmp)))
    n_same = len(tracked) - len(changed)
    L = ["# Reproduction check", "", f"Files under {', '.join(FOLDERS)} compared with the committed versions (git HEAD). "
         f"{n_same} of {len(tracked)} tracked files came out byte-identical; the {len(changed)} that did not are listed below. "
         "Rules in `src/ef/repro.py`; run_at and code_version ignored; hashes and timestamps masked in text.", "",
         "| File | Result | Note |", "|---|---|---|"] + [f"| `{p}` | {s} | {n} |" for p, s, n in rows]
    if new: L += ["", "New files the rerun wrote that are not in the repository:", ""] + [f"- `{p}`" for p in new]
    counts = {s: sum(r[1] == s for r in rows) for s in ("EXACT", "MATCH", "DIFFERS", "NOT COMPARED")}
    L += ["", f"Byte-identical {n_same}; " + "; ".join(f"{k} {v}" for k, v in counts.items()) + "."]
    os.makedirs("build", exist_ok=True); open("build/REPRODUCE.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
    if counts["DIFFERS"]: sys.exit(f"{counts['DIFFERS']} file(s) differ")


if __name__ == "__main__":
    main()
