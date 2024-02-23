"""Model for the parameter table widget."""

from dataclasses import dataclass, astuple, fields
from typing import Any
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from edcon.utils.logging import Logging
from edcon.edrive.parameter_mapping import read_pnu_map_file


@dataclass
class PnuDataItem:
    """Class representing a PNU data item."""

    pnu: int
    name: str
    data_type: str
    parameter_id: str
    value: Any


class ParameterTableModel(QtCore.QAbstractTableModel):
    """Defines the model for the parameter table."""

    def __init__(self):
        super().__init__()

        pnu_list = read_pnu_map_file()
        self._name_filter = ""
        self._headers = [field.name for field in fields(PnuDataItem)]

        self._data = [PnuDataItem(*pnu, "") for pnu in pnu_list]
        self._filtered_data = self._data

    def set_name_filter(self, name_filter):
        """uses name filter to filter the data

        Parameters:
            name_filter (str): string sequence used to filter the pnu names
        """
        self._name_filter = name_filter
        if self._name_filter == "":
            self._filtered_data = self._data
        self._filtered_data = [
            data for data in self._data if self._name_filter in data.name
        ]
        self.layoutChanged.emit()

    def update_all_values(self, pnu_read_func):
        """Fill the column "value" for all rows.

        Parameters:
            pnu_read_func (function): function to read a PNU
        """
        for data in self._filtered_data:
            try:
                data.value = pnu_read_func(data.pnu)
            except (ValueError, AttributeError):
                Logging.logger.error(f"Could not access PNU register {data.pnu}")

        self.layoutChanged.emit()

    def update_value(self, pnu, pnu_read_func):
        """Fill the column "value" for one row.

        Parameters:
            pnu (int): PNU id
            pnu_read_func (function): function to read a PNU

        Returns:
            list: updated data value or None
        """
        data = next((data for data in self._data if data.pnu == pnu), None)
        if data is None:
            Logging.logger.error(f"PNU {pnu} not in table")
            return None

        try:
            data.value = pnu_read_func(data.pnu)
        except (ValueError, AttributeError):
            Logging.logger.error(f"Could not access PNU register {data.pnu}")

        self.layoutChanged.emit()
        return data

    def data(self, index, role):
        """returns the cell value if the role is Qt.DisplayRole

        Parameters:
            index (QModelIndex): index of the cell
            role (Qt.DisplayRole): role of the cell

        Returns:
            Any: cell value
        """
        if role != Qt.DisplayRole:
            return None

        pnu_data_item = self._filtered_data[index.row()]
        return astuple(pnu_data_item)[index.column()]

    # pylint: disable=invalid-name, unused-argument
    # PyQt API naming
    def rowCount(self, index):
        """returns the number of rows.

        Parameters:
            index (QModelIndex): index of the cell

        Returns:
            int: number of rows
        """
        return len(self._filtered_data)

    # pylint: disable=invalid-name, unused-argument
    # PyQt API naming
    def columnCount(self, index):
        """returns the number of columns.

        Parameters:
            index (QModelIndex): index of the cell

        Returns:
            int: number of columns
        """
        return len(self._headers)

    # pylint: disable=invalid-name
    # PyQt API naming
    def headerData(self, section, orientation, role):
        """Used to provide data for the header rows

        Parameters:
            section (int): section
            orientation (Qt.Orientation): orientation
            role (Qt.DisplayRole): role

        Returns:
            Any: header value
        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self._headers[section]

        if orientation == Qt.Vertical:
            return str(section + 1)

        return None
