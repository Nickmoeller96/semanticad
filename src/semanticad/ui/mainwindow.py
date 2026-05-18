"""Main application window — 3-panel layout: side | viewer | info."""

import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QColor
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
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
        self._part_tree.itemClicked.connect(self._on_tree_item_clicked)
        left_layout.addWidget(self._part_tree, stretch=3)

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

        left.setMinimumWidth(230)

        # ---- Center: 3D viewer ----
        self._viewer = OCCViewerWidget()
        self._viewer.part_selected.connect(self._on_part_selected)

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
        right_layout.addWidget(self._knowledge_browser, stretch=1)

        right.setMinimumWidth(260)

        splitter.addWidget(left)
        splitter.addWidget(self._viewer)
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
        if name:
            self._show_part_info(name)

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
            html_parts.append(
                f"<div style='margin-bottom:10px; padding:8px; background:#fff; "
                f"border-left:3px solid #3b5bdb; border-radius:3px;'>"
                f"<b>{icon} {n['category']}</b>"
                f"<span style='color:#888; font-size:10px'> · {author} · {conf_pct}% confidence</span><br>"
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
