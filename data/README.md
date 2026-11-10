# Data provenance

## Drawings: Pahala WWTP design/build drawings

| | |
|---|---|
| Source | US EPA, https://www.epa.gov/system/files/documents/2021-08/pahala-wwtp-design-build-drawings-2021-07-23.pdf |
| Found via | https://github.com/ScottDuncanAI/public-chemical-manufacturing-datasets (README, section on P&ID drawing sets; the link list is CC BY 4.0) |
| Downloaded | 2026-11-10, 7,302,619 bytes |
| SHA-256 | `6b61266b4fc32d6bd209648d8509d9e75be2d9bc584f499d855c2d4f16b8d0af` |
| Content | 25 pages. Pages 9 to 25 are P&IDs (drawings P-101, P-201 to P-211, P-401, P-501, P-601 to P-603), all vector with a text layer |
| Used in the demo | Pages 9 to 14, 21 and 22: the main liquid path from headworks to effluent disposal |

### Terms

- The file is a public record published by a US federal agency. No explicit license is attached to it.
- The drawings were prepared by an engineering consultant for the County of Hawaii. The consultant may hold copyright.
- For that reason the PDF, the rendered tiles and the text-layer hints are **not committed** to this repository. `make fetch` downloads the file and checks the hash.
- The extracted graph (tags, connections, positions) is committed as derived data.

### Caveat printed on every sheet

"These drawings were prepared for submission to EPA in July 2021 to provide a general understanding of the project concept and are not intended to reflect design requirements."

The plant graph therefore describes a concept design, not an as-built plant. Many instrument bubbles carry incomplete tag numbers.

## Synthetic data

`data/synthetic/` will hold generated history and know-how records (milestone M2). Every record carries `origin = 'synthetic'`. None of it is real plant history.
