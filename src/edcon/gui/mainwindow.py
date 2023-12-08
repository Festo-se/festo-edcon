from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("C:/Workspace/festo-edcon/src/edcon/gui/mainwindow.ui", self)
        self.setWindowTitle("GUI")

        # Create a tab widget to hold the different pages
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)

        # Create the connection page
        connection_page = QWidget()
        loadUi("C:/Workspace/festo-edcon/src/edcon/gui/connection.ui", connection_page)
        self.tabWidget.addTab(connection_page, "Connection")

        # Create the configuration page
        configuration_page = QWidget()
        loadUi("C:/Workspace/festo-edcon/src/edcon/gui/configuration.ui", configuration_page)
        self.tabWidget.addTab(configuration_page, "Configuration")

        # Create the movement page
        movement_page = QWidget()
        loadUi("C:/Workspace/festo-edcon/src/edcon/gui/movement.ui", movement_page)
        self.tabWidget.addTab(movement_page, "Movement")

        # Create the analysis page
        analysis_page = QWidget()
        loadUi("C:/Workspace/festo-edcon/src/edcon/gui/analysis.ui", analysis_page)
        self.tabWidget.addTab(analysis_page, "Analysis")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()