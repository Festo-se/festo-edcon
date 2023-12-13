from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget, QToolBar, QLineEdit, QPushButton
from PyQt5.uic import loadUi
from edcon.gui.costumconnection import CostumConnection
from edcon.gui.costumreadparameters import CostumReadParameters
from edcon.gui.costumwriteparameters import CostumWriteParameters

class MainWindow(QMainWindow):
    def __init__(self, ip_address):
        super().__init__()
        loadUi("C:/Workspace/festo-edcon/src/edcon/gui/mainwindow.ui", self)
        self.setWindowTitle("GUI")

        connection_widget = loadUi("C:/Workspace/festo-edcon/src/edcon/gui/connection.ui")
        connection_widget.ipAddressEdit.setText(ip_address)
        self.toolBar.addWidget(connection_widget)

        # self.toolBar.addWidget(connection_widget)
        # self.toolBar.addWidget(QLineEdit())
        # self.toolBar.addWidget(QLineEdit())
        # self.tabWidget.addTab(connection_widget, "Connection")
        

        # # Create a tab widget to hold the different pages
        # self.tabWidget = QTabWidget()
        # self.setCentralWidget(self.tabWidget)

        # # Create the configuration page
        # configuration_page = QWidget()
        # loadUi("C:/Workspace/festo-edcon/src/edcon/gui/configuration.ui", configuration_page)
        # self.tabWidget.addTab(configuration_page, "Configuration")

        # # Create a toolbar
        # toolbar = QToolBar()
        # self.addToolBar(toolbar)

        # toolbar2 = QToolBar()
        # self.addToolBar(toolbar2)

        # # Create a QWidget as a spacer for the layout
        # spacer = QWidget()
        # spacer.setFixedWidth(50)  # Set the width to half a centimeter

        # # Create a QLineEdit for the user to enter the IP address
        # txteditIP = QLineEdit()
        # txteditIP.setStyleSheet("QLineEdit{background-color:white; color:black;}")
        # txteditIP.setInputMask("000.000.000.000")
        # txteditIP.setFixedWidth(txteditIP.fontMetrics().boundingRect("000.000.000.0000").width())
        # txteditIP.setText(ip_address)  # Set the default value
        # toolbar.addWidget(txteditIP)
        # toolbar.addWidget(spacer)
        # # Create a QPushButton for the connect button
        # btnConnect = QPushButton("Connect")
        # btnConnect.setStyleSheet("QPushButton{background-color:rgb(0, 170, 255); color:white;}")
        # toolbar.addWidget(btnConnect)

        # # Create an instance of CustomConnection 
        # self.costum_connection = CostumConnection(txteditIP, btnConnect)

        # # Create an instance of CustomReadParameters
        # self.costum_read_parameters = CostumReadParameters(configuration_page.txtsearchParameter, txteditIP.text())

        # # Create an instance of CustomReadParameters
        # self.costum_write_parameters = CostumWriteParameters(configuration_page.txtValueParameter, txteditIP.text(), configuration_page.txtsearchParameter)