"""Chat panel — AI Engineering Assistant powered by the Anthropic agent."""

import html

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from semanticad.agent.client import SemanticAgentClient

_TOOL_LABELS = {
    "get_part_info":             "Bauteil-Info abrufen…",
    "get_knowledge_for_part":    "Wissensknoten laden…",
    "search_knowledge_semantic": "Wissens-Pool durchsuchen…",
    "find_similar_parts":        "Ähnliche Bauteile suchen…",
    "get_related_knowledge":     "Verwandtes Wissen suchen…",
    "list_parts_by_type":        "Bauteilliste abrufen…",
}

_DEMO_QUESTIONS = [
    "Was muss ich über Pumpe P-101 wissen?",
    "P-101 vibriert seit gestern. Was sind mögliche Ursachen?",
    "Wir wollen P-101 durch eine Pumpe mit höherer Förderhöhe ersetzen. Was sollten wir beachten?",
]


class _AgentWorker(QThread):
    tool_called = pyqtSignal(str)
    finished    = pyqtSignal(str)
    errored     = pyqtSignal(str)

    def __init__(self, client: SemanticAgentClient, conversation: list[dict]) -> None:
        super().__init__()
        self._client = client
        self._conversation = conversation

    def run(self) -> None:
        try:
            result = self._client.send(
                self._conversation,
                on_tool_call=lambda name: self.tool_called.emit(name),
            )
            self.finished.emit(result)
        except Exception as exc:
            self.errored.emit(str(exc))


