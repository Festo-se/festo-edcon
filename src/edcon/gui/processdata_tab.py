"""Setup code of the main window."""

from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from edcon.edrive.telegram1_handler import Telegram1Handler


class ProcessDataTab(QWidget):
    """Defines the main window."""

    def __init__(self, com):
        super().__init__()
        loadUi(PurePath(files("edcon") / "gui" / "ui" / "processdata_tab.ui"), self)
        
        self.com = com
        self.tg1 = Telegram1Handler(self.com)
        
        self.treeWidget.itemClicked.connect(self.on_item_clicked)
        self.treeWidget.itemChanged.connect(self.on_item_changed)  

    def on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Item click callback for invert boolean value 

        Parameters:
            item (QTreeWidgetItem): item from treewidget
            column (int): column from treewidget
        """
        # Check if the clicked item is an attribute of "stw1"
        if item.parent() and item.parent().text(0) == "Control word (STW1)" and column == 0:
            current_value = item.data(0, Qt.CheckStateRole)
            new_value = not current_value
            item.setData(0, Qt.CheckStateRole, new_value)
            item.setText(0, f"{item.text(0).split(':')[0]}: {new_value}")
            
            attribute_names = ['on', 'no_coast_stop', 'no_quick_stop', 'enable_operation', 
                               'enable_ramp_generator', 'unfreeze_ramp_generator', 'setpoint_enable', 
                               'fault_ack', 'jog1_on', 'jog2_on', 'control_by_plc', 'invert_setpoint', 
                               'open_holding_brake', 'motor_pot_increase', 'motor_pot_decrease', 'reserved1']
            
            position = item.parent().indexOfChild(item)
            attribute_name = attribute_names[position]

            # Update the corresponding attribute in "stw1"
            setattr(self.tg1.telegram.stw1, attribute_name, new_value)
            print(bin(int(self.tg1.telegram.stw1))[2:].zfill(16)) #test
        
        if item.parent() and item.parent().text(0) == "Status word (ZSW1)" and column == 0:
            current_value = item.data(0, Qt.CheckStateRole)
            new_value = not current_value
            item.setData(0, Qt.CheckStateRole, new_value)
            item.setText(0, f"{item.text(0).split(':')[0]}: {new_value}")

            attribute_names = ['ready_to_switch_on', 'ready_to_operate', 'operation_enabled', 'fault_present', 
                               'coast_stop_not_activated', 'quick_stop_not_activated', 'switching_on_inhibited', 
                               'warning_present', 'speed_error_within_tolerance_range', 'control_requested', 
                               'f_or_n_reached_or_exceeded', 'im_or_p_not_reached', 
                               'holding_break_released', 'motor_temp_warning_inactive', 'positive_direction_rotation', 
                               'ps_temp_warning_inactive']
            
            position = item.parent().indexOfChild(item)
            attribute_name = attribute_names[position]

            # Update the corresponding attribute in "stw1"
            setattr(self.tg1.telegram.zsw1, attribute_name, new_value)
            print(bin(int(self.tg1.telegram.zsw1))[2:].zfill(16)) #test
    
    def on_item_changed(self, item, column):
        """Item changed callback for write new value

        Parameters:
            item (QTreeWidgetItem): item from treewidget
            column (int): column from treewidget
        """  
        if item.parent() and item.parent().text(0) == "NSOLL-A" and column == 0:
            try:
                value = int(item.text(column))
                self.tg1.telegram.nsoll_a.value = value
                print(self.tg1.telegram.nsoll_a) #test

            except ValueError:
                pass
            
        if item.parent() and item.parent().text(0) == "NIST-A" and column == 0:
            try:
                value = int(item.text(column))
                self.tg1.telegram.nist_a.value = value
                print(self.tg1.telegram.nist_a) #test

            except ValueError:
                pass
