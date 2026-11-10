SK      := vendor/pid-to-kg/skills/pid-to-kg/scripts
WORK    := work/pahala
PDF     := data/raw/pahala.pdf
PDF_URL := https://www.epa.gov/system/files/documents/2021-08/pahala-wwtp-design-build-drawings-2021-07-23.pdf
PDF_SHA := 6b61266b4fc32d6bd209648d8509d9e75be2d9bc584f499d855c2d4f16b8d0af
PAGES   := 9-14,21-22

.PHONY: fetch render graph test-vendor

# Download the source drawings (not committed, see data/README.md)
fetch:
	mkdir -p data/raw
	test -f $(PDF) || curl -sSL -A "Mozilla/5.0" -o $(PDF) "$(PDF_URL)"
	echo "$(PDF_SHA)  $(PDF)" | sha256sum -c -

# Classify pages, render tiles, collect text-layer hints
render: fetch
	python3 $(SK)/probe_pdf.py $(PDF) --work $(WORK) --plant-name "Pahala WWTP" --pages $(PAGES)
	python3 $(SK)/render_pages.py $(WORK)
	python3 $(SK)/make_hints.py $(WORK)

# Build graph.json, graph.duckdb, summary.md and qa_report.md from the committed page extractions
graph:
	python3 $(SK)/build_kg.py $(WORK) --plant-name "Pahala WWTP"

test-vendor:
	cd vendor/pid-to-kg && python3 -m pytest -q