class ChatPanel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._client = SemanticAgentClient()
        self._conversation: list[dict] = []
        self._worker: _AgentWorker | None = None
        self._build_ui()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_part_map(self, part_map: dict[str, str]) -> None:
        self._client.set_part_map(part_map)

    def set_current_part(self, name: str) -> None:
        self._input.setPlaceholderText(f'Frage zu "{name}" oder zur gesamten Anlage…')

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 6)
        layout.setSpacing(4)

        # Header row
        header_row = QHBoxLayout()
        header = QLabel("AI Engineering Assistant")
        header.setStyleSheet("font-weight: bold; font-size: 13px; color: #1a1a2e;")
        header_row.addWidget(header)
        header_row.addStretch()

        clear_btn = QPushButton("Verlauf löschen")
        clear_btn.setStyleSheet(
            "QPushButton { color: #666; border: none; font-size: 11px; }"
            "QPushButton:hover { color: #333; }"
        )
        clear_btn.clicked.connect(self._clear)
        header_row.addWidget(clear_btn)
        layout.addLayout(header_row)

        # Demo question shortcuts
        demo_row = QHBoxLayout()
        demo_row.setSpacing(4)
        for q in _DEMO_QUESTIONS:
            btn = QPushButton(q[:40] + "…")
            btn.setToolTip(q)
            btn.setStyleSheet(
                "QPushButton { font-size: 10px; color: #3b5bdb; background: #eef2ff; "
                "border: 1px solid #c5cef5; border-radius: 3px; padding: 2px 5px; }"
                "QPushButton:hover { background: #dde4ff; }"
            )
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.clicked.connect(lambda _checked, question=q: self._send(question))
            demo_row.addWidget(btn)
        layout.addLayout(demo_row)

        # Chat history display
        self._history = QTextBrowser()
        self._history.setStyleSheet(
            "font-size: 12px; background: #fafafa; "
            "border: 1px solid #ddd; border-radius: 4px;"
        )
        self._history.setOpenLinks(False)
        layout.addWidget(self._history, stretch=1)

        # Status label (shown while agent is thinking)
        self._status = QLabel("")
        self._status.setStyleSheet("font-size: 11px; color: #888; font-style: italic;")
        self._status.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self._status)

        # Input row
        input_row = QHBoxLayout()
        input_row.setSpacing(6)

        self._input = QLineEdit()
        self._input.setPlaceholderText("Frage zur Anlage stellen…  (STEP-Datei zuerst laden)")
        self._input.setStyleSheet(
            "font-size: 12px; padding: 5px; border: 1px solid #ccc; border-radius: 4px;"
        )
        self._input.returnPressed.connect(self._on_send_clicked)
        input_row.addWidget(self._input, stretch=1)

        self._send_btn = QPushButton("Senden")
        self._send_btn.setStyleSheet(
            "QPushButton { background: #3b5bdb; color: white; border-radius: 4px; "
            "padding: 5px 14px; font-size: 12px; }"
            "QPushButton:disabled { background: #aaa; }"
            "QPushButton:hover { background: #2f4ac0; }"
        )
        self._send_btn.clicked.connect(self._on_send_clicked)
        input_row.addWidget(self._send_btn)

        layout.addLayout(input_row)

        self._append_system(
            "Lade eine STEP-Datei und stelle dann Fragen zur Anlage. "
            "Der Agent greift auf den Wissens-Graphen zu und kombiniert die Ergebnisse."
        )

    # ------------------------------------------------------------------
    # Sending / receiving
    # ------------------------------------------------------------------

    def _on_send_clicked(self) -> None:
        text = self._input.text().strip()
        if text:
            self._send(text)

    def _send(self, text: str) -> None:
        if self._worker and self._worker.isRunning():
            return

        self._input.clear()
        self._append_user(text)
        self._conversation.append({"role": "user", "content": text})

        self._set_busy(True)

        self._worker = _AgentWorker(self._client, list(self._conversation))
        self._worker.tool_called.connect(self._on_tool_called)
        self._worker.finished.connect(self._on_finished)
        self._worker.errored.connect(self._on_error)
        self._worker.start()

    def _on_tool_called(self, name: str) -> None:
        label = _TOOL_LABELS.get(name, f"{name}…")
        self._status.setText(f"🔧 {label}")

    def _on_finished(self, text: str) -> None:
        self._conversation.append({"role": "assistant", "content": text})
        self._append_assistant(text)
        self._set_busy(False)

    def _on_error(self, msg: str) -> None:
        if "api_key" in msg.lower() or "auth" in msg.lower():
            self._append_system(
                "⚠️ Kein API-Key gefunden. Bitte ANTHROPIC_API_KEY in der .env-Datei setzen."
            )
        else:
            self._append_system(f"⚠️ Fehler: {html.escape(msg)}")
        self._set_busy(False)

    def _set_busy(self, busy: bool) -> None:
        self._send_btn.setEnabled(not busy)
        self._input.setEnabled(not busy)
        if not busy:
            self._status.setText("")
        else:
            self._status.setText("Agent denkt nach…")

    def _clear(self) -> None:
        self._conversation.clear()
        self._history.clear()
        self._append_system("Verlauf gelöscht. Neue Frage stellen.")

    # ------------------------------------------------------------------
    # HTML rendering helpers
    # ------------------------------------------------------------------

    def _append_user(self, text: str) -> None:
        self._history.append(
            f"<div style='background:#eef2ff; border-radius:5px; padding:6px 8px; margin:4px 0;'>"
            f"<b>Du:</b> {html.escape(text)}"
            f"</div>"
        )

    def _append_assistant(self, text: str) -> None:
        # Convert newlines to <br> and escape HTML
        body = html.escape(text).replace("\n\n", "</p><p>").replace("\n", "<br>")
        self._history.append(
            f"<div style='padding:4px 0; margin:4px 0;'>"
            f"<b>🤖 Agent:</b><p style='margin:4px 0 0 0'>{body}</p>"
            f"</div>"
            f"<hr style='border:none; border-top:1px solid #eee; margin:4px 0;'>"
        )

    def _append_system(self, text: str) -> None:
        self._history.append(
            f"<div style='color:#888; font-size:11px; font-style:italic; margin:2px 0;'>"
            f"{html.escape(text)}</div>"
        )
