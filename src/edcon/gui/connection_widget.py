"""Functionality related to the connection widget."""
from PyQt5.QtWidgets import QWidget, QMessageBox
from pymodbus.exceptions import ConnectionException
from edcon.edrive.com_modbus import ComModbus


class ConnectionWidget(QWidget):
    """Defines the connection widget."""

    def __init__(self, line_edit_ip, push_button_connect):
        super().__init__()

        # Connect the button's clicked signal to the function
        push_button_connect.clicked.connect(self.push_button_connect_clicked)

        # Store the QLineEdit and QPushButton for future use
        self.line_edit_ip = line_edit_ip
        self.push_button_connect = push_button_connect

        self.com = None

    def push_button_connect_clicked(self):
        """Method that is called when the push_button_connect is clicked."""

        # Get the content of the QLineEdit txteditIP
        ip_address = self.line_edit_ip.text()
        try:
            # Establish the connection with the drive
            self.com = ComModbus(ip_address, timeout_ms=0)
        except ConnectionException as exception:
            QMessageBox.warning(self, "Connection Failed",
                                f"Failed to establish the connection: {str(exception)}")
            return

        QMessageBox.information(
            self, "Connection Successful", "Connection established!")
