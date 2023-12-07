# mainwindow

from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QStackedWidget, QWidget, QVBoxLayout, QLabel
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("C:/Workspace/festo-edcon/src/edcon/gui/mainwindow.ui", self)
        self.setWindowTitle("MainWindow")

        # Create a stacked widget to hold the different pages
        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        # Create the connection page
        connection_page = QMainWindow()
        loadUi("C:/Workspace/festo-edcon/src/edcon/gui/connection.ui", connection_page)
        self.stackedWidget.addWidget(connection_page)

        # Create the configuration page
        configuration_page = QMainWindow()
        loadUi("C:/Workspace/festo-edcon/src/edcon/gui/configuration.ui", configuration_page)
        self.stackedWidget.addWidget(configuration_page)

        # Create the movement page
        movement_page = QMainWindow()
        loadUi("C:/Workspace/festo-edcon/src/edcon/gui/movement.ui", movement_page)
        self.stackedWidget.addWidget(movement_page)

        # Create the analysis page
        analysis_page = QMainWindow()
        loadUi("C:/Workspace/festo-edcon/src/edcon/gui/analysis.ui", analysis_page)
        self.stackedWidget.addWidget(analysis_page)

        # Connect the menu actions to switch between pages
        self.actionconnection.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.actionconfiguration.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.actionmovement.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.actionanalysis.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(3))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()