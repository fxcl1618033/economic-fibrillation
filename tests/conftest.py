"""Shared, session-wide fixtures: each expensive build or run happens once per pytest session."""
import os

import pytest

from ef import config


def _have_data():
    return os.path.exists(config.raw_file('maddison'))


needs_data = pytest.mark.skipif(not _have_data(), reason="pinned data not fetched: run make data")


@pytest.fixture(scope='session')
def built(tmp_path_factory):
    """The data build as used (GMD read as float64), in a temporary folder."""
    from ef.data import build
    out = tmp_path_factory.mktemp('data'); build.main(['--out', str(out), '--quiet']); return out


@pytest.fixture(scope='session')
def built32(tmp_path_factory):
    """The data build at the as-run scripts' precision (GMD as float32)."""
    from ef.data import build
    out = tmp_path_factory.mktemp('data32'); build.main(['--out', str(out), '--quiet', '--float32']); return out


@pytest.fixture(scope='session')
def paper1():
    """Every Paper 1 test under the as-run config (configs/runs/paper1_S26_asrun.yaml), about 12 seconds."""
    from ef import paper1 as p1
    return p1.run(p1.load_run_config(os.path.join(config.repo_root(), 'configs/runs/paper1_S26_asrun.yaml')))['results']
