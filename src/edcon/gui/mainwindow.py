# mainwindow

from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QStackedWidget, QWidget, QVBoxLayout, QLabel
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("C:/Workspace/festo-edcon/src/edcon/gui/mainwindow.ui", self)
        self.setWindowTitle("MainWindow")

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.actionVerbindungsverwaltung.triggered.connect(self.show_verbindungsverwaltung_page)
        self.actionKonfiguration.triggered.connect(self.show_konfiguration_page)
        self.actionSteuerung.triggered.connect(self.show_steuerung_page)
        self.actionAnalyse_und_Diagnose.triggered.connect(self.show_analyse_page)

        self.create_pages()

    def create_pages(self):
        verbindungsverwaltung_page = QWidget()
        verbindungsverwaltung_layout = QVBoxLayout()
        verbindungsverwaltung_label = QLabel("Verbindungsverwaltung Page")
        verbindungsverwaltung_layout.addWidget(verbindungsverwaltung_label)
        verbindungsverwaltung_page.setLayout(verbindungsverwaltung_layout)
        self.stacked_widget.addWidget(verbindungsverwaltung_page)

        konfiguration_page = QWidget()
        konfiguration_layout = QVBoxLayout()
        konfiguration_label = QLabel("Konfiguration Page")
        konfiguration_layout.addWidget(konfiguration_label)
        konfiguration_page.setLayout(konfiguration_layout)
        self.stacked_widget.addWidget(konfiguration_page)

        steuerung_page = QWidget()
        steuerung_layout = QVBoxLayout()
        steuerung_label = QLabel("Steuerung Page")
        steuerung_layout.addWidget(steuerung_label)
        steuerung_page.setLayout(steuerung_layout)
        self.stacked_widget.addWidget(steuerung_page)

        analyse_page = QWidget()
        analyse_layout = QVBoxLayout()
        analyse_label = QLabel("Analyse und Diagnose Page")
        analyse_layout.addWidget(analyse_label)
        analyse_page.setLayout(analyse_layout)
        self.stacked_widget.addWidget(analyse_page)

    def show_verbindungsverwaltung_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_konfiguration_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_steuerung_page(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_analyse_page(self):
        self.stacked_widget.setCurrentIndex(3)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()