# SemantiCAD MVP — Build Specification

> **Prompt for Claude Code:** Du baust einen Prototypen für SemantiCAD — eine Standalone-Desktop-App, die einen semantischen Wissens-Layer über CAD-Modelle legt. Dieses Dokument ist die vollständige Spezifikation. Arbeite die Phasen sequenziell ab. Frage nach, wenn etwas unklar ist. Liefere nach jeder Phase einen lauffähigen Zwischenstand mit einer kurzen Demo-Anleitung im README.

---

## 1. Produktidee in einem Absatz

SemantiCAD ist ein semantischer Layer über CAD/PLM. Er verknüpft Engineering-Erfahrungswissen ("tacit knowledge") und explizite Bauteilinformationen an konkrete Geometrie in 3D-Modellen — sodass das Wissen einer Ingenieursgeneration auch nach deren Renteneintritt für die nächste Generation und für AI-Agenten abrufbar bleibt. Der MVP demonstriert das Prinzip an einer Beispielanlage (Brownfield, statische CAD-Modelle) mit drei Agent-Modi: Wissens-Lookup, Root-Cause-Analyse und Design-Review.

## 2. Tech-Stack

- **Sprache:** Python 3.11+
- **3D-Engine:** PythonOCC-Core (OpenCascade-Wrapper) für STEP-Dateien
- **UI-Framework:** PyQt6
- **Datenbank:** SQLite (lokale Datei, Graph-imitierendes Schema)
- **AI-Agent:** Anthropic Python SDK mit Tool-Calling (Claude Opus 4.7 oder Sonnet 4.6)
- **Paketmanagement:** uv oder pip mit requirements.txt
- **Plattform:** Mac (Primary), Linux/Windows als Bonus

Alle Komponenten lokal lauffähig, keine Server-Infrastruktur nötig. App startet via `python -m semanticad`.

## 3. Architektur

```
┌─────────────────────────────────────────────────────┐
│  SemantiCAD Desktop App (PyQt6)                     │
│  ┌───────────────┬────────────────┬───────────────┐ │
│  │  3D Viewer    │  Side Panel    │  Chat Panel   │ │
│  │  (PythonOCC)  │  (Part Tree +  │  (Agent UI)   │ │
│  │               │   Knowledge)   │               │ │
│  └───────────────┴────────────────┴───────────────┘ │
└─────────────────────────────────────────────────────┘
              ↓                ↓             ↓
       ┌─────────────┐  ┌──────────┐  ┌────────────┐
       │ STEP Loader │  │ Data     │  │ Anthropic  │
       │ (OCC)       │  │ Layer    │  │ Agent      │
       └─────────────┘  │ (SQLite) │  │ (Tools)    │
                       └──────────┘  └────────────┘
```

**Strikte Trennung:** Datenmodell darf keine CAD-system-spezifischen Annahmen enthalten. `semantic_part_id` ist neutral; `cad_mappings` macht die Verbindung zu konkreten Systemen.

## 4. Datenmodell (SQLite)

```sql
CREATE TABLE parts (
    semantic_part_id TEXT PRIMARY KEY,       -- UUID, CAD-system-neutral
    canonical_name TEXT NOT NULL,            -- z.B. "Centrifugal Pump P-101"
    part_type TEXT,                          -- z.B. "Pump", "Valve", "Pipe"
    description TEXT,                        -- semantische Beschreibung (AI-generierbar)
    metadata JSON,                           -- alle CAD-Properties als JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cad_mappings (
    mapping_id TEXT PRIMARY KEY,
    semantic_part_id TEXT NOT NULL,
    cad_system TEXT NOT NULL,                -- z.B. "STEP", "FreeCAD", "Onshape"
    native_id TEXT NOT NULL,                 -- ID im jeweiligen System
    file_reference TEXT,                     -- Pfad zur Datei
    last_synced TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (semantic_part_id) REFERENCES parts(semantic_part_id)
);

CREATE TABLE knowledge_nodes (
    knowledge_id TEXT PRIMARY KEY,           -- UUID
    content TEXT NOT NULL,                   -- der Wissensinhalt
    category TEXT NOT NULL,                  -- "Failure Mode", "Maintenance",
                                             -- "Design Rationale", "Material Experience",
                                             -- "Operating Experience", "Safety Note"
    author TEXT,                             -- wer hat erfasst
    confidence REAL DEFAULT 1.0,             -- 0.0 bis 1.0
    references JSON,                         -- Links zu Dokumenten, Schadensfällen
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE anchors (
    anchor_id TEXT PRIMARY KEY,
    knowledge_id TEXT NOT NULL,
    semantic_part_id TEXT NOT NULL,
    relation_type TEXT DEFAULT 'applies_to', -- "applies_to", "warning_for", "experience_with"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (knowledge_id) REFERENCES knowledge_nodes(knowledge_id),
    FOREIGN KEY (semantic_part_id) REFERENCES parts(semantic_part_id)
);

CREATE INDEX idx_anchors_part ON anchors(semantic_part_id);
CREATE INDEX idx_anchors_knowledge ON anchors(knowledge_id);
CREATE INDEX idx_mappings_native ON cad_mappings(cad_system, native_id);
```

