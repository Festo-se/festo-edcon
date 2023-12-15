from PyQt5.QtWidgets import QMessageBox
from edcon.edrive.com_modbus import ComModbus

class CostumReadParameters:
    def __init__(self, txtsearchParameter, costumconnection):
        self.costumconnection = costumconnection
        self.txtsearchParameter = txtsearchParameter

    def read_pnu_from_text(self):
        pnu = int(self.txtsearchParameter.text())  # Convert pnu to an integer
        try:
            result = self.costumconnection.com.read_pnu(pnu, 0)
            # Do something with the result, such as displaying it in a QMessageBox
            QMessageBox.information(self.txtsearchParameter.parent(), "Read PNU Result", f"The result for PNU {pnu} is: {result}")
        except Exception as e:
            QMessageBox.warning(self.txtsearchParameter.parent(), "Read PNU Failed", f"Failed to read PNU {pnu}: {str(e)}")