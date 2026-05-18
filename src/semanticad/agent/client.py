"""Anthropic agent client with tool-calling loop."""

import json
from typing import Callable

import anthropic

from semanticad.agent import tools as _tools
from semanticad.agent.tool_definitions import TOOL_DEFINITIONS

_MODEL = "claude-sonnet-4-6"

_SYSTEM_TEMPLATE = """\
Du bist ein Engineering-Assistent für eine Industrieanlage. Du hast Zugriff auf einen \
semantischen Wissens-Graphen (SemantiCAD), der Ingenieurswissen mit konkreten Bauteilen \
in CAD-Modellen verknüpft.

Nutze die verfügbaren Tools, um:
- Wissensknoten zu Bauteilen zu finden
- Ähnliche Bauteile zu identifizieren
- Verwandtes Wissen über Kategoriegrenzen hinweg zu finden
- Semantische Suche im Wissens-Pool durchzuführen

Antworte präzise, technisch korrekt, und zitiere konkrete Wissensknoten mit ihrer Kategorie \
und Quelle (Autor). Wenn du Wissen aus mehreren Knoten kombinierst, mache das transparent. \
Wenn keine relevanten Daten existieren, sage das ehrlich statt zu raten. \
Antworte auf Deutsch, es sei denn der Nutzer schreibt auf Englisch.

{part_list}
"""

_DISPATCH: dict[str, Callable] = {
    "get_part_info":           lambda i: _tools.get_part_info(i["semantic_part_id"]),
    "get_knowledge_for_part":  lambda i: _tools.get_knowledge_for_part(i["semantic_part_id"]),
    "search_knowledge_semantic": lambda i: _tools.search_knowledge_semantic(
        i["query"], i.get("limit", 5)
    ),
    "find_similar_parts":      lambda i: _tools.find_similar_parts(
        i["semantic_part_id"], i.get("limit", 5)
    ),
    "get_related_knowledge":   lambda i: _tools.get_related_knowledge(
        i["knowledge_id"], i.get("limit", 5)
    ),
    "list_parts_by_type":      lambda i: _tools.list_parts_by_type(i["part_type"]),
}


class SemanticAgentClient:
    def __init__(self) -> None:
        self._client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
        self._part_map: dict[str, str] = {}   # {canonical_name: semantic_part_id}

    def set_part_map(self, part_map: dict[str, str]) -> None:
        self._part_map = part_map

    def _system_prompt(self) -> str:
        if self._part_map:
            lines = ["Verfügbare Bauteile in der aktuellen Anlage (Name → UUID):"]
            for name, pid in sorted(self._part_map.items()):
                lines.append(f'  - "{name}" → {pid}')
            part_list = "\n".join(lines)
        else:
            part_list = "Noch keine STEP-Datei geladen."
        return _SYSTEM_TEMPLATE.format(part_list=part_list)

    def send(
        self,
        conversation: list[dict],
        on_tool_call: Callable[[str], None] | None = None,
    ) -> str:
        """
        Run one agentic turn. Handles the full tool-calling loop.
        Returns the final assistant text.
        `on_tool_call(tool_name)` is called (from the worker thread) for each tool use.
        """
        messages = list(conversation)

        while True:
            response = self._client.messages.create(
                model=_MODEL,
                max_tokens=4096,
                system=self._system_prompt(),
                tools=TOOL_DEFINITIONS,
                messages=messages,
            )

            if response.stop_reason == "end_turn":
                return "".join(
                    block.text
                    for block in response.content
                    if hasattr(block, "text")
                )

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        if on_tool_call:
                            on_tool_call(block.name)
                        handler = _DISPATCH.get(block.name)
                        result = handler(block.input) if handler else {"error": f"Unknown tool: {block.name}"}
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result, ensure_ascii=False, indent=2),
                        })
                messages.append({"role": "user", "content": tool_results})
            else:
                # Unexpected stop reason — return whatever text is available
                return "".join(
                    block.text
                    for block in response.content
                    if hasattr(block, "text")
                )
