"""OCC 3D viewer widget — subclasses qtViewer3d directly for macOS Qt6 compatibility."""

# Backend must be loaded before qtDisplay is imported
from OCC.Display.backend import load_backend
load_backend("pyqt6")

from OCC.Display.qtDisplay import qtViewer3d  # noqa: E402

from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect, Graphic3d_NOM_ALUMINIUM
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Aspect import Aspect_GFM_VER

from PyQt6.QtCore import pyqtSignal, QTimer
from PyQt6.QtWidgets import QWidget

from semanticad.viewer.step_loader import PartEntry, load_step as _load_step


_GRAY_COLOR      = Quantity_Color(0.62, 0.63, 0.65, Quantity_TOC_RGB)  # all parts default
_HIGHLIGHT_COLOR = Quantity_Color(0.18, 0.52, 1.00, Quantity_TOC_RGB)  # selected — bright blue
_ANCHOR_COLOR    = Quantity_Color(0.95, 0.78, 0.05, Quantity_TOC_RGB)  # knowledge anchor — gold


class OCCViewerWidget(qtViewer3d):
    """
    OCC 3D viewer with STEP loading, part-selection signal, and visual polish.

    All parts render in uniform gray. Clicking a part highlights it blue.
    Parts with knowledge anchors are gold; selection overrides to blue.
    """

    part_selected = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._parts: list[PartEntry] = []
        # {name: (AIS_Shape, base_color)}  — base_color is gray or gold (anchored)
        self._ais_shapes: dict[str, tuple[AIS_Shape, Quantity_Color]] = {}
        self._anchored_names: set[str] = set()
        self._selected_name: str | None = None
        self.sig_topods_selected.connect(self._on_selection)

    # ------------------------------------------------------------------
    # Qt overrides
    # ------------------------------------------------------------------

    def showEvent(self, event):
        super().showEvent(event)
        if not self._inited:
            self._do_init()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_step_file(self, filepath: str) -> list[PartEntry]:
        """Load a STEP file, display all parts in gray, return PartEntry list."""
        if not self._inited:
            self._do_init()

        self._parts = _load_step(filepath)
        self._ais_shapes = {}
        self._anchored_names = set()
        self._selected_name = None
        d = self._display

        mat = Graphic3d_MaterialAspect(Graphic3d_NOM_ALUMINIUM)

        for entry in self._parts:
            ais = AIS_Shape(entry.shape)
            ais.SetMaterial(mat)
            d.Context.Display(ais, False)
            d.Context.SetColor(ais, _GRAY_COLOR, False)
            self._ais_shapes[entry.name] = (ais, _GRAY_COLOR)

        d.EnableAntiAliasing()
        d.FitAll()

        for delay in (0, 80, 200):
            QTimer.singleShot(delay, self._force_repaint)

        return self._parts

    def highlight_anchored(self, names: set[str]) -> None:
        """Color anchored parts gold, restore others to gray. Keeps selection blue."""
        if not self._inited or not self._ais_shapes:
            return
        self._anchored_names = names
        d = self._display
        for name, (ais, _) in self._ais_shapes.items():
            if name == self._selected_name:
                color = _HIGHLIGHT_COLOR
            elif name in names:
                color = _ANCHOR_COLOR
            else:
                color = _GRAY_COLOR
            self._ais_shapes[name] = (ais, _ANCHOR_COLOR if name in names else _GRAY_COLOR)
            d.Context.SetColor(ais, color, False)
            d.Context.Redisplay(ais, False)
        d.Repaint()
        self.update()

    def select_part(self, name: str) -> None:
        """Highlight one part blue; restore the previous selection to its base color."""
        if not self._inited or not self._ais_shapes:
            return
        d = self._display

        # Restore previous selection
        if self._selected_name and self._selected_name in self._ais_shapes:
            prev_ais, prev_base = self._ais_shapes[self._selected_name]
            d.Context.SetColor(prev_ais, prev_base, False)
            d.Context.Redisplay(prev_ais, False)

        self._selected_name = name

        if name and name in self._ais_shapes:
            ais, _ = self._ais_shapes[name]
            d.Context.SetColor(ais, _HIGHLIGHT_COLOR, False)
            d.Context.Redisplay(ais, False)

        d.Repaint()
        self.update()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _do_init(self):
        self.InitDriver()
        d = self._display
        d.SetModeShaded()
        d.set_bg_gradient_color([20, 22, 28], [38, 42, 52], Aspect_GFM_VER)

    def _force_repaint(self):
        if self._inited:
            self._display.Repaint()
        self.update()

    def _on_selection(self, shapes: list) -> None:
        for shape in shapes:
            name = self._find_name(shape)
            if name:
                self.select_part(name)
                self.part_selected.emit(name)
                return

    def _find_name(self, selected_shape) -> str | None:
        for entry in self._parts:
            try:
                if entry.shape.IsSame(selected_shape):
                    return entry.name
            except Exception:
                pass
        return None
