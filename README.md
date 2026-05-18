# SemantiCAD

Semantic knowledge layer over CAD models. Links engineering tacit knowledge to 3D geometry — making the expertise of one generation available to the next and to AI agents.

## Setup

### Option A — pip (recommended if pythonocc-core wheel is available)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pip install pythonocc-core
```

### Option B — conda-forge (most reliable on macOS, including Apple Silicon)

```bash
conda create -n semanticad python=3.11
conda activate semanticad
conda install -c conda-forge pythonocc-core
pip install -e ".[dev]"
```

### API Key

```bash
cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY=sk-ant-...
```

## Run

```bash
conda activate semanticad
python -m semanticad
# or (if conda not on PATH):
/Users/nickmllr8/opt/anaconda3/envs/semanticad/bin/python -m semanticad
```

---

## Demo — Phase 2 (Knowledge Anchors)

This demo shows how Müller (Senior Engineer) anchors tacit knowledge to CAD parts before retirement,
so Schmidt (Junior Engineer) can find it later.

```bash
# Step 1 — generate the demo STEP file (run once)
/Users/nickmllr8/opt/anaconda3/envs/semanticad/bin/python scripts/generate_demo_step.py

# Step 2 — seed 10 realistic engineering knowledge nodes (run once)
/Users/nickmllr8/opt/anaconda3/envs/semanticad/bin/python scripts/seed_demo_data.py

# Step 3 — launch the app
/Users/nickmllr8/opt/anaconda3/envs/semanticad/bin/python -m semanticad
```

Then in the app:
1. **File → Open STEP…** → select `data/models/pump_station.step`
2. Parts with knowledge anchors appear **gold** in the 3D viewer and marked with ★ in the tree
3. **Click any gold part** → see its knowledge nodes in the right panel
4. **Click "+ Add Knowledge"** to add your own knowledge node to any part
5. The **Knowledge Anchors** list (bottom-left) shows all anchors; click one to navigate

Navigation: Left-drag = Rotate · Middle-drag = Pan · Scroll = Zoom

---

## Demo — Phase 1 (3D Viewer only)

```bash
/Users/nickmllr8/opt/anaconda3/envs/semanticad/bin/python scripts/generate_demo_step.py
/Users/nickmllr8/opt/anaconda3/envs/semanticad/bin/python -m semanticad
# File → Open STEP… → select data/models/pump_station.step
# Click any part → see its name in the Side Panel
```

---

## Phase status

| Phase | Status | Description |
|-------|--------|-------------|
| 1 — 3D Viewer | ✅ done | STEP load, navigation, click-selection, part tree, color by type |
| 2 — Data Model | ✅ done | SQLite, knowledge anchors, visual highlight, seed data |
| 3 — Agent | ⏳ planned | Anthropic tool-calling, chat UI |
| 4 — Polish | ⏳ planned | Layout, README screenshots, demo script |
