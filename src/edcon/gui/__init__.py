"""Test import of pyqt5."""

import sys

try:
    # pylint: disable=import-error, no-name-in-module
    from PyQt5.QtWidgets import (
        QApplication,
    )
except ImportError:
    print("Error loading PyQt5!")
    print(
        "Please install festo-edcon with GUI support:\n\n\tpip install 'festo-edcon[gui]'\n"
    )
    print("Alternatively, install PyQt5 manually:\n\n\tpip install pyqt5\n")
    sys.exit(1)
