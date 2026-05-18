"""The 6 stable tool functions exposed to the Anthropic agent."""

from semanticad.data.database import get_connection


def get_part_info(semantic_part_id: str) -> dict:
    """Full info for one part: name, type, description, metadata."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM parts WHERE semantic_part_id = ?",
            (semantic_part_id,),
        ).fetchone()
    if not row:
        return {"error": f"Part '{semantic_part_id}' not found"}
    return dict(row)


def get_knowledge_for_part(semantic_part_id: str) -> list[dict]:
    """All knowledge nodes anchored to a part."""
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


def search_knowledge_semantic(query: str, limit: int = 5) -> list[dict]:
    """Full-text LIKE search across knowledge node content and category."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT kn.knowledge_id, kn.content, kn.category, kn.author, "
            "kn.confidence, kn.created_at, p.canonical_name AS part_name "
            "FROM knowledge_nodes kn "
            "LEFT JOIN anchors a ON kn.knowledge_id = a.knowledge_id "
            "LEFT JOIN parts p   ON a.semantic_part_id = p.semantic_part_id "
            "WHERE kn.content LIKE ? OR kn.category LIKE ? OR p.canonical_name LIKE ? "
            "GROUP BY kn.knowledge_id "
            "ORDER BY kn.created_at DESC "
            "LIMIT ?",
            (f"%{query}%", f"%{query}%", f"%{query}%", limit),
        ).fetchall()
    return [dict(r) for r in rows]


def find_similar_parts(semantic_part_id: str, limit: int = 5) -> list[dict]:
    """Parts with the same part_type as the given part."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT part_type FROM parts WHERE semantic_part_id = ?",
            (semantic_part_id,),
        ).fetchone()
        if not row:
            return []
        rows = conn.execute(
            "SELECT * FROM parts "
            "WHERE part_type = ? AND semantic_part_id != ? "
            "ORDER BY canonical_name LIMIT ?",
            (row["part_type"], semantic_part_id, limit),
        ).fetchall()
    return [dict(r) for r in rows]


def get_related_knowledge(knowledge_id: str, limit: int = 5) -> list[dict]:
    """Knowledge nodes in the same category as the given node."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT category FROM knowledge_nodes WHERE knowledge_id = ?",
            (knowledge_id,),
        ).fetchone()
        if not row:
            return []
        rows = conn.execute(
            "SELECT kn.*, p.canonical_name AS part_name "
            "FROM knowledge_nodes kn "
            "LEFT JOIN anchors a ON kn.knowledge_id = a.knowledge_id "
            "LEFT JOIN parts p   ON a.semantic_part_id = p.semantic_part_id "
            "WHERE kn.category = ? AND kn.knowledge_id != ? "
            "GROUP BY kn.knowledge_id "
            "ORDER BY kn.created_at DESC LIMIT ?",
            (row["category"], knowledge_id, limit),
        ).fetchall()
    return [dict(r) for r in rows]


def list_parts_by_type(part_type: str) -> list[dict]:
    """All parts of a given type (e.g. 'Pump', 'Valve', 'Sensor')."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM parts WHERE part_type LIKE ? ORDER BY canonical_name",
            (f"%{part_type}%",),
        ).fetchall()
    return [dict(r) for r in rows]
