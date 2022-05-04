import sys

from ui import main_window
from PySide6.QtWidgets import QApplication


def main():
    """
    main
    """
    app = QApplication([])
    window = main_window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
