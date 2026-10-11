"""
Fetch every pinned data source in data/sources.yaml into data/raw/<dir> and verify its checksums.

    python3 tools/fetch_data.py            # fetch what is missing, then verify everything
    python3 tools/fetch_data.py --verify   # verify only

Each source is a GitHub repository fetched blobless and sparse, so only the listed files are
downloaded (about 20 MB in total). The script stops with a non-zero exit code if any file is
missing or its sha256 differs from the pin: never build on unverified data.
"""
import argparse, hashlib, os, subprocess, sys
import yaml

ap = argparse.ArgumentParser()
ap.add_argument("--raw", default="data/raw")
ap.add_argument("--verify", action="store_true")
args = ap.parse_args()
S = yaml.safe_load(open("data/sources.yaml"))["sources"]
env = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1")

def git(*a, cwd=None):
    r = subprocess.run(["git", *a], cwd=cwd, env=env, capture_output=True, text=True)
    if r.returncode: raise SystemExit(f"git {' '.join(a)} failed:\n{r.stderr}")
    return r.stdout.strip()

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()

os.makedirs(args.raw, exist_ok=True)
bad = 0
for s in S:
    d = os.path.join(args.raw, s["dir"])
    if not args.verify:
        if not os.path.isdir(os.path.join(d, ".git")):
            print(f"[{s['id']}] cloning {s['repo']}")
            git("clone", "-q", "--filter=blob:none", "--no-checkout", f"https://github.com/{s['repo']}", d)
        git("sparse-checkout", "set", "--no-cone", *["/" + f["path"] for f in s["files"]], cwd=d)
        git("checkout", "-q", s["commit"], cwd=d)
    head = git("rev-parse", "HEAD", cwd=d) if os.path.isdir(os.path.join(d, ".git")) else "missing"
    for f in s["files"]:
        p = os.path.join(d, f["path"])
        ok = os.path.exists(p) and sha256(p) == f["sha256"]
        bad += not ok
        print(f"  {'ok ' if ok else 'BAD'} {s['id']:20s} {head[:10]}  {f['path']}")
print("all sources verified" if not bad else f"{bad} file(s) missing or changed")
sys.exit(1 if bad else 0)
