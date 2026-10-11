"""data/sources.yaml and configs parse, and every pinned entry has what fetch_data.py needs."""
import glob
import os

import yaml

from ef import config

ROOT = config.repo_root()


def test_sources_yaml_parses_and_is_complete():
    Y = yaml.safe_load(open(os.path.join(ROOT, 'data/sources.yaml')))
    for s in Y['sources']:
        assert {'id', 'repo', 'dir', 'commit', 'files'} <= set(s), s.get('id')
    for s in Y['downloads']:
        assert {'id', 'url', 'downloaded', 'dir', 'files'} <= set(s), s.get('id')
    for s in Y['sources'] + Y['downloads']:
        for f in s['files']:
            assert len(f['sha256']) == 64 and f['bytes'] > 0, (s['id'], f['path'])


def test_configs_parse():
    for p in glob.glob(os.path.join(ROOT, 'configs', '**', '*.yaml'), recursive=True):
        assert isinstance(yaml.safe_load(open(p)), dict), p
