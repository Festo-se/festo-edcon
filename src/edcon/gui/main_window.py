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
        self.connection_widget.txteditIP.setText(ip_address)
        self.toolBar.addWidget(self.connection_widget)

        # # Create an instance of CustomConnection
        self.connection_widget = ConnectionWidget(
            self.connection_widget.txteditIP, self.connection_widget.btnConnect)

        # Create an instance of ParameterTableModel
        csv_file_path = PurePath(
            files('edcon') / 'edrive' / 'data' / 'pnu_map.csv')
        self.model = ParameterTableModel(csv_file_path, self.connection_widget)

        self.btnUpdate.clicked.connect(self.btn_update_clicked)
        self.btnConfirmValue.clicked.connect(self.btn_confirm_clicked)
        self.btnReadValue.clicked.connect(self.btn_read_clicked)
        self.tblPnuList.setModel(self.model)
        self.txtsearchPnuList.textChanged.connect(self.on_text_changed)
        self.txtValueParameter.returnPressed.connect(self.pressed_enter_value)
        self.txtsearchParameter.returnPressed.connect(self.pressed_enter_read)

    def read_pnu_from_text(self):
        """Takes input from line edit and reads corresponding PNU."""
        try:
            # Convert pnu to an integer
            pnu = int(self.txtsearchParameter.text())
        except ValueError as exception:
            QMessageBox.warning(
                self.txtValueParameter.parent(),
                "Read PNU Failed",
                f"Failed to read PNU{self.txtsearchParameter.text()}: {str(exception)}"
            )
            return

        result = self.connection_widget.com.read_pnu(pnu, 0)
        # Do something with the result, such as displaying it in a QMessageBox
        QMessageBox.information(self.txtsearchParameter.parent(
        ), "Read PNU Result", f"The result for PNU {pnu} is: {result}")

    def write_pnu_value_from_text(self):
        new_value = self.txtValueParameter.text()
        try:
            # Convert pnu to an integer
            pnu = int(self.txtsearchParameter.text())
        except ValueError as exception:
            QMessageBox.warning(
                self.txtValueParameter.parent(),
                "Write PNU Failed",
                f"Failed to write PNU{self.txtsearchParameter.text()}: {str(exception)}"
            )
            return

        self.connection_widget.com.write_pnu(pnu, 0, new_value)
        # Do something with the result, such as displaying it in a QMessageBox
        QMessageBox.information(self.txtValueParameter.parent(
        ), "Write PNU successfull", f"The value {new_value} is written in: {pnu}")

    def on_text_changed(self, text):
        self.model.set_name_filter(text)
        self.tblPnuList.model().layoutChanged.emit()

    def btn_update_clicked(self):
        self.model.set_pnu_for_all_rows()

    def btn_confirm_clicked(self):
        self.write_pnu_value_from_text()
        self.model.set_value_for_one_row(self.txtsearchParameter.text())

    def btn_read_clicked(self):
        self.read_pnu_from_text()

    def pressed_enter_read(self):
        self.read_pnu_from_text()

    def pressed_enter_value(self):
        self.write_pnu_value_from_text()
        self.model.set_value_for_one_row(self.txtsearchParameter.text())
