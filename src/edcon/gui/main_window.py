"""Setup code of the main window."""

from pathlib import PurePath
from importlib.resources import files
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from edcon.gui.connection_widget import ConnectionWidget
from edcon.gui.parameter_table_model import ParameterTableModel


class MainWindow(QMainWindow):
    """Defines the main window."""

    def __init__(self, ip_address):
        super().__init__()
        loadUi(PurePath(files('edcon') / 'gui' / 'main_window.ui'), self)
        self.setWindowTitle("GUI")

        self.connection_widget = loadUi(
            PurePath(files('edcon') / 'gui' / 'connection.ui'))
        self.connection_widget.line_edit_ip.setText(ip_address)
        self.toolBar.addWidget(self.connection_widget)

        # # Create an instance of CustomConnection
        self.connection_widget = ConnectionWidget(
            self.connection_widget.line_edit_ip, self.connection_widget.btnConnect)

        # Create an instance of ParameterTableModel
        csv_file_path = PurePath(
            files('edcon') / 'edrive' / 'data' / 'pnu_map.csv')
        self.model = ParameterTableModel(csv_file_path, self.connection_widget)

        self.btn_update.clicked.connect(self.btn_update_clicked)
        self.btn_confirm.clicked.connect(self.btn_confirm_clicked)
        self.btn_read.clicked.connect(self.btn_read_clicked)
        self.tbl_pnu_list.setModel(self.model)
        self.line_edit_pnu_list.textChanged.connect(self.on_text_changed)
        self.line_edit_pnu_value.returnPressed.connect(self.pressed_enter_value)
        self.line_edit_pnu.returnPressed.connect(self.pressed_enter_read)

    def read_pnu_from_text(self):
        """Takes input from line edit and reads corresponding PNU."""
        try:
            # Convert pnu to an integer
            pnu = int(self.line_edit_pnu.text())
        except ValueError as exception:
            QMessageBox.warning(
                self.line_edit_pnu_value.parent(),
                "Read PNU Failed",
                f"Failed to read PNU{self.line_edit_pnu.text()}: {str(exception)}"
            )
            return

        result = self.connection_widget.com.read_pnu(pnu, 0)
        # Do something with the result, such as displaying it in a QMessageBox
        QMessageBox.information(self.line_edit_pnu.parent(
        ), "Read PNU Result", f"The result for PNU {pnu} is: {result}")

    def write_pnu_value_from_text(self):
        """Takes input from line edit and write value into corresponding PNU."""
        new_value = self.line_edit_pnu_value.text()
        try:
            # Convert pnu to an integer
            pnu = int(self.line_edit_pnu.text())
        except ValueError as exception:
            QMessageBox.warning(
                self.line_edit_pnu_value.parent(),
                "Write PNU Failed",
                f"Failed to write PNU{self.line_edit_pnu.text()}: {str(exception)}"
            )
            return

        self.connection_widget.com.write_pnu(pnu, 0, new_value)
        # Do something with the result, such as displaying it in a QMessageBox
        QMessageBox.information(self.line_edit_pnu_value.parent(
        ), "Write PNU successfull", f"The value {new_value} is written in: {pnu}")

    def on_text_changed(self, text):
        """Searches for the content of the line edit in the table."""
        self.model.set_name_filter(text)
        self.tbl_pnu_list.model().layoutChanged.emit()

    def btn_update_clicked(self):
        """Activate the function set_pnu_for_all_rows."""
        self.model.set_pnu_for_all_rows()

    def btn_confirm_clicked(self):
        """Activate the functions set_value_for_one_row and write_pnu_value_from_text."""
        self.write_pnu_value_from_text()
        self.model.set_value_for_one_row(self.line_edit_pnu.text())

    def btn_read_clicked(self):
        """Activate the function read_pnu_from_text."""
        self.read_pnu_from_text()

    def pressed_enter_read(self):
        """Activate the function read_pnu_from_text."""
        self.read_pnu_from_text()

    def pressed_enter_value(self):
        """Activate the function write_pnu_value_from_text and set_value_for_one_row."""
        self.write_pnu_value_from_text()
        self.model.set_value_for_one_row(self.line_edit_pnu.text())
