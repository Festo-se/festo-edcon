"""Setup code of the main window."""

from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class RecordTab(QWidget):
    """Defines the record tab widget."""

    def __init__(self):
        super().__init__()
        loadUi(PurePath(files("edcon") / "gui" / "ui" / "record_tab.ui"), self)