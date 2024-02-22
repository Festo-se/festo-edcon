"""Model for the parameter table widget."""

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from edcon.utils.logging import Logging
from edcon.edrive.parameter_mapping import read_pnu_map_file


class ParameterTableModel(QtCore.QAbstractTableModel):
    """Defines the model for the parameter table."""

    def __init__(self):
        super().__init__()

        pnu_list = read_pnu_map_file()
        self._name_filter = ""
        self._headers = [*pnu_list[0]._fields] + ["value"]
        self._data = [[*pnu, ""] for pnu in pnu_list]
        self._filtered_data = self._data

    def set_name_filter(self, name_filter):
        """uses name filter to filter the data"""
        self._name_filter = name_filter
        if self._name_filter == "":
            self._filtered_data = self._data
        self._filtered_data = [
            data for data in self._data if self._name_filter in data[1]
        ]
        self.layoutChanged.emit()

    def update_all_values(self, pnu_read_func):
        """Fill the column "value" for all rows."""
        for data in self._filtered_data:
            try:
                data[4] = pnu_read_func(data[0])
            except (ValueError, AttributeError):
                Logging.logger.error(f"Could not access PNU register {data[0]}")
        self.layoutChanged.emit()

    def update_value(self, pnu, pnu_read_func):
        """Fill the column "value" for one row."""
        data = next((data for data in self._data if data[0] == int(pnu)), None)
        if data is None:
            Logging.logger.error(f"PNU {pnu} not in table")
            return

        try:
            data[4] = pnu_read_func(data[0])
        except (ValueError, AttributeError):
            Logging.logger.error(f"Could not access PNU register {pnu}")
        self.layoutChanged.emit()

    def data(self, index, role):
        """returns the cell value if the role is "Qt.DisplayRole"""
        if role != Qt.DisplayRole:
            return None

        return self._filtered_data[index.row()][index.column()]

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
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self._headers[section]

        if orientation == Qt.Vertical:
            return str(section + 1)

        return None
