# Source note for `trade_network.npz`

Built from the International Monetary Fund's International Trade in Goods by partner country (IMTS) and the World
Bank's GDP in current US dollars. Material transformation: each weight is the exports of one economy to another divided
by the importer's GDP, the mean of the exporter's and the importer's reports where both exist (`ef.gnn.simulator.trade_network`).
Source: International Monetary Fund, IMTS, data.imf.org; World Bank, World Development Indicators (CC BY 4.0). IMF data
are used under the IMF's terms (https://www.imf.org/en/About/copyright-and-terms). The other files in this folder are
simulation results under CC BY 4.0. See `DATA_LICENSES.md` at the top of the repository.
