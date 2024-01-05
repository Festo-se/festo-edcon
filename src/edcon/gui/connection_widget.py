"""Functionality related to the connection widget."""
from pathlib import PurePath
from importlib.resources import files
from PyQt5.QtWidgets import QWidget, QMessageBox  # pylint: disable=import-error, no-name-in-module
from PyQt5.uic import loadUi
from pymodbus.exceptions import ConnectionException


class ConnectionWidget(QWidget):
    """Defines the connection widget."""

    # pylint: disable=too-few-public-methods
    def __init__(self, ip_address, connect_function):
        super().__init__()
        loadUi(PurePath(files('edcon') / 'gui' / 'connection.ui'), self)
        # Connect the button's clicked signal to the function
        self.btn_connect.clicked.connect(self.push_button_connect_clicked)

        self.line_edit_ip.setText(ip_address)
        self.connect_function = connect_function

    def push_button_connect_clicked(self):
        """Method that is called when the push_button_connect is clicked."""
        try:
            self.connect_function(self.line_edit_ip.text())
        except ConnectionException as exception:
            QMessageBox.warning(self, "Connection Failed",
                                f"Failed to establish the connection: {str(exception)}")
            return

        QMessageBox.information(
            self, "Connection Successful", "Connection established!")
