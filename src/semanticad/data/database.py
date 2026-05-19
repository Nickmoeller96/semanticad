"""SQLite database — schema creation and connection management."""

import sqlite3
from pathlib import Path

_PACKAGE_DIR = Path(__file__).parent          # src/semanticad/data/
_PROJECT_ROOT = _PACKAGE_DIR.parent.parent.parent  # semanticad/
DB_PATH = _PROJECT_ROOT / "data" / "semanticad.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS parts (
    semantic_part_id TEXT PRIMARY KEY,
    canonical_name   TEXT NOT NULL,
    part_type        TEXT,
    description      TEXT,
    metadata         JSON,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cad_mappings (
    mapping_id       TEXT PRIMARY KEY,
    semantic_part_id TEXT NOT NULL,
    cad_system       TEXT NOT NULL,
    native_id        TEXT NOT NULL,
    file_reference   TEXT,
    last_synced      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (semantic_part_id) REFERENCES parts(semantic_part_id)
);

CREATE TABLE IF NOT EXISTS knowledge_nodes (
    knowledge_id TEXT PRIMARY KEY,
    content      TEXT NOT NULL,
    category     TEXT NOT NULL,
    author       TEXT,
    confidence   REAL DEFAULT 1.0,
    refs         JSON,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS anchors (
    anchor_id        TEXT PRIMARY KEY,
    knowledge_id     TEXT NOT NULL,
    semantic_part_id TEXT NOT NULL,
    relation_type    TEXT DEFAULT 'applies_to',
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (knowledge_id)     REFERENCES knowledge_nodes(knowledge_id),
    FOREIGN KEY (semantic_part_id) REFERENCES parts(semantic_part_id)
);

CREATE TABLE IF NOT EXISTS part_relationships (
    relation_id   TEXT PRIMARY KEY,
    from_part_id  TEXT NOT NULL,
    to_part_id    TEXT NOT NULL,
    relation_type TEXT NOT NULL DEFAULT 'connected_to',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_part_id) REFERENCES parts(semantic_part_id),
    FOREIGN KEY (to_part_id)   REFERENCES parts(semantic_part_id)
);

CREATE INDEX IF NOT EXISTS idx_anchors_part        ON anchors(semantic_part_id);
CREATE INDEX IF NOT EXISTS idx_anchors_knowledge   ON anchors(knowledge_id);
CREATE INDEX IF NOT EXISTS idx_mappings_native     ON cad_mappings(cad_system, native_id);
CREATE INDEX IF NOT EXISTS idx_relations_from      ON part_relationships(from_part_id);
CREATE INDEX IF NOT EXISTS idx_relations_to        ON part_relationships(to_part_id);
"""


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(_SCHEMA)
