import csv
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from edcon.edrive.com_modbus import ComModbus
class CostumTableModel(QtCore.QAbstractTableModel):
    def __init__(self, file_path, costumconnection):
        super(CostumTableModel, self).__init__()
        self.costumconnection = costumconnection

        with open(file_path, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            self._headers = next(reader, None) + ['value']
            self._data = [line + [''] for line in list(reader)]
            self._filtered_data = self._data

    def setNameFilter(self, name_filter):
        self.name_filter = name_filter
        if name_filter == '':
            self._filtered_data = self._data
        self._filtered_data = [line for line in self._data if name_filter in line[1]]
    
    def setPnuForAllRows(self):
        pnu_list = [row[0] for row in self._data]
        for pnu in pnu_list:
            self.setValueForOneRow(pnu)

    def setValueForOneRow(self, pnu):
        #print(pnu)
        pnu_for_Modbus = int(pnu)
        pnu_for_Index = str(pnu)
        try:
            pnu = int(pnu)
            value = self.costumconnection.com.read_pnu(pnu_for_Modbus, 0)  # Execute the command with the current pnu value
        except Exception as e:
            print("Fehler beim Lesen des PNU:", str(e))
            value = None  # Set the result to None if an error occurs

        index = [row[0] for row in self._data].index(pnu_for_Index)
        self._data[index][4] = value

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self._filtered_data[row][column]

    def rowCount(self, index):
        return len(self._filtered_data)

    def columnCount(self, index):   
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section + 1)
        return None
    