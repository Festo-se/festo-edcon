"""Functionality related to the connection widget."""

from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from edcon.gui.state_diagram import StateDiagram


class StateDiagramWidget(QWidget):
    """Defines the state diagram widget."""

    # pylint: disable=too-few-public-methods
    def __init__(self):
        super().__init__()
        loadUi(
            PurePath(files("edcon") / "gui" / "ui" / "state_diagram.ui"),
            self,
        )
        self.view = StateDiagram()
        self.verticalLayout.addWidget(self.view)

    def update(self, current_state):
        """Updates the state diagram view"""
        self.view.update(current_state)
