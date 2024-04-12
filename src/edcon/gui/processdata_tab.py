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


class ProcessDataTab(QWidget):
    """Defines the main window."""

    def __init__(self, get_com_function):
        super().__init__()
        loadUi(PurePath(files("edcon") / "gui" / "ui" / "processdata_tab.ui"), self)
        self.get_com_function = get_com_function

        self.model = ProcessDataTreeViewModel(None)

        self.comboBox.currentIndexChanged.connect(self.select_telegramhandler)

    def select_telegramhandler(self):
        """Select a Telegram handler from the combobox."""
        selected_item_name = self.comboBox.currentText()

        if self.model.tgh is not None:
            self.model.tgh.shutdown()
            self.model = ProcessDataTreeViewModel(None)
            self.treeView.setModel(self.model)
            self.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        if selected_item_name == "None":
            self.model = ProcessDataTreeViewModel(None)
            self.treeView.setModel(self.model)
            self.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        elif selected_item_name == "Telegram1":
            com = self.get_com_function()
            com.write_pnu(3490, value=1)
            self.model = ProcessDataTreeViewModel(Telegram1Handler(com))
            self.treeView.setModel(self.model)
            self.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        elif selected_item_name == "Telegram9":
            com = self.get_com_function()
            com.write_pnu(3490, value=9)
            self.model = ProcessDataTreeViewModel(Telegram9Handler(com))
            self.treeView.setModel(self.model)
            self.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        elif selected_item_name == "Telegram102":
            com = self.get_com_function()
            com.write_pnu(3490, value=102)
            self.model = ProcessDataTreeViewModel(Telegram102Handler(com))
            self.treeView.setModel(self.model)
            self.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        elif selected_item_name == "Telegram111":
            com = self.get_com_function()
            com.write_pnu(3490, value=111)
            self.model = ProcessDataTreeViewModel(Telegram111Handler(com))
            self.treeView.setModel(self.model)
            self.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
