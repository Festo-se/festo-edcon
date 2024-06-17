"""Setup code of the process data tab."""

from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtWidgets import QWidget, QHeaderView
from PyQt5.uic import loadUi
from edcon.edrive.telegram1_handler import Telegram1Handler
from edcon.edrive.telegram9_handler import Telegram9Handler
from edcon.edrive.telegram102_handler import Telegram102Handler
from edcon.edrive.telegram111_handler import Telegram111Handler

from edcon.gui.processdata_treeview_model import ProcessDataTreeViewModel
from edcon.gui.processdata_graphicview_model import StateDiagram
from edcon.gui.pyqt_helpers import bold_string


class ProcessDataTab(QWidget):
    """Defines the process data tab."""

    def __init__(self, get_com_function):
        super().__init__()
        loadUi(PurePath(files("edcon") / "gui" / "ui" / "processdata_tab.ui"), self)
        self.get_com_function = get_com_function

        self.model = None
        self.graphic_view_widget = None

        self.comboBox.currentIndexChanged.connect(self.select_telegramhandler)

        self.expand_button.clicked.connect(self.expand_all_button_clicked)
        self.button_show_graphicview.clicked.connect(self.show_or_hide_graphicview)

        self.selection_dict = {
            "Telegram1": Telegram1Handler,
            "Telegram9": Telegram9Handler,
            "Telegram102": Telegram102Handler,
            "Telegram111": Telegram111Handler,
        }

    def update_treeview(self):
        """Update the treeview with the current model."""
        self.treeView.setModel(self.model)
        self.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

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
            self.set_fault_label_string,
        )

        self.state_diagram = StateDiagram(
            self.get_telegram_handler,
            self.graphicsView,
        )

        self.update_treeview()

    def get_telegram_handler(self):
        return self.model.tgh

    def set_fault_label_string(self, string):
        self.label_fault_string.setText(bold_string(f"{string}", "red"))

    def expand_all_button_clicked(self):
        """Expand the whole treeview"""
        self.treeView.expandAll()

    def show_or_hide_graphicview(self):
        """Show graphicview button callback"""
        self.graphicsView.setVisible(not self.graphicsView.isVisible())
