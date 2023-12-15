"""Model for the parameter table widget."""

import csv
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class ParameterTableModel(QtCore.QAbstractTableModel):
    """Defines the model for the parameter table."""

    def __init__(self, csv_file_path, connection_widget):
        super().__init__()
        self.connection_widget = connection_widget

        self.name_filter = ''
        with open(csv_file_path, encoding='ascii') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            self._headers = next(reader, None) + ['value']
            self._data = [line + [''] for line in list(reader)]
            self._filtered_data = self._data

    def set_name_filter(self, name_filter):
        """takes input from line edit and filter table widget"""
        self.name_filter = name_filter
        if name_filter == '':
            self._filtered_data = self._data
        self._filtered_data = [
            line for line in self._data if name_filter in line[1]]

    def set_pnu_for_all_rows(self):
        """Fill the column "value" for all rows."""
        pnu_list = [row[0] for row in self._data]
        for pnu in pnu_list:
            self.set_value_for_one_row(pnu)

    def set_value_for_one_row(self, pnu):
        """Fill the column "value" for one row."""
        try:
            # Execute the command with the current pnu value
            value = self.connection_widget.com.read_pnu(int(pnu), 0)
            index = [row[0] for row in self._data].index(str(pnu))
            self._data[index][4] = value

        except (ValueError, AttributeError):
            pass

    def data(self, index, role):
        """returns the cell value if the role is "Qt.DisplayRole"""
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self._filtered_data[row][column]
        return None

    # pylint: disable=invalid-name, unused-argument
    # PyQt API naming
    def rowCount(self, index):
        """returns the number of rows."""
        return len(self._filtered_data)

    # pylint: disable=invalid-name, unused-argument
    # PyQt API naming
    def columnCount(self, index):
        """returns the number of columns."""
        return len(self._headers)

    # pylint: disable=invalid-name
    # PyQt API naming
    def headerData(self, section, orientation, role):
        """Used to provide data for the header rows"""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section + 1)
        return None
