"""Setup code of the main window."""

from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from edcon.utils.logging import Logging
from edcon.gui.pyqt_helpers import bold_string


# Enable loglevel info
Logging()


class DeviceConfigurationTab(QWidget):
    """Defines the main window."""

    def __init__(self, motion_tab, get_com_function):
        super().__init__()
        loadUi(
            PurePath(files("edcon") / "gui" / "ui" / "device_configuration_tab.ui"),
            self,
        )
        self.motion_tab = motion_tab
        self.get_com_function = get_com_function

        self.line_edit_position_unit.textChanged.connect(self.change_position_unit)
        self.line_edit_velocity_unit.textChanged.connect(self.change_velocity_unit)

    def change_position_unit(self):
        # com = self.get_com_function()
        # position_unit = self.line_edit_position_unit.text()
        # if position_unit is not None:
        #     #self.motion_tab.position_unit = 10 ** int(position_unit)
        #     com.write_pnu(11724, 0, (-1 * int(position_unit)))
        None

    def change_velocity_unit(self):
        # com = self.get_com_function()
        # velocity_unit = self.line_edit_velocity_unit.text()
        # if velocity_unit is not None:
        #     #self.motion_tab.velocity_unit = 10 ** int(velocity_unit)
        #     com.write_pnu(11725, 0, (-1 * int(velocity_unit)))
        None
