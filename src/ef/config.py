"""Repository paths, samples and pinned-source locations, read from configs/default.yaml and data/sources.yaml."""
import os
from functools import lru_cache

import yaml


def repo_root():
    """The repository root: $EF_ROOT if set, else the folder above src/."""
    return os.environ.get("EF_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


@lru_cache(maxsize=None)
def load(path="configs/default.yaml"):
    root = repo_root()
    cfg = yaml.safe_load(open(os.path.join(root, path)))
    cfg["paths"] = {k: os.path.join(root, v) for k, v in cfg["paths"].items()}
    cfg["root"] = root
    return cfg


def raw_file(source_id, path=None):
    """Absolute path of a pinned file (a source or a download in data/sources.yaml): data/raw/<dir>/<path>. With one
    listed file, `path` may be omitted."""
    cfg = load(); y = yaml.safe_load(open(cfg["paths"]["sources"]))
    for s in y["sources"] + y.get("downloads", []):
        if s["id"] == source_id:
            files = [f["path"] for f in s["files"]]
            if path is None:
                if len(files) != 1: raise ValueError(f"{source_id} has {len(files)} files; name one")
                path = files[0]
            if path not in files: raise ValueError(f"{path} is not pinned for {source_id}")
            return os.path.join(cfg["paths"]["raw"], s["dir"], path)
    raise KeyError(f"no pinned source {source_id!r} in data/sources.yaml")


def sample(name):
    return list(load()["samples"][name])
