from PyQt5.QtWidgets import QMessageBox
from edcon.edrive.com_modbus import ComModbus

class CostumWriteParameters:
    def __init__(self, txtValueParameter, costumconnection, txtsearchParameter):

        self.txtValueParameter = txtValueParameter
        self.txtsearchParameter = txtsearchParameter
        self.costumconnection = costumconnection

    def write_pnu_value_from_text(self):
        new_value = self.txtValueParameter.text()
        pnu = int(self.txtsearchParameter.text())  # Convert pnu to an integer
    
        try:
            self.costumconnection.com.write_pnu(pnu,0,new_value)
            # Do something with the result, such as displaying it in a QMessageBox
            QMessageBox.information(self.txtValueParameter.parent(), "Write PNU successfull", f"The value {new_value} is written in: {pnu}")
        except Exception as e:
            QMessageBox.warning(self.txtValueParameter.parent(), "Write PNU Failed", f"Failed to write PNU {new_value}: {str(e)}")

