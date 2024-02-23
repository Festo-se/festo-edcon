"""Setup code of the main window."""

from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from edcon.gui.connection_widget import ConnectionWidget
from edcon.gui.parameter_tab import ParameterTab
from edcon.edrive.com_modbus import ComModbus


class MainWindow(QMainWindow):
    """Defines the main window."""

    def __init__(self, ip_address):
        super().__init__()
        self._com = None

        loadUi(PurePath(files("edcon") / "gui" / "ui" / "main_window.ui"), self)
        self.setWindowTitle("GUI")

        self.connection_widget = ConnectionWidget(
            ip_address=ip_address, connect_function=self.connect_function
        )
        self.toolBar.addWidget(self.connection_widget)

        self.tabWidget.addTab(
            ParameterTab(self.pnu_read_function, self.pnu_write_function), "Parameter"
        )

    @property
    def com(self):
        """
        Returns the communication driver.
        Trys to establish the connection if not yet established.
        """
        if self._com is None:
            self.connection_widget.connect()
        return self._com

    def connect_function(self, ip_address):
        """Establishes the connection using the communication driver."""
        self._com = ComModbus(ip_address=ip_address, timeout_ms=0)

    def pnu_read_function(self, pnu):
        """Reads a PNU using the communication driver."""
        return self.com.read_pnu(pnu)

    def pnu_write_function(self, pnu, value):
        """Writes a PNU using the communication driver."""
        return self.com.write_pnu(pnu, value=value)
