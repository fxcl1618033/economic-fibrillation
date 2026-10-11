"""
Fetch every pinned data source in data/sources.yaml into data/raw/<dir> and verify its checksums.

    python3 tools/fetch_data.py            # fetch what is missing, then verify everything
    python3 tools/fetch_data.py --verify   # verify only

`sources`: GitHub repositories fetched blobless and sparse at a pinned commit, so only the listed files
are downloaded (about 20 MB in total).

`downloads`: files downloaded once from official sources (BIS, IMF). Their URLs serve the latest release,
so they are never downloaded again. A missing file is restored from its `archive` folder (a copy on Sid's
Mac) or from the gzip copy in data/archive/<dir>/, and a file listed with `from_zip` is unzipped from its
pinned zip. If neither copy exists the file is reported missing; for a source marked `optional` (BIS,
needed only for the GNN) that is a warning, not a failure. A changed checksum always fails.

The script stops with a non-zero exit code if any file is missing or its sha256 differs from the pin:
never build on unverified data.
"""
import argparse, gzip, hashlib, os, shutil, subprocess, sys, zipfile
import yaml

ap = argparse.ArgumentParser()
ap.add_argument("--raw", default="data/raw")
ap.add_argument("--verify", action="store_true")
args = ap.parse_args()
Y = yaml.safe_load(open("data/sources.yaml"))
S, DL = Y["sources"], Y.get("downloads", [])
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

def restore(s, f, p):
    """Bring back a missing pinned download from a local copy; never from the network."""
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if "from_zip" in f:
        z = os.path.join(os.path.dirname(p), f["from_zip"])
        if os.path.exists(z):
            with zipfile.ZipFile(z) as zf: zf.extract(f["path"], os.path.dirname(p))
            return "unzipped"
    if s.get("archive"):
        a = os.path.join(os.path.expanduser(s["archive"]), f["path"])
        if os.path.exists(a): shutil.copy2(a, p); return f"copied from {s['archive']}"
    g = os.path.join("data/archive", s["dir"], f["path"] + ".gz")
    if os.path.exists(g):
        with gzip.open(g, "rb") as src, open(p, "wb") as dst: shutil.copyfileobj(src, dst)
        return f"restored from {g}"
    return None

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
for s in DL:
    for f in sorted(s["files"], key=lambda f: "from_zip" in f):      # zips before the files unzipped from them
        p = os.path.join(args.raw, s["dir"], f["path"])
        how = restore(s, f, p) if not os.path.exists(p) and not args.verify else None
        if how: print(f"[{s['id']}] {f['path']}: {how}")
        ok = os.path.exists(p) and sha256(p) == f["sha256"]
        skip = not os.path.exists(p) and s.get("optional")
        bad += not ok and not skip
        note = "" if ok else ((" (missing)" if args.verify else " (missing: no local copy to restore; see data/sources.yaml)") if not os.path.exists(p) else " (checksum differs)")
        if skip: note += " - optional, needed only for the GNN"
        print(f"  {'ok ' if ok else ('-- ' if skip else 'BAD')} {s['id']:20s} {str(s['downloaded'])[:10]}  {f['path']}{note}")
print("all sources verified" if not bad else f"{bad} file(s) missing or changed")
sys.exit(1 if bad else 0)
