"""Anthropic tool-use JSON schemas for the 6 SemantiCAD agent tools."""

TOOL_DEFINITIONS = [
    {
        "name": "get_part_info",
        "description": (
            "Vollständige Informationen zu einem Bauteil: Name, Typ, Beschreibung, Metadaten. "
            "Nutze dies als ersten Schritt, wenn der Nutzer nach einem bestimmten Bauteil fragt."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "semantic_part_id": {
                    "type": "string",
                    "description": "UUID des Bauteils (aus der Bauteilliste im System-Prompt)",
                }
            },
            "required": ["semantic_part_id"],
        },
    },
    {
        "name": "get_knowledge_for_part",
        "description": (
            "Alle Wissensknoten, die mit diesem Bauteil verankert sind: "
            "Schadensfälle, Wartungshinweise, Designentscheidungen, Betriebserfahrungen."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "semantic_part_id": {
                    "type": "string",
                    "description": "UUID des Bauteils",
                }
            },
            "required": ["semantic_part_id"],
        },
    },
    {
        "name": "search_knowledge_semantic",
        "description": (
            "Durchsucht alle Wissensknoten nach einem Begriff oder Konzept (z.B. 'Kavitation', "
            "'Dichtung', 'Schadensfall'). Gibt Knoten zurück, deren Inhalt oder Kategorie passt."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Suchbegriff oder kurze Beschreibung des gesuchten Wissens",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximale Anzahl Ergebnisse (Standard: 5)",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "find_similar_parts",
        "description": (
            "Findet Bauteile mit dem gleichen Typ wie das angegebene Bauteil. "
            "Nützlich bei Fragen wie 'Gibt es andere Pumpen/Ventile in der Anlage?'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "semantic_part_id": {
                    "type": "string",
                    "description": "UUID des Referenzbauteils",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximale Anzahl Ergebnisse (Standard: 5)",
                },
            },
            "required": ["semantic_part_id"],
        },
    },
    {
        "name": "get_related_knowledge",
        "description": (
            "Wissensknoten der gleichen Kategorie wie ein bekannter Knoten. "
            "Nützlich um weitere Schadensfälle, Wartungshinweise o.ä. zu finden."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "knowledge_id": {
                    "type": "string",
                    "description": "UUID eines bekannten Wissensknotens",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximale Anzahl Ergebnisse (Standard: 5)",
                },
            },
            "required": ["knowledge_id"],
        },
    },
    {
        "name": "get_part_relationships",
        "description": (
            "Alle Verbindungen eines Bauteils zu anderen Bauteilen: "
            "drives, contains, seals, connected_to, monitors. "
            "Nützlich um Abhängigkeitsketten zu analysieren, z.B. 'Was ist mit der Welle verbunden?'"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "semantic_part_id": {
                    "type": "string",
                    "description": "UUID des Bauteils",
                }
            },
            "required": ["semantic_part_id"],
        },
    },
    {
        "name": "list_parts_by_type",
        "description": (
            "Alle Bauteile eines bestimmten Typs in der Anlage. "
            "Gültige Typen: 'Pump', 'Motor', 'Valve', 'Pipe', 'Sensor', 'Fan', 'Shaft', "
            "'Structure', 'Component'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "part_type": {
                    "type": "string",
                    "description": "Bauteiltyp, z.B. 'Pump', 'Valve', 'Sensor'",
                }
            },
            "required": ["part_type"],
        },
    },
]
