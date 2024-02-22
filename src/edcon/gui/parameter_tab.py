"""Setup code of the main window."""

from pathlib import PurePath
from importlib.resources import files
from PyQt5.QtWidgets import (
    QWidget,
    QHeaderView,
)  # pylint: disable=import-error, no-name-in-module
from PyQt5.uic import loadUi
from edcon.gui.parameter_table_model import ParameterTableModel
from edcon.gui.qt_helpers import checkmark, ballot


class ParameterTab(QWidget):
    """Defines the main window."""

    def __init__(self, pnu_read_func, pnu_write_func):
        super().__init__()
        loadUi(PurePath(files("edcon") / "gui" / "parameter_tab.ui"), self)

        self.read_pnu = pnu_read_func
        self.write_pnu = pnu_write_func
        # Create an instance of ParameterTableModel
        self.model = ParameterTableModel()

        self.table_view_pnu_list.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table_view_pnu_list.setModel(self.model)
        self.button_pnu_read.clicked.connect(self.button_pnu_read_clicked)
        self.button_pnu_write.clicked.connect(self.button_pnu_write_clicked)
        self.button_pnu_list_update.clicked.connect(self.button_pnu_list_update_clicked)
        self.line_edit_pnu_list_filter.textChanged.connect(
            self.on_pnu_list_filter_text_changed
        )
        self.line_edit_pnu_value.returnPressed.connect(self.pressed_enter_value)
        self.line_edit_pnu.returnPressed.connect(self.pressed_enter_read)

    def read_pnu_from_text(self):
        """Takes input from line edit and reads corresponding PNU."""
        ret_status = "Unknown"
        try:
            # Convert pnu to an integer
            pnu = int(self.line_edit_pnu.text())
            result = self.read_pnu(pnu)
            if result is not None:
                self.label_pnu_feedback.setText(f"{checkmark()} {result}")
                return
        except ValueError as exception:
            ret_status = str(exception)

        self.label_pnu_feedback.setText(f"{ballot()} Failed to read PNU {ret_status}")

    def write_pnu_value_from_text(self):
        """Takes input from line edit and write value into corresponding PNU."""
        ret_status = "Unknown"
        try:
            # Convert pnu to an integer
            pnu = int(self.line_edit_pnu.text())
            value = self.line_edit_pnu_value.text()
            if self.write_pnu(pnu, value=value):
                self.label_pnu_value_feedback.setText(f"{checkmark()} Success!")
                return
        except ValueError as exception:
            ret_status = str(exception)

        self.label_pnu_value_feedback.setText(
            f"{ballot()} Failed to write PNU: {ret_status}"
        )

    def on_pnu_list_filter_text_changed(self, text):
        """Updates the table view content with name filter."""
        self.model.set_name_filter(text)

    def button_pnu_read_clicked(self):
        """Button click callback for PNU read."""
        self.read_pnu_from_text()
        self.model.update_value(self.line_edit_pnu.text(), self.read_pnu)

    def button_pnu_write_clicked(self):
        """Button click callback for PNU write."""
        self.write_pnu_value_from_text()
        self.model.update_value(self.line_edit_pnu.text(), self.read_pnu)

    def button_pnu_list_update_clicked(self):
        """Button click callback for PNU list update."""
        self.model.update_all_values(self.read_pnu)

    def pressed_enter_read(self):
        """Enter press callback for PNU read."""
        self.read_pnu_from_text()
        self.model.update_value(self.line_edit_pnu.text(), self.read_pnu)

    def pressed_enter_value(self):
        """Enter press callback for PNU write."""
        self.write_pnu_value_from_text()
        self.model.update_value(self.line_edit_pnu.text(), self.read_pnu)
