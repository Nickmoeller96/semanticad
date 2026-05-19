"""Main application window — 3-panel layout: side | viewer | info."""

import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QColor
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSplitter,
    QStatusBar,
    QTextBrowser,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from semanticad.viewer.occ_widget import OCCViewerWidget
from semanticad.viewer.step_loader import PartEntry
from semanticad.data.database import init_db
from semanticad.data import repository as repo
from semanticad.ui.knowledge_dialog import KnowledgeDialog
from semanticad.ui.chat_panel import ChatPanel

_CATEGORY_ICONS = {
    "Failure Mode":        "🔴",
    "Maintenance":         "🔧",
    "Design Rationale":    "📐",
    "Material Experience": "⚗️",
    "Operating Experience":"📋",
    "Safety Note":         "⚠️",
}


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SemantiCAD")
        self.resize(1500, 920)

        # State
        self._current_filepath: str | None = None
        self._part_map: dict[str, str] = {}   # {canonical_name: semantic_part_id}
        self._selected_part: str | None = None
        self._multi_selected: list[str] = []  # up to 2 parts for relationship creation

        init_db()
        self._build_ui()
        self._build_menu()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # ---- Left panel: part tree + anchor list ----
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(4, 4, 4, 4)
        left_layout.setSpacing(4)

        parts_label = QLabel("Parts")
        parts_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        left_layout.addWidget(parts_label)

        self._part_tree = QTreeWidget()
        self._part_tree.setHeaderHidden(True)
        self._part_tree.setStyleSheet("font-size: 12px;")
        self._part_tree.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self._part_tree.itemClicked.connect(self._on_tree_item_clicked)
        left_layout.addWidget(self._part_tree, stretch=3)

        self._connect_btn = QPushButton("🔗 Verbinden")
        self._connect_btn.setEnabled(False)
        self._connect_btn.setToolTip("⌘+Klick auf 2 Bauteile, dann verbinden")
        self._connect_btn.setStyleSheet(
            "QPushButton { background: #e67700; color: white; border-radius: 4px; "
            "padding: 4px 8px; font-size: 11px; }"
            "QPushButton:disabled { background: #ccc; color: #888; }"
            "QPushButton:hover { background: #cc6600; }"
        )
        self._connect_btn.clicked.connect(self._on_connect_parts)
        left_layout.addWidget(self._connect_btn)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #ccc;")
        left_layout.addWidget(sep)

        anchors_label = QLabel("Knowledge Anchors")
        anchors_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #555;")
        left_layout.addWidget(anchors_label)

        self._anchor_list = QListWidget()
        self._anchor_list.setStyleSheet("font-size: 11px;")
        self._anchor_list.setMaximumHeight(200)
        self._anchor_list.itemClicked.connect(self._on_anchor_clicked)
        self._anchor_list.setWordWrap(True)
        left_layout.addWidget(self._anchor_list, stretch=2)

        sep4 = QFrame()
        sep4.setFrameShape(QFrame.Shape.HLine)
        sep4.setStyleSheet("color: #ccc;")
        left_layout.addWidget(sep4)

        conn_label = QLabel("Verbindung erstellen")
        conn_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #555;")
        left_layout.addWidget(conn_label)

        from_row = QHBoxLayout()
        from_row.addWidget(QLabel("Von:"))
        self._from_combo = QComboBox()
        self._from_combo.setStyleSheet("font-size: 11px;")
        self._from_combo.setEnabled(False)
        from_row.addWidget(self._from_combo, stretch=1)
        left_layout.addLayout(from_row)

        to_row = QHBoxLayout()
        to_row.addWidget(QLabel("Zu:  "))
        self._to_combo = QComboBox()
        self._to_combo.setStyleSheet("font-size: 11px;")
        self._to_combo.setEnabled(False)
        to_row.addWidget(self._to_combo, stretch=1)
        left_layout.addLayout(to_row)

        type_row = QHBoxLayout()
        type_row.addWidget(QLabel("Typ:"))
        self._rel_type_combo = QComboBox()
        self._rel_type_combo.addItems(["drives", "contains", "connected_to", "seals", "monitors"])
        self._rel_type_combo.setStyleSheet("font-size: 11px;")
        self._rel_type_combo.setEnabled(False)
        type_row.addWidget(self._rel_type_combo, stretch=1)
        left_layout.addLayout(type_row)

        self._connect_btn2 = QPushButton("🔗 Verbinden")
        self._connect_btn2.setEnabled(False)
        self._connect_btn2.setStyleSheet(
            "QPushButton { background: #e67700; color: white; border-radius: 4px; "
            "padding: 4px 8px; font-size: 11px; }"
            "QPushButton:disabled { background: #ccc; color: #888; }"
            "QPushButton:hover { background: #cc6600; }"
        )
        self._connect_btn2.clicked.connect(self._on_connect_from_panel)
        left_layout.addWidget(self._connect_btn2)

        left.setMinimumWidth(230)

        # ---- Center: 3D viewer ----
        viewer_container = QWidget()
        viewer_v = QVBoxLayout(viewer_container)
        viewer_v.setContentsMargins(0, 0, 0, 0)
        viewer_v.setSpacing(2)

        self._reset_view_btn = QPushButton("⟳ Ansicht zurücksetzen")
        self._reset_view_btn.setStyleSheet(
            "QPushButton { font-size: 11px; color: #555; background: #f0f0f0; "
            "border: 1px solid #ccc; border-radius: 3px; padding: 2px 8px; }"
            "QPushButton:hover { background: #e0e0e0; }"
        )
        self._reset_view_btn.clicked.connect(self._reset_view)
        viewer_v.addWidget(self._reset_view_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self._viewer = OCCViewerWidget()
        self._viewer.part_selected.connect(self._on_part_selected)
        viewer_v.addWidget(self._viewer, stretch=1)

        # ---- Right panel: part info + knowledge ----
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(6, 6, 6, 6)
        right_layout.setSpacing(6)

        info_header = QLabel("Part Info")
        info_header.setStyleSheet("font-weight: bold; font-size: 13px;")
        right_layout.addWidget(info_header)

        self._part_name_label = QLabel("—")
        self._part_name_label.setStyleSheet(
            "font-size: 12px; font-weight: bold; color: #1a1a2e; "
            "padding: 4px; background: #eef2ff; border-radius: 4px;"
        )
        self._part_name_label.setWordWrap(True)
        right_layout.addWidget(self._part_name_label)

        self._add_knowledge_btn = QPushButton("+ Add Knowledge")
        self._add_knowledge_btn.setEnabled(False)
        self._add_knowledge_btn.setStyleSheet(
            "QPushButton { background: #3b5bdb; color: white; border-radius: 4px; "
            "padding: 5px 10px; font-size: 12px; }"
            "QPushButton:disabled { background: #aaa; }"
            "QPushButton:hover { background: #2f4ac0; }"
        )
        self._add_knowledge_btn.clicked.connect(self._on_add_knowledge)
        right_layout.addWidget(self._add_knowledge_btn)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #ccc;")
        right_layout.addWidget(sep2)

        knowledge_header = QLabel("Knowledge Nodes")
        knowledge_header.setStyleSheet("font-weight: bold; font-size: 12px; color: #555;")
        right_layout.addWidget(knowledge_header)

        self._knowledge_browser = QTextBrowser()
        self._knowledge_browser.setStyleSheet(
            "font-size: 12px; background: #fafafa; border: 1px solid #ddd; border-radius: 4px;"
        )
        self._knowledge_browser.setOpenLinks(False)
        self._knowledge_browser.setPlaceholderText("Click a part to see its knowledge nodes.")
        self._knowledge_browser.anchorClicked.connect(self._on_knowledge_link)
        right_layout.addWidget(self._knowledge_browser, stretch=1)

        sep3 = QFrame()
        sep3.setFrameShape(QFrame.Shape.HLine)
        sep3.setStyleSheet("color: #ccc;")
        right_layout.addWidget(sep3)

        rel_header = QLabel("Verbundene Bauteile")
        rel_header.setStyleSheet("font-weight: bold; font-size: 12px; color: #555;")
        right_layout.addWidget(rel_header)

        self._relations_browser = QTextBrowser()
        self._relations_browser.setStyleSheet(
            "font-size: 11px; background: #fafafa; border: 1px solid #ddd; border-radius: 4px;"
        )
        self._relations_browser.setMaximumHeight(120)
        self._relations_browser.setPlaceholderText("Keine Verbindungen.")
        self._relations_browser.setOpenLinks(False)
        self._relations_browser.anchorClicked.connect(self._on_relation_link)
        right_layout.addWidget(self._relations_browser)

        right.setMinimumWidth(260)

        splitter.addWidget(left)
        splitter.addWidget(viewer_container)
        splitter.addWidget(right)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)
        splitter.setStretchFactor(2, 2)

        # Chat panel sits below the 3-panel row
        self._chat_panel = ChatPanel()

        v_splitter = QSplitter(Qt.Orientation.Vertical)
        v_splitter.addWidget(splitter)
        v_splitter.addWidget(self._chat_panel)
        v_splitter.setStretchFactor(0, 3)
        v_splitter.setStretchFactor(1, 1)
        v_splitter.setSizes([620, 280])

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(v_splitter)

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Open a STEP file via File → Open STEP…")

    def _build_menu(self) -> None:
        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        open_action = QAction("Open STEP…", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_step_dialog)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

    # ------------------------------------------------------------------
    # File loading
    # ------------------------------------------------------------------

    def _open_step_dialog(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open STEP file",
            str(os.path.expanduser("~")),
            "STEP files (*.step *.stp *.STEP *.STP)",
        )
        if path:
            self._load_step(path)

    def _load_step(self, filepath: str) -> None:
        self.statusBar().showMessage(f"Loading {os.path.basename(filepath)}…")
        try:
            parts = self._viewer.load_step_file(filepath)
            self._current_filepath = filepath
            self._part_map = repo.import_parts_from_step(filepath, [p.name for p in parts])
            self._chat_panel.set_part_map(self._part_map)
            self._populate_tree(parts)
            self._refresh_anchored_parts()
            self._refresh_anchor_list()
            self._refresh_part_combos()
            self.setWindowTitle(f"SemantiCAD — {os.path.basename(filepath)}")
            self.statusBar().showMessage(
                f"Loaded {len(parts)} components from {os.path.basename(filepath)}"
            )
        except Exception as exc:
            self.statusBar().showMessage(f"Error: {exc}")
            raise

    # ------------------------------------------------------------------
    # Tree population
    # ------------------------------------------------------------------

    def _populate_tree(self, parts: list[PartEntry]) -> None:
        self._part_tree.clear()
        root = QTreeWidgetItem(self._part_tree, ["Model"])
        root.setExpanded(True)
        for entry in parts:
            item = QTreeWidgetItem(root, [entry.name])
            item.setData(0, Qt.ItemDataRole.UserRole, entry.name)
        self._part_tree.addTopLevelItem(root)

    def _update_tree_anchors(self, anchored_names: set[str]) -> None:
        root = self._part_tree.topLevelItem(0)
        if root is None:
            return
        for i in range(root.childCount()):
            child = root.child(i)
            name = child.data(0, Qt.ItemDataRole.UserRole)
            if name in anchored_names:
                child.setText(0, f"★ {name}")
                child.setForeground(0, QColor("#b8860b"))
            else:
                child.setText(0, name)
                child.setForeground(0, QColor("#000000"))

    # ------------------------------------------------------------------
    # Anchors
    # ------------------------------------------------------------------

    def _refresh_anchored_parts(self) -> None:
        if not self._current_filepath:
            return
        anchored = repo.get_anchored_part_names(self._current_filepath)
        self._viewer.highlight_anchored(anchored)
        self._update_tree_anchors(anchored)

    def _refresh_anchor_list(self) -> None:
        self._anchor_list.clear()
        if not self._current_filepath:
            return
        anchors = repo.get_all_anchors(self._current_filepath)
        for a in anchors:
            icon = _CATEGORY_ICONS.get(a["category"], "•")
            text = f"{icon} {a['canonical_name']}\n  {a['category']} — {a['content'][:60]}…"
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, a["canonical_name"])
            item.setToolTip(a["content"])
            self._anchor_list.addItem(item)

    # ------------------------------------------------------------------
    # Selection handlers
    # ------------------------------------------------------------------

    def _on_part_selected(self, name: str) -> None:
        self._show_part_info(name)
        self._select_tree_item(name)

    def _on_tree_item_clicked(self, item: QTreeWidgetItem, _col: int) -> None:
        name = item.data(0, Qt.ItemDataRole.UserRole)
        if not name:
            return
        selected_items = self._part_tree.selectedItems()
        selected_names = [
            i.data(0, Qt.ItemDataRole.UserRole)
            for i in selected_items
            if i.data(0, Qt.ItemDataRole.UserRole)
        ]
        self._multi_selected = selected_names
        self._connect_btn.setEnabled(len(selected_names) == 2 and bool(self._current_filepath))
        if len(selected_names) == 1:
            self._show_part_info(name)
        elif len(selected_names) == 2:
            self.statusBar().showMessage(
                f"2 Bauteile gewählt: {selected_names[0]} + {selected_names[1]} → 'Verbinden' klicken"
            )

    def _on_anchor_clicked(self, item: QListWidgetItem) -> None:
        name = item.data(Qt.ItemDataRole.UserRole)
        if name:
            self._on_part_selected(name)

    def _show_part_info(self, name: str) -> None:
        self._selected_part = name
        self._part_name_label.setText(name)
        self._add_knowledge_btn.setEnabled(bool(self._current_filepath))
        self.statusBar().showMessage(f"Selected: {name}")
        self._viewer.select_part(name)
        self._chat_panel.set_current_part(name)
        self._refresh_knowledge_panel(name)
        self._refresh_relations_panel(name)
        # Auto-fill "Von" in the connection panel
        idx = self._from_combo.findText(name)
        if idx >= 0:
            self._from_combo.setCurrentIndex(idx)
        self._update_connect_btn2()

    def _refresh_knowledge_panel(self, name: str) -> None:
        pid = self._part_map.get(name)
        if not pid:
            self._knowledge_browser.setHtml(
                "<i style='color:#888'>No knowledge nodes yet.</i>"
            )
            return

        nodes = repo.get_knowledge_for_part(pid)
        if not nodes:
            self._knowledge_browser.setHtml(
                "<i style='color:#888'>No knowledge nodes yet.<br>"
                "Click <b>+ Add Knowledge</b> to add one.</i>"
            )
            return

        html_parts = []
        for n in nodes:
            icon = _CATEGORY_ICONS.get(n["category"], "•")
            conf_pct = int(n["confidence"] * 100)
            author = n["author"] or "Anonymous"
            kid = n["knowledge_id"]
            html_parts.append(
                f"<div style='margin-bottom:10px; padding:8px; background:#fff; "
                f"border-left:3px solid #3b5bdb; border-radius:3px;'>"
                f"<table width='100%' cellspacing='0' cellpadding='0'><tr>"
                f"<td><b>{icon} {n['category']}</b>"
                f"<span style='color:#888; font-size:10px'> · {author} · {conf_pct}% confidence</span></td>"
                f"<td align='right'><a href='delete-knowledge://{kid}' "
                f"style='color:#cc0000; font-size:11px; text-decoration:none;'>✕</a></td>"
                f"</tr></table>"
                f"<span style='margin-top:4px; display:block'>{n['content']}</span>"
                f"</div>"
            )

        self._knowledge_browser.setHtml("".join(html_parts))

    def _select_tree_item(self, name: str) -> None:
        root = self._part_tree.topLevelItem(0)
        if root is None:
            return
        for i in range(root.childCount()):
            child = root.child(i)
            if child.data(0, Qt.ItemDataRole.UserRole) == name:
                self._part_tree.setCurrentItem(child)
                break

    def _reset_view(self) -> None:
        if self._viewer._inited:
            self._viewer._display.FitAll()
            self._viewer._display.Repaint()
            self._viewer.update()

    def _refresh_part_combos(self) -> None:
        names = sorted(self._part_map.keys())
        for combo in (self._from_combo, self._to_combo):
            combo.clear()
            combo.addItem("— wählen —")
            combo.addItems(names)
            combo.setEnabled(bool(names))
        self._rel_type_combo.setEnabled(bool(names))
        self._from_combo.currentIndexChanged.connect(self._update_connect_btn2)
        self._to_combo.currentIndexChanged.connect(self._update_connect_btn2)

    def _update_connect_btn2(self) -> None:
        from_ok = self._from_combo.currentIndex() > 0
        to_ok   = self._to_combo.currentIndex() > 0
        different = self._from_combo.currentText() != self._to_combo.currentText()
        self._connect_btn2.setEnabled(from_ok and to_ok and different)

    def _on_connect_from_panel(self) -> None:
        name_a = self._from_combo.currentText()
        name_b = self._to_combo.currentText()
        rel_type = self._rel_type_combo.currentText()
        pid_a = self._part_map.get(name_a)
        pid_b = self._part_map.get(name_b)
        if not pid_a or not pid_b:
            return
        repo.add_relationship(pid_a, pid_b, rel_type)
        if self._selected_part:
            self._refresh_relations_panel(self._selected_part)
        self.statusBar().showMessage(f"Verbindung erstellt: {name_a} {rel_type} {name_b}")

    def _refresh_relations_panel(self, name: str) -> None:
        pid = self._part_map.get(name)
        if not pid:
            self._relations_browser.setHtml("<i style='color:#888'>Keine Verbindungen.</i>")
            self._viewer.highlight_connected(set())
            return

        rels = repo.get_relationships_for_part(pid)
        if not rels:
            self._relations_browser.setHtml("<i style='color:#888'>Keine Verbindungen.</i>")
            self._viewer.highlight_connected(set())
            return

        _REL_ICONS = {
            "drives": "⚙", "contains": "📦", "seals": "🔒",
            "connected_to": "🔗", "monitors": "📡",
        }
        connected_names = set()
        html_parts = []
        for r in rels:
            icon = _REL_ICONS.get(r["relation_type"], "↔")
            rid = r["relation_id"]
            if r["from_id"] == pid:
                other = r["to_name"]
                direction = f"{icon} {r['relation_type']} → <b>{other}</b>"
            else:
                other = r["from_name"]
                direction = f"{icon} ← {r['relation_type']} <b>{other}</b>"
            connected_names.add(other)
            html_parts.append(
                f"<div style='padding:3px 6px; margin:2px 0; background:#fff3e0; "
                f"border-left:3px solid #e67700; border-radius:3px; font-size:11px;'>"
                f"<table width='100%' cellspacing='0' cellpadding='0'><tr>"
                f"<td>{direction}</td>"
                f"<td align='right'><a href='delete-relation://{rid}' "
                f"style='color:#cc0000; font-size:11px; text-decoration:none;'>✕</a></td>"
                f"</tr></table></div>"
            )

        self._relations_browser.setHtml("".join(html_parts))
        self._viewer.highlight_connected(connected_names)

    # ------------------------------------------------------------------
    # Delete handlers
    # ------------------------------------------------------------------

    def _on_knowledge_link(self, url) -> None:
        scheme = url.scheme()
        if scheme != "delete-knowledge":
            return
        kid = url.host()
        from PyQt6.QtWidgets import QMessageBox
        if QMessageBox.question(
            self, "Löschen?", "Wissensknoten wirklich löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        ) != QMessageBox.StandardButton.Yes:
            return
        repo.delete_knowledge_node(kid)
        if self._selected_part:
            self._refresh_knowledge_panel(self._selected_part)
            self._refresh_anchored_parts()
            self._refresh_anchor_list()
        self.statusBar().showMessage("Wissensknoten gelöscht.")

    def _on_relation_link(self, url) -> None:
        scheme = url.scheme()
        if scheme != "delete-relation":
            return
        rid = url.host()
        from PyQt6.QtWidgets import QMessageBox
        if QMessageBox.question(
            self, "Löschen?", "Verbindung wirklich löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        ) != QMessageBox.StandardButton.Yes:
            return
        repo.delete_relationship(rid)
        if self._selected_part:
            self._refresh_relations_panel(self._selected_part)
        self.statusBar().showMessage("Verbindung gelöscht.")

    # ------------------------------------------------------------------
    # Connect parts
    # ------------------------------------------------------------------

    def _on_connect_parts(self) -> None:
        if len(self._multi_selected) != 2 or not self._current_filepath:
            return
        name_a, name_b = self._multi_selected[0], self._multi_selected[1]
        pid_a = self._part_map.get(name_a)
        pid_b = self._part_map.get(name_b)
        if not pid_a or not pid_b:
            return

        dlg = _RelationDialog(name_a, name_b, parent=self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        rel_type = dlg.relation_type()

        repo.add_relationship(pid_a, pid_b, rel_type)

        self._multi_selected = []
        self._connect_btn.setEnabled(False)
        self._part_tree.clearSelection()

        if self._selected_part:
            self._refresh_relations_panel(self._selected_part)

        self.statusBar().showMessage(
            f"Verbindung erstellt: {name_a} {rel_type} {name_b}"
        )

    # ------------------------------------------------------------------
    # Add knowledge
    # ------------------------------------------------------------------

    def _on_add_knowledge(self) -> None:
        if not self._selected_part or not self._current_filepath:
            return
        pid = self._part_map.get(self._selected_part)
        if not pid:
            return

        dlg = KnowledgeDialog(self._selected_part, parent=self)
        if dlg.exec() != KnowledgeDialog.DialogCode.Accepted:
            return

        data = dlg.get_data()
        if not data["content"]:
            return

        repo.add_knowledge_node(
            semantic_part_id=pid,
            content=data["content"],
            category=data["category"],
            author=data["author"],
            confidence=data["confidence"],
            relation_type=data["relation_type"],
        )

        self._refresh_anchored_parts()
        self._refresh_anchor_list()
        self._refresh_knowledge_panel(self._selected_part)
        self.statusBar().showMessage(
            f"Knowledge node added to {self._selected_part}"
        )


_RELATION_TYPES = ["drives", "contains", "connected_to", "seals", "monitors"]


class _RelationDialog(QDialog):
    def __init__(self, name_a: str, name_b: str, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Verbindung erstellen")
        self.setMinimumWidth(340)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"<b>{name_a}</b>  →  <b>{name_b}</b>"))

        layout.addWidget(QLabel("Beziehungstyp:"))
        self._combo = QComboBox()
        self._combo.addItems(_RELATION_TYPES)
        layout.addWidget(self._combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def relation_type(self) -> str:
        return self._combo.currentText()
