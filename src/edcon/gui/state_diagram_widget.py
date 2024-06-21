"""Functionality related to the connection widget."""

from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtCore import Qt
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
        self.scene = StateDiagram()
        self.graphicsView.setVisible(True)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setSceneRect(self.scene.sceneRect())
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def update(self, current_state):
        """Updates the state diagram view"""
        self.scene.update(current_state)
