"""GUI entry point."""
from PyQt5.QtWidgets import QApplication
from edcon.gui.mainwindow import MainWindow

class Gui:
    """GUI container class. Entry point for the GUI."""
    def __init__(self, ip_address):
        app = QApplication([])
        window = MainWindow(ip_address)
        window.show()
        app.exec_()
