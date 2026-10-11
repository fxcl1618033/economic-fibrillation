# data/

- `sources.yaml` — every source pinned to a repository commit, with the files used, their sha256 and the scripts that
  read them. Also the checksums of the derived atlas files.
- `raw/` — created by `python3 tools/fetch_data.py` (git-ignored). Layout: `raw/maddisondata`, `raw/gmd`, `raw/pwt10`,
  `raw/owid`, `raw/oilprices`, `raw/wbgdp`, each a sparse checkout at its pinned commit.

Derived data live with the code that made them: `atlas/` (panel.csv, global.csv, meta.json, stats.json, sync.json) and
`paper1/data/` (the superseded current-dollar panels).

Adding a source: download once into `raw/<dir>`, add an entry to `sources.yaml` (URL or repository, commit or download
date, every file with sha256, what uses it, how to cite it), run `python3 tools/fetch_data.py --verify`, and only then
let code read it.
