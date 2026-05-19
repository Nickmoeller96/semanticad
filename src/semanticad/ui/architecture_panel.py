"""Architecture / Platform view — three-layer diagram, live stats, tool-endpoint list."""

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from semanticad.agent.tools import get_ontology_stats

_TOOLS = [
    ("get_part_info",             "Vollständige Infos zu einem Bauteil: Name, Typ, Metadaten"),
    ("get_knowledge_for_part",    "Alle Wissensknoten eines Bauteils"),
    ("search_knowledge_semantic", "Volltext-Suche im Wissens-Pool"),
    ("find_similar_parts",        "Bauteile gleichen Typs finden"),
    ("get_related_knowledge",     "Wissensknoten gleicher Kategorie"),
    ("list_parts_by_type",        "Alle Bauteile eines Typs (Pump, Valve, Sensor …)"),
    ("get_part_relationships",    "Verbindungen zwischen Bauteilen"),
    ("get_ontology_stats",        "Live-Statistiken der gesamten Ontology"),
]

_ARCH_HTML = """\
<div style='padding:14px; font-family:sans-serif;'>

<h2 style='color:#1a1a2e; margin-bottom:4px;'>Geometrie-nativer Ontology-Layer</h2>
<p style='color:#555; font-size:12px; margin-top:0; line-height:1.5;'>
SemantiCAD ist ein semantischer Layer über CAD/PLM-Modelle.
Diese Desktop-App ist nur <b>einer</b> der möglichen Konsumenten —
der Layer ist so designed, dass externe AI-Agents über MCP,
Wartungs-Dashboards und PLM-Plugins auf dieselbe Ontology zugreifen können.
</p>

<h3 style='color:#1a1a2e; margin-bottom:6px;'>Drei-Schichten-Architektur</h3>

<table width='100%' cellspacing='0' cellpadding='0'
       style='border-collapse:collapse; font-size:12px;'>

  <!-- Konsumenten header -->
  <tr>
    <td colspan='3' style='background:#dde4ff; border:1px solid #bac4f5;
        padding:8px 12px; text-align:center;'>
      <b>Konsumenten</b>
    </td>
  </tr>
  <!-- Konsumenten boxes -->
  <tr>
    <td style='background:#eef2ff; border:1px solid #c5cef5;
        padding:10px; text-align:center; width:34%;'>
      Desktop-App<br>
      <span style='color:#3b5bdb; font-size:11px; font-weight:bold;'>← diese App</span>
    </td>
    <td style='background:#eef2ff; border:1px solid #c5cef5;
        padding:10px; text-align:center; width:33%;'>
      Claude Desktop<br>
      <span style='color:#888; font-size:11px;'>via MCP · Phase 2</span>
    </td>
    <td style='background:#eef2ff; border:1px solid #c5cef5;
        padding:10px; text-align:center; width:33%;'>
      Wartungs-Dashboards<br>
      <span style='color:#888; font-size:11px;'>PLM-Plugins · Roadmap</span>
    </td>
  </tr>

  <!-- Tool-Layer -->
  <tr>
    <td colspan='3' style='background:#d3f9d8; border:1px solid #8ce99a;
        padding:10px 12px;'>
      <b>Tool-Layer / API</b><br>
      <span style='font-size:11px; color:#555;'>
        get_part_info &nbsp;·&nbsp; get_knowledge_for_part &nbsp;·&nbsp;
        search_knowledge_semantic &nbsp;·&nbsp; find_similar_parts<br>
        get_related_knowledge &nbsp;·&nbsp; list_parts_by_type &nbsp;·&nbsp;
        get_part_relationships &nbsp;·&nbsp; get_ontology_stats
      </span>
    </td>
  </tr>

  <!-- Ontology -->
  <tr>
    <td colspan='3' style='background:#fff9db; border:1px solid #ffe066;
        padding:10px 12px;'>
      <b>Ontology / Wissens-Graph</b><br>
      <span style='font-size:11px; color:#555;'>
        Parts &nbsp;·&nbsp; Knowledge Nodes &nbsp;·&nbsp; Anchors &nbsp;·&nbsp;
        Part Relationships &nbsp;·&nbsp; CAD-Mappings (Multi-System-Ready)<br>
        Datenbank: SQLite (heute) &nbsp;·&nbsp; Neo4j, Postgres (Roadmap)
      </span>
    </td>
  </tr>

  <!-- CAD-Quellen -->
  <tr>
    <td colspan='3' style='background:#ffe3e3; border:1px solid #ffa8a8;
        padding:10px 12px;'>
      <b>CAD-Quellen</b><br>
      <span style='font-size:11px; color:#555;'>
        STEP (heute) &nbsp;·&nbsp; JT, Onshape, SolidWorks (Roadmap)
      </span>
    </td>
  </tr>
</table>

<h3 style='color:#1a1a2e; margin-top:16px; margin-bottom:6px;'>
  Tool-Endpoints (verfügbar heute)
</h3>
<table width='100%' cellspacing='0' cellpadding='0'
       style='border-collapse:collapse; font-size:11px;'>
{tool_rows}
</table>

<p style='color:#999; font-size:11px; font-style:italic; margin-top:12px;'>
  ⚠ MCP-Server: geplant für Phase 2. Heute ist der Tool-Layer intern in der Desktop-App.
</p>
</div>
"""


