"""Functionality related to the connection widget."""

from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
import pyqtgraph as pg
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
        self.view_box = StateDiagram()
        graphic_widget = pg.GraphicsLayoutWidget()
        graphic_widget.addItem(self.view_box)
        self.verticalLayout.addWidget(graphic_widget)

    def update(self, current_state):
        """Updates the state diagram view"""
        self.view_box.update_state(current_state)
