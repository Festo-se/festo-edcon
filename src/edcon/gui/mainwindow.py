from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from importlib.resources import files
from pathlib import PurePath
from edcon.gui.costumconnection import CostumConnection
from edcon.gui.costumreadparameters import CostumReadParameters
from edcon.gui.costumwriteparameters import CostumWriteParameters
from edcon.gui.costumtablemodel import CostumTableModel
class MainWindow(QMainWindow):
    def __init__(self, ip_address):
        super().__init__()
        loadUi(PurePath(files('edcon') / 'gui' / 'mainwindow.ui'), self)
        self.setWindowTitle("GUI")

        self.connection_widget = loadUi(PurePath(files('edcon') / 'gui' / 'connection.ui'))
        self.connection_widget.txteditIP.setText(ip_address)
        self.toolBar.addWidget(self.connection_widget)

          # # Create an instance of CustomConnection 
        self.costum_connection = CostumConnection(self.connection_widget.txteditIP, self.connection_widget.btnConnect)

        # Create an instance of CustomReadParameters
        self.costum_read_parameters = CostumReadParameters(self.txtsearchParameter, self.costum_connection)

        # Create an instance of CustomWriteParameters
        self.costum_write_parameters = CostumWriteParameters(self.txtValueParameter, self.costum_connection, self.txtsearchParameter)

        # Create an instance of CostumTableCsv
        csv_file_path = PurePath(files('edcon') / 'edrive' / 'data'/ 'pnu_map.csv')
        self.model = CostumTableModel(csv_file_path, self.costum_connection)

        self.btnUpdate.clicked.connect(self.btnUpdate_clicked)
        self.btnConfirmValue.clicked.connect(self.btnConfirm_clicked)
        self.btnReadValue.clicked.connect(self.btnRead_clicked)
        self.tblPnuList.setModel(self.model)
        self.txtsearchPnuList.textChanged.connect(self.on_textChanged)
        self.txtValueParameter.returnPressed.connect(self.pressedEnter_value)
        self.txtsearchParameter.returnPressed.connect(self.pressedEnter_read)

    def on_textChanged(self, text):
        self.model.setNameFilter(text)
        self.tblPnuList.model().layoutChanged.emit()
        
    def btnUpdate_clicked(self):
        self.model.setPnuForAllRows()
    
    def btnConfirm_clicked(self):
        try:
          self.costum_write_parameters.write_pnu_value_from_text()
          self.model.setValueForOneRow(self.txtsearchParameter.text())
        except Exception as e:
            print("failed")

    def btnRead_clicked(self):
        try:
          self.costum_read_parameters.read_pnu_from_text()
        except Exception as e:
            print("failed")


    def pressedEnter_read(self):
        try:
          self.costum_read_parameters.read_pnu_from_text()
        except Exception as e:
            print("failed")

    def pressedEnter_value(self):
        try:
          self.costum_write_parameters.write_pnu_value_from_text()
          self.model.setValueForOneRow(self.txtsearchParameter.text())
        except Exception as e:
            print("failed")