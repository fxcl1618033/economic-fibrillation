"""Compare a rerun output with a stored result: EXACT, MATCH (to rounding) or DIFFERS.

The stored results were made on a Linux x86 machine. The Global Macro Database loads as single precision
(float32), and NumPy computes logs of float32 numbers with chip-specific routines, so on another chip the
last digit of a log can differ. Those differences propagate into anything built from GMD data. The rules
below separate that from a real change (decision of 11 October 2026 in docs/decisions.md).

EXACT    every number within 1e-9 x max(1, |stored|); text and missing values identical.
MATCH    allowed only for outputs built from float32 sources (the GMD files); every number within
         1e-3 x max(1, |stored|), phase angles (any field whose name contains "phase") within 0.005 radians;
         every p-value identical; text and missing values identical.
DIFFERS  anything else.

Why 1e-3: a float32 log of a level up to about e^35 carries an error up to about 35 x 6e-8 = 2e-6; a growth
rate in percent takes the difference of two logs times 100, so up to about 4e-4. Phase angles are looser
because a phase turns sharply in years when the cycle's swing is close to zero.
"""
import json, math, re

EXACT_TOL = 1e-9
MATCH_TOL = 1e-3
PHASE_TOL = 5e-3
P_TOL = 1e-12
TEST_LABELS = {"lead2", "lead1", "same", "crisis", "after1", "after2"}   # [statistic, p] pairs
P_KEY = re.compile(r"^p($|_|val)|_p$")


def _is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _isnan(x):
    return isinstance(x, float) and math.isnan(x)


class Tally:
    """Collects every compared value and the largest differences."""

    def __init__(self):
        self.n = 0; self.n_diff = 0
        self.max_abs = 0.0; self.max_abs_at = None
        self.max_scaled = 0.0; self.max_scaled_at = None      # |d| / max(1, |stored|)
        self.over_match = []; self.p_changes = []; self.other = []

    def number(self, path, field, new, old, is_p=False):
        self.n += 1
        if _isnan(new) or _isnan(old):
            if not (_isnan(new) and _isnan(old)): self.other.append(f"{path}: missing in one ({new!r} vs {old!r})")
            return
        d = abs(new - old)
        if d == 0: return
        self.n_diff += 1
        scaled = d / max(1.0, abs(old))
        if d > self.max_abs: self.max_abs, self.max_abs_at = d, path
        if scaled > self.max_scaled: self.max_scaled, self.max_scaled_at = scaled, path
        if is_p and d > P_TOL: self.p_changes.append(f"{path}: {new!r} vs {old!r}")
        tol = PHASE_TOL if "phase" in field.lower() else MATCH_TOL * max(1.0, abs(old))
        if d > tol: self.over_match.append(f"{path}: {new!r} vs {old!r}")

    def status(self, allow_match=True):
        if self.other: return "DIFFERS"
        if self.max_scaled <= EXACT_TOL: return "EXACT"
        if allow_match and not self.over_match and not self.p_changes: return "MATCH"
        return "DIFFERS"

    def note(self):
        if self.other: return "; ".join(self.other[:3])
        if self.max_scaled <= EXACT_TOL: return ""
        s = f"{self.n_diff} of {self.n} numbers differ; largest {self.max_abs:.2g} at {self.max_abs_at}"
        if self.p_changes: s += f"; p-values changed: {'; '.join(self.p_changes[:3])}"
        elif self.status() == "MATCH": s += "; no p-value changed"
        if self.over_match: s += f"; beyond rounding: {'; '.join(self.over_match[:3])}"
        return s


def _walk_json(new, old, t, path="", field="", parent=""):
    if isinstance(old, dict) and isinstance(new, dict):
        for k in sorted(set(old) | set(new), key=str):
            if k not in old or k not in new: t.other.append(f"{path}/{k}: missing in one"); continue
            _walk_json(new[k], old[k], t, f"{path}/{k}", str(k), field)
    elif isinstance(old, list) and isinstance(new, list):
        if len(old) != len(new): t.other.append(f"{path}: length {len(new)} vs {len(old)}"); return
        pair = field in TEST_LABELS and len(old) == 2
        for i, (x, y) in enumerate(zip(new, old)):
            if pair and i == 1 and _is_num(x) and _is_num(y): t.number(f"{path}[1]", field, x, y, is_p=True)
            else: _walk_json(x, y, t, f"{path}[{i}]", field, parent)
    elif _is_num(old) and _is_num(new):
        t.number(path, field, float(new), float(old), is_p=bool(P_KEY.search(field)))
    elif old != new and not (_isnan(old) and _isnan(new)):
        t.other.append(f"{path}: {new!r} vs {old!r}")


def compare_json(new_path, old_path):
    t = Tally(); _walk_json(json.load(open(new_path)), json.load(open(old_path)), t); return t


def compare_csv(new_path, old_path):
    import pandas as pd
    A, B = pd.read_csv(new_path), pd.read_csv(old_path)
    t = Tally()
    if list(A.columns) != list(B.columns) or A.shape != B.shape:
        t.other.append(f"shape or columns differ: {A.shape} vs {B.shape}"); return t
    key = [c for c in ("iso", "year") if c in B.columns]
    label = (B[key].astype(str).agg(" ".join, axis=1) if key else B.index.astype(str)).tolist()
    for c in B.columns:
        a, b = A[c], B[c]
        if pd.api.types.is_numeric_dtype(b) and pd.api.types.is_numeric_dtype(a) and not pd.api.types.is_bool_dtype(b):
            for i, (x, y) in enumerate(zip(a.astype(float), b.astype(float))):
                t.number(f"{c}[{label[i]}]", c, x, y, is_p=bool(P_KEY.search(c)))
        else:
            same = (a.isna() & b.isna()) | (a.astype(str) == b.astype(str))
            for i in [i for i, s in enumerate(same) if not s][:3]: t.other.append(f"{c}[{label[i]}]: {a.iloc[i]!r} vs {b.iloc[i]!r}")
    return t


def compare(new_path, old_path):
    """Return a Tally for two result files (.json or .csv)."""
    return compare_json(new_path, old_path) if str(old_path).endswith(".json") else compare_csv(new_path, old_path)
