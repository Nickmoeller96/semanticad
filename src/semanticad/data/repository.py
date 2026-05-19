"""CRUD operations for the SemantiCAD knowledge graph."""

import uuid
from typing import Optional

from semanticad.data.database import get_connection


def _infer_part_type(name: str) -> str:
    lower = name.lower()
    if "pump" in lower:    return "Pump"
    if "motor" in lower:   return "Motor"
    if "valve" in lower:   return "Valve"
    if any(k in lower for k in ("pipe", "flange")): return "Pipe"
    if any(k in lower for k in ("sensor", "gauge")): return "Sensor"
    if any(k in lower for k in ("fan", "cooling")): return "Fan"
    if any(k in lower for k in ("shaft", "coupling", "bearing", "seal")): return "Shaft"
    if any(k in lower for k in ("base", "plate")): return "Structure"
    return "Component"


def import_parts_from_step(filepath: str, part_names: list[str]) -> dict[str, str]:
    """Upsert parts from a STEP file. Returns {canonical_name: semantic_part_id}."""
    result: dict[str, str] = {}
    fp = str(filepath)
    with get_connection() as conn:
        for name in part_names:
            row = conn.execute(
                "SELECT semantic_part_id FROM cad_mappings "
                "WHERE cad_system = 'STEP' AND native_id = ? AND file_reference = ?",
                (name, fp),
            ).fetchone()
            if row:
                result[name] = row["semantic_part_id"]
            else:
                pid = str(uuid.uuid4())
                conn.execute(
                    "INSERT INTO parts (semantic_part_id, canonical_name, part_type) "
                    "VALUES (?, ?, ?)",
                    (pid, name, _infer_part_type(name)),
                )
                conn.execute(
                    "INSERT INTO cad_mappings "
                    "(mapping_id, semantic_part_id, cad_system, native_id, file_reference) "
                    "VALUES (?, ?, 'STEP', ?, ?)",
                    (str(uuid.uuid4()), pid, name, fp),
                )
                result[name] = pid
    return result


def get_part_id(name: str, filepath: str) -> Optional[str]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT semantic_part_id FROM cad_mappings "
            "WHERE cad_system = 'STEP' AND native_id = ? AND file_reference = ?",
            (name, str(filepath)),
        ).fetchone()
        return row["semantic_part_id"] if row else None


def get_anchored_part_names(filepath: str) -> set[str]:
    """Return canonical_names of parts that have at least one anchor."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT p.canonical_name "
            "FROM parts p "
            "JOIN cad_mappings m ON p.semantic_part_id = m.semantic_part_id "
            "JOIN anchors a     ON p.semantic_part_id = a.semantic_part_id "
            "WHERE m.cad_system = 'STEP' AND m.file_reference = ?",
            (str(filepath),),
        ).fetchall()
        return {r["canonical_name"] for r in rows}


def get_knowledge_for_part(semantic_part_id: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT kn.knowledge_id, kn.content, kn.category, kn.author, "
            "kn.confidence, a.relation_type, kn.created_at "
            "FROM knowledge_nodes kn "
            "JOIN anchors a ON kn.knowledge_id = a.knowledge_id "
            "WHERE a.semantic_part_id = ? "
            "ORDER BY kn.created_at DESC",
            (semantic_part_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def add_knowledge_node(
    semantic_part_id: str,
    content: str,
    category: str,
    author: str,
    confidence: float,
    relation_type: str = "applies_to",
) -> str:
    """Create a knowledge node and anchor it to a part. Returns knowledge_id."""
    kid = str(uuid.uuid4())
    aid = str(uuid.uuid4())
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO knowledge_nodes (knowledge_id, content, category, author, confidence) "
            "VALUES (?, ?, ?, ?, ?)",
            (kid, content, category, author, confidence),
        )
        conn.execute(
            "INSERT INTO anchors (anchor_id, knowledge_id, semantic_part_id, relation_type) "
            "VALUES (?, ?, ?, ?)",
            (aid, kid, semantic_part_id, relation_type),
        )
    return kid


def delete_knowledge_node(knowledge_id: str) -> None:
    """Delete a knowledge node and all its anchors."""
    with get_connection() as conn:
        conn.execute("DELETE FROM anchors WHERE knowledge_id = ?", (knowledge_id,))
        conn.execute("DELETE FROM knowledge_nodes WHERE knowledge_id = ?", (knowledge_id,))


def delete_relationship(relation_id: str) -> None:
    """Delete a part relationship."""
    with get_connection() as conn:
        conn.execute("DELETE FROM part_relationships WHERE relation_id = ?", (relation_id,))


def add_relationship(from_part_id: str, to_part_id: str, relation_type: str) -> str:
    """Create a directional relationship between two parts. Returns relation_id."""
    rid = str(uuid.uuid4())
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO part_relationships (relation_id, from_part_id, to_part_id, relation_type) "
            "VALUES (?, ?, ?, ?)",
            (rid, from_part_id, to_part_id, relation_type),
        )
    return rid


def get_relationships_for_part(semantic_part_id: str) -> list[dict]:
    """All relationships where this part is from or to. Returns both directions."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT r.relation_id, r.relation_type, r.created_at, "
            "p_from.canonical_name AS from_name, p_from.semantic_part_id AS from_id, "
            "p_to.canonical_name   AS to_name,   p_to.semantic_part_id   AS to_id "
            "FROM part_relationships r "
            "JOIN parts p_from ON r.from_part_id = p_from.semantic_part_id "
            "JOIN parts p_to   ON r.to_part_id   = p_to.semantic_part_id "
            "WHERE r.from_part_id = ? OR r.to_part_id = ? "
            "ORDER BY r.created_at DESC",
            (semantic_part_id, semantic_part_id),
        ).fetchall()
    return [dict(r) for r in rows]


def get_connected_part_names(semantic_part_id: str) -> set[str]:
    """Canonical names of all parts directly connected to the given part."""
    rels = get_relationships_for_part(semantic_part_id)
    names = set()
    for r in rels:
        if r["from_id"] == semantic_part_id:
            names.add(r["to_name"])
        else:
            names.add(r["from_name"])
    return names


def get_all_anchors(filepath: str) -> list[dict]:
    """All anchors for the current STEP file with part name + knowledge summary."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT p.canonical_name, kn.category, kn.content, kn.author, "
            "a.anchor_id, a.relation_type "
            "FROM anchors a "
            "JOIN parts p           ON a.semantic_part_id = p.semantic_part_id "
            "JOIN knowledge_nodes kn ON a.knowledge_id = kn.knowledge_id "
            "JOIN cad_mappings m    ON p.semantic_part_id = m.semantic_part_id "
            "WHERE m.cad_system = 'STEP' AND m.file_reference = ? "
            "ORDER BY p.canonical_name, kn.created_at DESC",
            (str(filepath),),
        ).fetchall()
        return [dict(r) for r in rows]
