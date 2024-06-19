"""Setup code of the process data tab."""

from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QHeaderView
from PyQt5.uic import loadUi
from edcon.edrive.telegram1_handler import Telegram1Handler
from edcon.edrive.telegram9_handler import Telegram9Handler
from edcon.edrive.telegram102_handler import Telegram102Handler
from edcon.edrive.telegram111_handler import Telegram111Handler

from edcon.gui.processdata_treeview_model import ProcessDataTreeViewModel
from edcon.gui.state_diagram import StateDiagram
from edcon.gui.pyqt_helpers import bold_string


class ProcessDataTab(QWidget):
    """Defines the process data tab."""

    def __init__(self, get_com_function):
        super().__init__()
        loadUi(PurePath(files("edcon") / "gui" / "ui" / "processdata_tab.ui"), self)
        self.get_com_function = get_com_function

        self.model = None
        self.scene = None

        self.comboBox.currentIndexChanged.connect(self.select_telegramhandler)

        self.expand_button.clicked.connect(self.expand_all_button_clicked)
        self.state_diagram_button.clicked.connect(self.toggle_graphicview)

        self.selection_dict = {
            "Telegram1": Telegram1Handler,
            "Telegram9": Telegram9Handler,
            "Telegram102": Telegram102Handler,
            "Telegram111": Telegram111Handler,
        }

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_functions)
        self.timer.start(100)

    def update_functions(self):
        """Updates the content of process data tab"""
        if self.model is not None:
            self.model.update()
            self.label_fault_string.setText(
                bold_string(f"{self.model.fault_string()}", "red")
            )
            if self.scene is not None:
                self.scene.update(
                    self.model.tgh.telegram.stw1, self.model.tgh.telegram.zsw1
                )

    def select_telegramhandler(self):
        """Select a Telegram handler from the combobox."""
        selected_item_name = self.comboBox.currentText()

        if self.model is not None:
            self.model.clear()

        if selected_item_name not in self.selection_dict:
            self.model = None
            return

        com = self.get_com_function()
        self.model = ProcessDataTreeViewModel(
            self.selection_dict[selected_item_name](com, config_mode="write"),
        )
        self.treeView.setModel(self.model)
        self.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.scene = StateDiagram()
        self.graphicsView.setVisible(False)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setSceneRect(self.scene.sceneRect())
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def expand_all_button_clicked(self):
        """Expand the whole treeview"""
        self.treeView.expandAll()

    def toggle_graphicview(self):
        """Toggle graphicview button callback"""
        self.graphicsView.setVisible(not self.graphicsView.isVisible())
