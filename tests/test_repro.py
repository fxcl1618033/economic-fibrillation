"""The EXACT / MATCH / DIFFERS rules in ef.repro (docs/decisions.md, 11 October 2026)."""
import json

from ef.repro import compare


def _pair(tmp_path, new, old):
    a, b = tmp_path / "new.json", tmp_path / "old.json"
    a.write_text(json.dumps(new)); b.write_text(json.dumps(old))
    return compare(a, b)


def test_identical_is_exact(tmp_path):
    assert _pair(tmp_path, {"x": [1.0, 2.0]}, {"x": [1.0, 2.0]}).status() == "EXACT"


def test_last_digit_noise_is_exact(tmp_path):
    assert _pair(tmp_path, {"x": 0.3 + 1e-15}, {"x": 0.3}).status() == "EXACT"


def test_float32_rounding_is_match(tmp_path):
    t = _pair(tmp_path, {"growth": 0.9193}, {"growth": 0.9191})
    assert t.status() == "MATCH" and t.status(allow_match=False) == "DIFFERS"


def test_phase_has_looser_limit(tmp_path):
    assert _pair(tmp_path, {"phase": 1.0012}, {"phase": 1.0}).status() == "MATCH"
    assert _pair(tmp_path, {"phase": 1.01}, {"phase": 1.0}).status() == "DIFFERS"


def test_real_change_differs(tmp_path):
    assert _pair(tmp_path, {"corr": 0.25}, {"corr": 0.266}).status() == "DIFFERS"


def test_any_p_value_change_differs(tmp_path):
    # a [statistic, p] pair under a test label, and a p_ key
    assert _pair(tmp_path, {"lead2": [0.2661, 0.0566]}, {"lead2": [0.2660, 0.0377]}).status() == "DIFFERS"
    assert _pair(tmp_path, {"p_sync": 0.0006}, {"p_sync": 0.0005}).status() == "DIFFERS"
    assert _pair(tmp_path, {"lead2": [0.2661, 0.0377]}, {"lead2": [0.2660, 0.0377]}).status() == "MATCH"


def test_text_and_missing_values_must_agree(tmp_path):
    assert _pair(tmp_path, {"src": "M3"}, {"src": "M2"}).status() == "DIFFERS"
    assert _pair(tmp_path, {"x": [1.0]}, {"x": [1.0, 2.0]}).status() == "DIFFERS"


def test_csv_rows_are_labelled(tmp_path):
    a, b = tmp_path / "a.csv", tmp_path / "b.csv"
    a.write_text("year,iso,phase,growth\n1986,CHN,0.5012,2.0\n"); b.write_text("year,iso,phase,growth\n1986,CHN,0.5,2.0\n")
    t = compare(a, b)
    assert t.status() == "MATCH" and t.max_abs_at == "phase[CHN 1986]"