## 5. Agent-Tool-Layer (Python-Funktionen)

Die folgenden sechs Tools sind die stabile Schnittstelle für den Agent. Implementierung in SQLite jetzt, später migrierbar zu Neo4j ohne Interface-Änderung.

```python
def get_part_info(semantic_part_id: str) -> dict:
    """Vollständige Info zu einem Bauteil: Name, Typ, Beschreibung, Metadaten."""

def get_knowledge_for_part(semantic_part_id: str) -> list[dict]:
    """Alle Wissensknoten, die mit diesem Bauteil verankert sind."""

def search_knowledge_semantic(query: str, limit: int = 5) -> list[dict]:
    """Findet Wissensknoten nach Inhalt. MVP: SQLite-LIKE-Volltext.
    Phase 2: Embedding-basiert mit sentence-transformers."""

def find_similar_parts(semantic_part_id: str, limit: int = 5) -> list[dict]:
    """Bauteile mit gleichem Typ oder ähnlichen Eigenschaften."""

def get_related_knowledge(knowledge_id: str, limit: int = 5) -> list[dict]:
    """Wissensknoten gleicher Kategorie oder verlinkter Referenzen."""

def list_parts_by_type(part_type: str) -> list[dict]:
    """Alle Bauteile eines Typs (z.B. alle Pumpen in der Anlage)."""
```

Jedes Tool gibt strukturierte Dicts zurück, die der Agent direkt im Kontext nutzen kann. Tool-Definitionen für Anthropic API folgen dem offiziellen Schema (siehe Anthropic Tool-Use-Doku).

## 6. Build-Phasen

> **Wichtig:** Nach jeder Phase liefere einen lauffähigen Stand mit kurzem Demo-Befehl im README. Frage nach, bevor du zur nächsten Phase gehst.

### Phase 1 — 3D-Viewer-Fundament

**Ziel:** Lokale Desktop-App, die eine STEP-Datei lädt, anzeigt, navigierbar ist, und Klick-Selektion auf Bauteile unterstützt.

**Tasks:**
- Projekt-Setup: pyproject.toml mit Dependencies, `src/semanticad/` Struktur
- PyQt6-Mainwindow mit OCC-Viewer-Widget (siehe `OCC.Display.qtDisplay`)
- STEP-Datei via Dialog laden, anzeigen
- Mausnavigation: Rotate, Pan, Zoom
- Klick auf Bauteil → Hervorhebung + Ausgabe der Bauteil-ID in Side-Panel
- Bauteil-Hierarchie aus STEP extrahieren (XCAFDoc, Labels) und als Tree-View darstellen

**Akzeptanzkriterium:** Du kannst eine GrabCAD-STEP-Datei laden, das Modell drehen, ein Teil anklicken, und siehst seinen Namen im Side-Panel.

**Hinweise:**
- PythonOCC-Core Installation auf Mac: `pip install pythonocc-core` oder via conda-forge. Falls pip-Probleme: micromamba/conda-forge nutzen
- STEP-Bauteil-Namen liegen in `XCAFDoc_DocumentTool::ShapeTool()` mit Labels
- Beispiel-Code: STEP-Viewer-Pro auf GitHub als Referenz, aber sauberer neu schreiben

### Phase 2 — Datenmodell und Wissens-Anker

**Ziel:** Bauteile in DB importieren, Wissensanker setzen und visualisieren.

