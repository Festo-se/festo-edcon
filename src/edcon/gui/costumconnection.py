from PyQt5.QtWidgets import QWidget, QMessageBox
from edcon.edrive.com_modbus import ComModbus
from edcon.utils.logging import Logging

class CostumConnection(QWidget):
    com = None  # Class attribute to store the ComModbus object

    def __init__(self, txteditIP, btnConnect):
        super().__init__()

        # Connect the button's clicked signal to the function
        btnConnect.clicked.connect(self.connect_button_clicked)

        # Store the QLineEdit and QPushButton for future use
        self.txteditIP = txteditIP
        self.btnConnect = btnConnect

    def connect_button_clicked(self):
        # Enable loglevel info
        Logging()

        ip_address = self.txteditIP.text()  # Get the content of the QLineEdit txteditIP

        # Establish the connection with the SPS
        try:
            self.com = ComModbus(ip_address, timeout_ms = 0 )  # Füge die IP-Adresse in "IP Adresse" bei comModbus ein
            self.com.read_pnu(1)
        except Exception as e:
            QMessageBox.warning(self, "Connection Failed", f"Failed to establish the connection: {str(e)}")
            return

        QMessageBox.information(self, "Connection Successful", "Connection established!")
        # Replace the "Connect" button with a "Disconnect" button
        self.btnConnect.setText("Disconnect")
        self.btnConnect.clicked.disconnect()  # Disconnect the previous signal-slot connection
        self.btnConnect.clicked.connect(self.disconnect_button_clicked)  # Connect the new signal-slot connection

    def disconnect_button_clicked(self):
        if self.com is not None:
            # Perform the disconnection
            self.com = None  # Reset the com variable

        # Replace the "Disconnect" button with a "Connect" button
        self.btnConnect.setText("Connect")
        self.btnConnect.clicked.disconnect()  # Disconnect the previous signal-slot connection
        self.btnConnect.clicked.connect(self.connect_button_clicked)  # Connect the new signal-slot connections