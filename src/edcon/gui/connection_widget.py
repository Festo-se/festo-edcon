"""Functionality related to the connection widget."""

from pathlib import PurePath
from importlib.resources import files
from PyQt5.QtWidgets import QWidget  # pylint: disable=import-error, no-name-in-module
from PyQt5.uic import loadUi
from pymodbus.exceptions import ConnectionException
from edcon.gui.pyqt_helpers import bold_string


class ConnectionWidget(QWidget):
    """Defines the connection widget."""

    # pylint: disable=too-few-public-methods
    def __init__(self, ip_address, connect_function):
        super().__init__()
        loadUi(PurePath(files("edcon") / "gui" / "ui" / "connection.ui"), self)
        # Connect the button's clicked signal to the function
        self.button_connect.clicked.connect(self.connect)

        self.line_edit_ip.setText(ip_address)
        self.connect_function = connect_function

    def connect(self):
        """Method that is called when the push_button_connect is clicked."""
        try:
            self.connect_function(self.line_edit_ip.text())
        except ConnectionException as exception:
            self.label_connect_feedback.setText(bold_string(f"{str(exception)}", "red"))
            return

        self.label_connect_feedback.setText(bold_string("Connected", "green"))
