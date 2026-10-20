<!-- Data and code availability (Sid, 20 October 2026): the public repository and the tag of this version. -->
## Data and code availability

The code, the pinned data manifests, the pre-registrations, every results file and the figures are in the public
repository <https://github.com/fxcl1618033/economic-fibrillation>; the version described here is the tag `paper1-complete-v1.3`. Running `make reproduce`
regenerates every number in the paper from the pinned data and compares each file with the committed one; `make all`
is a quicker check. The data come from the Maddison Project Database 2023, the Global Macro Database, Penn World Table
10.01, the IMF, the BIS, the EIA and the World Bank, each pinned to a repository commit or a dated download with its
checksum (`data/sources.yaml`). Series from the Global Macro Database are not redistributed, as its terms require; the
repository rebuilds them from the pinned release. The code is under the MIT licence and the text, figures and results
under CC BY 4.0, except the outputs built on the Global Macro Database, which follow its terms (CC BY-NC-SA 4.0).
