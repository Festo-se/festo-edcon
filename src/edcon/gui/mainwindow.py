from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from importlib.resources import files
from pathlib import PurePath
from edcon.gui.costumconnection import CostumConnection
from edcon.gui.costumreadparameters import CostumReadParameters
from edcon.gui.costumwriteparameters import CostumWriteParameters
from edcon.gui.costumtablecsv import CostumTableCsv
class MainWindow(QMainWindow):
    def __init__(self, ip_address):
        super().__init__()
        loadUi(PurePath(files('edcon') / 'gui' / 'mainwindow.ui'), self)
        self.setWindowTitle("GUI")

        connection_widget = loadUi(PurePath(files('edcon') / 'gui' / 'connection.ui'))
        #connection_widget.txteditIP.setText(ip_address)
        self.toolBar.addWidget(connection_widget)

          # # Create an instance of CustomConnection 
        self.costum_connection = CostumConnection(connection_widget.txteditIP, connection_widget.btnConnect)

        # Create an instance of CustomReadParameters
        self.costum_read_parameters = CostumReadParameters(self.txtsearchParameter, connection_widget.txteditIP.text())

        # Create an instance of CustomWriteParameters
        self.costum_write_parameters = CostumWriteParameters(self.txtValueParameter, connection_widget.txteditIP.text(), self.txtsearchParameter)

        # Create an instance of CostumTableCsv
        csv_file_path = PurePath(files('edcon') / 'edrive' / 'data'/ 'pnu_map.csv')
        self.costum_table_csv = CostumTableCsv(csv_file_path,self.tblPnuList)

  