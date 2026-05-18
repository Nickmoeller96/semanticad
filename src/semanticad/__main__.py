"""Entry point: python -m semanticad"""

import sys
from dotenv import load_dotenv

load_dotenv()


def main():
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QCoreApplication

    app = QApplication(sys.argv)
    app.setApplicationName("SemantiCAD")
    app.setOrganizationName("SemantiCAD")

    from semanticad.ui.mainwindow import MainWindow
    window = MainWindow()
    window.show()

    # Process pending events so showEvent fires (and OCC InitDriver runs)
    # before the event loop starts — critical on macOS+Qt6
    app.processEvents()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