**Tasks:**
- SQLite-Schema implementieren (siehe Abschnitt 4)
- Beim Laden einer STEP-Datei: alle Bauteile in `parts` schreiben mit UUID als `semantic_part_id`, Eintrag in `cad_mappings` mit `cad_system="STEP"`, `native_id=<STEP-Label-ID>`
- "Wissen hinzufügen"-Dialog: Klick auf Bauteil → Button im Side-Panel → Pop-up mit Feldern (Kategorie-Dropdown, Inhalt-Textfeld, Autor, Konfidenz) → speichert Knoten und Anker
- Visuelle Markierung: Bauteile mit Ankern werden im 3D-Viewer farblich hervorgehoben (z.B. gelbe Umrandung oder dezenter Glow)
- Side-Panel zeigt für selektiertes Bauteil alle Wissensknoten als Liste
- Liste aller Wissensanker im Side-Panel mit Klick-zu-Bauteil-Navigation

**Akzeptanzkriterium:** Du kannst 5-10 Wissensknoten manuell anlegen, sie hängen sichtbar an Bauteilen, beim Wiederöffnen der App sind sie noch da.

**Demo-Daten:** Lege ein Script `scripts/seed_demo_data.py` bei, das 10 realistische Wissensknoten für ein Pumpenstations-Modell anlegt. Inhalte: Schadensfälle, Materialhinweise, Wartungserfahrungen, Design-Begründungen. Beispiel:
```
"Bei Schweißnaht zwischen Pumpengehäuse und Saugflansch muss auf 150°C vorgewärmt werden. 
Erfahrung aus Schadensfall S-2019-047: bei niedrigerer Vorwärmtemperatur trat Risswachstum auf. 
Bericht von Müller im PLM unter Doc-ID 4711."
```

### Phase 3 — Agent-Integration

**Ziel:** Chat-Interface, das den Wissens-Graphen für Engineering-Fragen nutzbar macht.

**Tasks:**
- Tool-Layer implementieren: die 6 Funktionen aus Abschnitt 5
- Tool-Definitionen für Anthropic API (JSON-Schema)
- Anthropic Python SDK anbinden: `anthropic.Anthropic()` Client, `messages.create()` mit `tools=` und Tool-Calling-Loop
- API-Key aus Umgebungsvariable `ANTHROPIC_API_KEY` oder lokaler `.env`-Datei
- Chat-Panel als drittes Widget im Mainwindow: Eingabefeld, Sendbutton, Antwort-Bereich
- System-Prompt für den Agent (siehe unten)
- Drei Test-Anfragen müssen funktionieren:
  1. Lookup: "Was muss ich über Pumpe P-101 wissen?"
  2. Root-Cause: "P-101 vibriert seit gestern. Was sind mögliche Ursachen?"
  3. Design-Review: "Wir wollen P-101 durch eine Pumpe mit höherer Förderhöhe ersetzen. Was sollten wir beachten?"

**System-Prompt-Entwurf:**
```
Du bist ein Engineering-Assistent für eine Industrieanlage. Du hast Zugriff auf einen 
semantischen Wissens-Graphen (SemantiCAD), der Ingenieurswissen mit konkreten Bauteilen 
in CAD-Modellen verknüpft.

Nutze die verfügbaren Tools, um:
- Wissensknoten zu Bauteilen zu finden
- Ähnliche Bauteile zu identifizieren
- Verwandtes Wissen über Kategoriegrenzen hinweg zu finden
- Semantische Suche im Wissens-Pool durchzuführen

Antworte präzise, technisch korrekt, und zitiere konkrete Wissensknoten mit ihrer ID 
und Quelle. Wenn du Wissen aus mehreren Knoten kombinierst, mache das transparent. 
Wenn keine relevanten Daten existieren, sage das ehrlich statt zu raten.
```

**Akzeptanzkriterium:** Alle drei Test-Anfragen liefern sinnvolle, auf den Wissens-Knoten basierende Antworten. Der Agent macht erkennbar Tool-Calls und kombiniert Ergebnisse.

### Phase 4 — Polish und Demo

**Ziel:** Zeigbarer Prototyp.

