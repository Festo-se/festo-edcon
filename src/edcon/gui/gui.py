"""GUI entry point."""
from PyQt5.QtWidgets import QApplication  # pylint: disable=import-error, no-name-in-module
from edcon.gui.main_window import MainWindow


def start_gui(ip_address):
    """Entry point for the GUI."""
    app = QApplication([])
    window = MainWindow(ip_address=ip_address)
    window.show()
    app.exec_()
