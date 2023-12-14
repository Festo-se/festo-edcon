import csv
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class CostumTableModel(QtCore.QAbstractTableModel):
    def __init__(self, file_path):
        super(CostumTableModel, self).__init__()

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

    def setValue(self, pnu, value):
        index = [row[0] for row in self._data].index(pnu)
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
    