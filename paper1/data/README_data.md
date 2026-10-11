# Data — Economic Fibrillation (Paper 1)

Panel of annual GDP for 26 economies, 1970–2023, for business-cycle
synchronization analysis (Kuramoto order parameter).

## Files
- `gdp_panel_wide_1970_2023.csv` — rows = year (1970–2023), columns = 26 countries. Best for quick plotting.
- `gdp_panel_long_1970_2023.csv` — tidy format: Year, CountryCode, Country, GDP_current_USD. Best for pandas.
- `prepare_data.py` — loads the panel; includes an optional switch to fetch **real** GDP (Maddison 2023) instead.

## The 26 economies
United States, United Kingdom, Germany, France, Italy, Japan, Canada, Spain,
Australia, South Korea, India, Mexico, Netherlands, Sweden, Switzerland,
Belgium, South Africa, Turkey, Norway, Austria, Denmark, Finland, Greece,
Portugal, Indonesia, Thailand.
(Chosen for continuous 1970–2023 coverage and a mix of advanced + large emerging economies.)

## Source and units
- **Source:** World Bank national accounts / OECD, via the `datasets/gdp` mirror
  (https://raw.githubusercontent.com/datasets/gdp/main/data/gdp.csv),
  World Bank indicator NY.GDP.MKTP.CD.
- **Unit:** GDP in **current US dollars** (nominal).

## IMPORTANT LIMITATION (state this in your Data section)
These figures are **current-dollar** GDP, so year-to-year changes mix three things:
real output, domestic inflation, and exchange-rate movements against the dollar.
The synchronization analysis band-passes log-GDP to the business-cycle frequency
band, which removes the slow inflation/exchange-rate *trend* — but short-lived
currency swings can still leak in as noise.

### Recommended upgrade: real (constant-price) GDP
For a more defensible version, use **real GDP per capita** from the Maddison
Project Database 2023 (constant 2011 international dollars, inflation- and
PPP-adjusted, coverage to 2022). `prepare_data.py` has a ready-to-run switch that
fetches it directly from Our World in Data. Do this for a robustness check, or as
your main series if you prefer. Cite it as:

> Bolt, Jutta and Jan Luiten van Zanden (2024), "Maddison style estimates of the
> evolution of the world economy: A new 2023 update", *Journal of Economic
> Surveys*, 1–41. DOI: 10.1111/joes.12618.

## How to cite the World Bank data
> World Bank, World Development Indicators, GDP (current US$), indicator
> NY.GDP.MKTP.CD. Accessed via the datasets/gdp GitHub mirror, 2026.

## Next step in the pipeline (not in these files)
From this panel: log-GDP → band-pass to the business-cycle band → Hilbert
transform → instantaneous phase per country → Kuramoto order parameter r(t) →
surrogate-data significance test. That analysis script comes next.
