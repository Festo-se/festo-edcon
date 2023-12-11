
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox,QLineEdit
from edcon.edrive.com_modbus import ComModbus
from edcon.utils.logging import Logging

class CostumConnection(QWidget):
    def __init__(self, connection_page):
        super().__init__()

        # Access the btnconnect of the connection_page instance
        self.btnconnect = connection_page.findChild(QPushButton, "btnconnect")

        # Connect the button's click event to the function
        self.btnconnect.clicked.connect(self.connect_button_clicked)

        # Create a QLineEdit for the user to enter the IP address
        self.txteditIP = connection_page.findChild(QLineEdit, "txteditIP")

    def connect_button_clicked(self):
        
        # Enable loglevel info
        Logging()

        ip_address = self.txteditIP.text()  # Get the content of the QLineEdit txteditIP
        com = ComModbus(ip_address)  # Füge die IP-Adresse in "IP Adresse" bei comModbus ein

        # Establish the connection with the SPS
        if com.connected():
            QMessageBox.warning(self, "Connection Failed", "Failed to establish the connection.")
        else:
            QMessageBox.information(self, "Connection Successful", "Connection established!")


if __name__ == "__main__":
    app = QApplication([])
    connection_page = window.tabWidget.widget(0)  # Get the connection_page from MainWindow
    connection = CostumConnection(connection_page)
    connection.show()
    app.exec_()