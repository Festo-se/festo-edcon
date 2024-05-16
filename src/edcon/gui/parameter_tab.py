"""Setup code of the main window."""

from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtWidgets import QWidget, QHeaderView
from PyQt5.uic import loadUi
from edcon.gui.parameter_table_model import ParameterTableModel
from edcon.gui.pyqt_helpers import checkmark, ballot


class ParameterTab(QWidget):
    """Defines the parameter tab widget."""

    def __init__(self, pnu_read_func, pnu_write_func):
        super().__init__()
        loadUi(PurePath(files("edcon") / "gui" / "ui" / "parameter_tab.ui"), self)

        self.read_pnu = pnu_read_func
        self.write_pnu = pnu_write_func
        # Create an instance of ParameterTableModel
        self.model = ParameterTableModel()

        self.table_view_pnu_list.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table_view_pnu_list.setModel(self.model)
        self.button_pnu_read.clicked.connect(self.button_pnu_read_clicked)
        self.line_edit_pnu.returnPressed.connect(self.button_pnu_read_clicked)
        self.button_pnu_write.clicked.connect(self.button_pnu_write_clicked)
        self.line_edit_pnu_value.returnPressed.connect(self.button_pnu_write_clicked)
        self.button_pnu_list_update.clicked.connect(self.button_pnu_list_update_clicked)
        self.line_edit_pnu_list_filter.textChanged.connect(
            self.on_pnu_list_filter_text_changed
        )

    def on_pnu_list_filter_text_changed(self, text):
        """Updates the table view content with name filter.

        Parameters:
            text (str): name filter text
        """
        self.model.set_name_filter(text)

    def button_pnu_read_clicked(self):
        """Button click callback for PNU read."""
        ret_status = "Unknown"
        try:
            pnu = int(self.line_edit_pnu.text())
        except ValueError as exception:
            ret_status = str(exception)

        data = self.model.update_value(pnu, self.read_pnu)
        if data is None:
            self.label_pnu_feedback.setText(
                f"{ballot()} Failed to read PNU {ret_status}"
            )
            return
        self.label_pnu_feedback.setText(f"{checkmark()} {data.value} ({data.name})")
        self.label_pnu_value_feedback.setText("")

    def button_pnu_write_clicked(self):
        """Button click callback for PNU write."""
        ret_status = "Unknown"
        try:
            pnu = int(self.line_edit_pnu.text())
        except ValueError as exception:
            ret_status = str(exception)

        value = self.line_edit_pnu_value.text()
        if not self.write_pnu(pnu, value=value):
            self.label_pnu_value_feedback.setText(
                f"{ballot()} Failed to write PNU: {ret_status}"
            )
            return
        self.model.update_value(pnu, self.read_pnu)
        self.label_pnu_feedback.setText("")
        self.label_pnu_value_feedback.setText(f"{checkmark()} Success!")

    def button_pnu_list_update_clicked(self):
        """Button click callback for PNU list update."""
        self.model.update_all_values(self.read_pnu)