class ArchitecturePanel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._arch_browser = QTextBrowser()
        self._arch_browser.setOpenLinks(False)
        self._arch_browser.setStyleSheet("border:none; background:#fff;")
        layout.addWidget(self._arch_browser, stretch=3)

        # Stats bar
        stats_bar = QHBoxLayout()
        stats_bar.setContentsMargins(8, 4, 8, 4)
        stats_lbl = QLabel("Live-Statistiken der Ontology")
        stats_lbl.setStyleSheet("font-weight:bold; font-size:12px;")
        stats_bar.addWidget(stats_lbl)
        stats_bar.addStretch()
        refresh_btn = QPushButton("⟳ Aktualisieren")
        refresh_btn.setStyleSheet(
            "QPushButton { font-size:11px; color:#555; background:#f0f0f0; "
            "border:1px solid #ccc; border-radius:3px; padding:2px 8px; }"
            "QPushButton:hover { background:#e0e0e0; }"
        )
        refresh_btn.clicked.connect(self.refresh)
        stats_bar.addWidget(refresh_btn)
        layout.addLayout(stats_bar)

        self._stats_browser = QTextBrowser()
        self._stats_browser.setMaximumHeight(70)
        self._stats_browser.setStyleSheet(
            "font-size:12px; background:#fafafa; border:none; "
            "border-top:1px solid #eee;"
        )
        layout.addWidget(self._stats_browser)

        self._render_arch()
        self.refresh()

    def _render_arch(self) -> None:
        rows = []
        for i, (name, desc) in enumerate(_TOOLS):
            bg = "#f8f9fa" if i % 2 == 0 else "#ffffff"
            rows.append(
                f"<tr style='background:{bg};'>"
                f"<td style='padding:4px 10px; font-family:monospace; "
                f"color:#3b5bdb; white-space:nowrap;'>{name}</td>"
                f"<td style='padding:4px 10px; color:#555;'>{desc}</td>"
                f"</tr>"
            )
        self._arch_browser.setHtml(_ARCH_HTML.replace("{tool_rows}", "\n".join(rows)))

    def refresh(self) -> None:
        try:
            s = get_ontology_stats()
            cats = s.get("categories", {})
            cat_str = (
                " &nbsp;·&nbsp; ".join(f"{k}: <b>{v}</b>" for k, v in cats.items())
                if cats else "—"
            )
            html = (
                f"<div style='padding:8px 10px; font-size:12px;'>"
                f"<b>{s['parts']}</b> Bauteile &nbsp;·&nbsp; "
                f"<b>{s['knowledge_nodes']}</b> Wissensknoten &nbsp;·&nbsp; "
                f"<b>{s['anchors']}</b> Anker &nbsp;·&nbsp; "
                f"<b>{s['relationships']}</b> Verbindungen"
                f"<br><span style='color:#888; font-size:11px;'>"
                f"Kategorien: {cat_str}</span></div>"
            )
        except Exception as exc:
            html = f"<i style='color:#cc0000; padding:8px;'>Fehler: {exc}</i>"
        self._stats_browser.setHtml(html)
