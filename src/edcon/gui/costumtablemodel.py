from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class CostumTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(CostumTableModel, self).__init__()

        self._headers = data[0]
        self._data = data[1:]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self._data[row][column]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]

        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section + 1)

        return None
    