**Tasks:**
- UI aufräumen: Layout, Spacing, Fonts, kleines Logo
- README mit Screenshots, Setup-Anleitung, Demo-Workflow
- Demo-Script: `scripts/run_demo.sh` startet die App mit voreingestelltem Modell und Wissensdaten
- Optional: 5-Minuten-Demo-Video-Storyboard als Markdown

## 7. Demo-Story (Leitnarrativ)

Pumpenstation einer Industrieanlage, seit 15 Jahren in Betrieb. Senior-Engineer Müller geht in Rente. Vor dem Abschied verknüpft er sein Wissen mit den Bauteilen im CAD-Modell. Zwei Jahre später: Junior-Engineer Schmidt soll die Anlage warten. Er öffnet das Modell, fragt den Agent, bekommt sofort Müllers Erfahrungswissen kontextuell ausgespielt.

**CAD-Modell-Quelle:** GrabCAD nach "pumping station", "centrifugal pump assembly", "industrial pump" durchsuchen. Modell mit 20-50 Bauteilen wählen, STEP-Format. Falls keins direkt passt: ein einfacheres Pumpengehäuse-Modell reicht.

## 8. Akzeptanzkriterien — Gesamt-MVP

Der Prototyp ist erfolgreich, wenn alle folgenden Aussagen wahr sind:

1. Die App startet auf einem Mac mit einem einzigen Befehl
2. Eine STEP-Datei kann geladen, das Modell navigiert, Bauteile selektiert werden
3. Wissensknoten können per UI angelegt und an Bauteile verankert werden
4. Bauteile mit Ankern sind im 3D-Modell visuell erkennbar
5. Der Agent beantwortet alle drei Test-Szenarien sinnvoll und nutzt dabei den Knowledge-Graph
6. Die Datenbank persistiert über App-Neustarts hinweg
7. README erlaubt es einem fremden Entwickler, die App in unter 15 Minuten zum Laufen zu bringen

## 9. Was explizit NICHT zum MVP gehört

- Re-Anchoring bei Modelländerungen → Phase 2 des Produkts (post-MVP)
- Multi-CAD-Import (Onshape, SolidWorks, JT) → vorbereitet im Datenmodell, aber nicht implementiert
- Embedding-basierte semantische Suche → SQLite-LIKE-Volltext reicht
- Multi-User / Cloud-Sync → Single-User-DB
- Authentifizierung → entfällt für lokalen Prototypen
- Automatische Wissens-Extraktion aus Dokumenten → späteres Modul
- Capture-Interview-Workflow → eigenständige Phase
- LLM-generierte Bauteil-Beschreibungen → optionales Nice-to-have für Phase 4

## 10. Repo-Struktur (Vorschlag)

```
semanticad/
├── pyproject.toml
├── README.md
├── SEMANTICAD_MVP_SPEC.md      (dieses Dokument)
├── .env.example                 (für ANTHROPIC_API_KEY)
├── src/
│   └── semanticad/
│       ├── __init__.py
│       ├── __main__.py          (Entry-Point: python -m semanticad)
│       ├── viewer/              (PythonOCC + Qt-Widget)
│       ├── data/                (SQLite-Layer, Modelle)
│       ├── agent/               (Tool-Layer + Anthropic-Anbindung)
│       └── ui/                  (Mainwindow, Dialoge, Panels)
├── scripts/
│   ├── seed_demo_data.py
│   └── run_demo.sh
├── data/
│   ├── semanticad.db            (SQLite, in .gitignore)
│   └── models/                  (STEP-Dateien für Demo)
└── tests/
    └── (Basics, kein TDD-Zwang)
```

## 11. Kommunikation mit dem Builder

Frage nach, wenn:
- PythonOCC-Installation auf Mac unerwartete Probleme macht (Alternative: conda-forge)
- Ein STEP-Beispielmodell ausgesucht werden muss (zeige 2-3 Optionen, frage welches)
- UI-Entscheidungen Auswirkung auf den Demo-Eindruck haben (z.B. Highlighting-Stil)
- Tool-Definitionen unklare Semantik haben

Liefere nach jeder Phase:
- Lauffähigen Stand
- Kurzes Demo-Kommando im README
- 2-3 Sätze "Was steht als Nächstes"

---

**Start:** Beginne mit Phase 1, Task 1 (Projekt-Setup). Frage nach, wenn du Klarstellungen brauchst, bevor du Annahmen triffst.