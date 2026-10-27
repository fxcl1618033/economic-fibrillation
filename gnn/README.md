# GNN stages G0, G1 and G1b — Economic Fibrillation

These stages support Paper 1. They build the data a network model would need and use simulated economies to measure
what Paper 1's tests can and cannot detect. No model is trained on real data here.

| Stage | What it is | Report | Code | Make target |
|---|---|---|---|---|
| G0 | A yearly graph of the 31 economies (S31) for 1970–2022 with trade, bank-lending and oil edges, built from pinned data | `G0_data_card.md`, `G0_missing_data.md`, `G0/` | `src/ef/gnn/dataset.py`, `report.py` | `make gnn-g0` |
| G1 | Kuramoto and Stuart–Landau worlds with known coupling on the real trade network, pushed through the exact Paper 1 pipeline: the size and power of every Paper 1 test (pre-registration `docs/preregistration_G1.md`) | `G1_report.md`, `G1_closing.md`, `G1/` | `src/ef/gnn/simulator.py`, `g1.py` | `make gnn-g1` |
| G1b | A synchrony-driven escape layer on the G1 worlds: does it reproduce Paper 1's past-only lead? (pre-registration `docs/preregistration_G1b_dtt.md`) | `G1b_report.md`, `G1b/` | `src/ef/gnn/g1b.py` | `make gnn-g1b` |

The graph dataset itself is built on your machine into `build/gnn/g0` (`make gnn-g0`); its bank-lending edges need
the BIS bulk file (see `data/sources.yaml`). Sources and terms: `G0/NOTICE.md`, `G1/NOTICE.md` and `DATA_LICENSES.md`.
