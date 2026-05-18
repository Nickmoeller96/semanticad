"""Dialog for adding a knowledge node to a selected part."""

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
)

CATEGORIES = [
    "Failure Mode",
    "Maintenance",
    "Design Rationale",
    "Material Experience",
    "Operating Experience",
    "Safety Note",
]

RELATION_TYPES = ["applies_to", "warning_for", "experience_with"]


class KnowledgeDialog(QDialog):
    def __init__(self, part_name: str, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"Add Knowledge — {part_name}")
        self.setMinimumWidth(500)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        form = QFormLayout()
        form.setSpacing(8)

        self._category = QComboBox()
        self._category.addItems(CATEGORIES)
        form.addRow("Category:", self._category)

        self._content = QTextEdit()
        self._content.setMinimumHeight(130)
        self._content.setPlaceholderText(
            "Describe the knowledge, experience, failure mode, or note…"
        )
        form.addRow("Content:", self._content)

        self._author = QLineEdit()
        self._author.setPlaceholderText("e.g. Müller, Hans")
        form.addRow("Author:", self._author)

        self._confidence = QDoubleSpinBox()
        self._confidence.setRange(0.0, 1.0)
        self._confidence.setSingleStep(0.1)
        self._confidence.setValue(1.0)
        self._confidence.setDecimals(1)
        self._confidence.setToolTip("0.0 = uncertain, 1.0 = fully verified")
        form.addRow("Confidence:", self._confidence)

        self._relation = QComboBox()
        self._relation.addItems(RELATION_TYPES)
        form.addRow("Relation:", self._relation)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _validate_and_accept(self) -> None:
        if self._content.toPlainText().strip():
            self.accept()

    def get_data(self) -> dict:
        return {
            "category": self._category.currentText(),
            "content": self._content.toPlainText().strip(),
            "author": self._author.text().strip() or "Anonymous",
            "confidence": self._confidence.value(),
            "relation_type": self._relation.currentText(),
        }
