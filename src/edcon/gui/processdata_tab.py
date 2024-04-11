from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
from dataclasses import fields
from PyQt5.QtWidgets import QWidget,QHeaderView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt,QTimer
from PyQt5.uic import loadUi
from edcon.edrive.telegram1_handler import Telegram1Handler
from edcon.edrive.telegram9_handler import Telegram9Handler
from edcon.edrive.telegram102_handler import Telegram102Handler
from edcon.edrive.telegram111_handler import Telegram111Handler
from edcon.utils.logging import Logging
from edcon.profidrive.words import BitwiseWord

class ProcessDataTab(QWidget):
    """Defines the main window."""

    def __init__(self, get_com_function):
        super().__init__()
        loadUi(PurePath(files("edcon") / "gui" / "ui" / "processdata_tab.ui"), self)
        self.get_com_function = get_com_function    
        self.tgh = None

        self.model = QStandardItemModel()
        self.treeView.setModel(self.model)

        self.comboBox.currentIndexChanged.connect(self.select_telegramhandler)
        self.treeView.clicked.connect(self.on_item_clicked)
        self.model.dataChanged.connect(self.on_item_changed)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_outputs_gui)
        self.timer.start(100)

    def select_telegramhandler(self):
        """Select a Telegram handler from the combobox."""
        selected_view = self.comboBox.currentIndex() 

        if self.tgh is not None:
            self.tgh.shutdown()
            self.tgh = None

        if selected_view == 0:
            self.model.clear()
            self.tgh = None

        elif selected_view == 1:
            self.model.clear()
            com = self.get_com_function()
            com.write_pnu(3490, value=1)
            self.tgh = Telegram1Handler(com)
            self.generate_treeview()

        elif selected_view == 2:
            self.model.clear()
            com = self.get_com_function()
            com.write_pnu(3490, value=9)
            self.tgh = Telegram9Handler(com)
            self.generate_treeview()
        
        elif selected_view == 3:
            self.model.clear()
            com = self.get_com_function()
            com.write_pnu(3490, value=102)
            self.tgh = Telegram102Handler(com)
            self.generate_treeview()

        elif selected_view == 4:
            self.model.clear()
            com = self.get_com_function()
            com.write_pnu(3490, value=111)
            self.tgh = Telegram111Handler(com)
            self.generate_treeview()

    def generate_treeview(self):
        """Generates a Treeview using the respective Telegram handler"""
        self.tgh.update_io()
        in_and_outputs = [x.name for x in fields(self.tgh.telegram)]
        root = QStandardItem("Inputs")
        root.setFlags(Qt.NoItemFlags)
        self.model.appendRow(root)
        self.treeView.setHeaderHidden(True)
        self.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.model.setColumnCount(2)

        for name in in_and_outputs:
            inputs = self.tgh.telegram.outputs()

            if getattr(self.tgh.telegram,name) in inputs:
                item = QStandardItem(name)
                item.setFlags(Qt.NoItemFlags)
                root.appendRow(item)
                attribute_name_list = [x.name for x in fields(getattr(self.tgh.telegram, name))]

                if isinstance(getattr(self.tgh.telegram, item.text()),BitwiseWord) == True:

                    for attribute_name in attribute_name_list:
                        attribute_item = QStandardItem(f"{attribute_name}")
                        attribute_item.setFlags(Qt.ItemIsUserCheckable)
                        attribute_item.setCheckable(True)
                        attribute_item.setCheckState(Qt.PartiallyChecked if getattr(getattr(self.tgh.telegram, name), attribute_name) else Qt.Unchecked)
                        item.appendRow(attribute_item)
                else:

                    for attribute_name in attribute_name_list:

                        if attribute_name != "byte_size":
                            attribute_value = getattr(getattr(self.tgh.telegram, name), attribute_name)
                            attribute_name_item = QStandardItem(f"{attribute_name}:")
                            attribute_name_item.setFlags(Qt.NoItemFlags)
                            attribute_value_item = QStandardItem(f"{str(attribute_value)}")
                            attribute_value_item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
                            item.appendRow([attribute_name_item, attribute_value_item])

        root = QStandardItem("Outputs")
        root.setFlags(Qt.NoItemFlags)
        self.model.appendRow(root)

        for name in in_and_outputs:
            outputs = self.tgh.telegram.inputs()
                
            if getattr(self.tgh.telegram,name) in outputs:
                item = QStandardItem(name)
                item.setFlags(Qt.NoItemFlags)
                root.appendRow(item)
                attribute_name_list = [x.name for x in fields(getattr(self.tgh.telegram, name))]

                for attribute_name in attribute_name_list:

                    if isinstance(getattr(self.tgh.telegram, item.text()),BitwiseWord) == True:
                        attribute_item = QStandardItem(f"{attribute_name}")
                        attribute_item.setFlags(Qt.ItemIsUserCheckable)
                        attribute_item.setCheckable(True)
                        attribute_item.setCheckState(Qt.PartiallyChecked if getattr(getattr(self.tgh.telegram, name), attribute_name) else Qt.Unchecked)
                        attribute_item.setFlags(Qt.NoItemFlags)
                        item.appendRow(attribute_item)

                    elif attribute_name != "byte_size":
                        attribute_value = getattr(getattr(self.tgh.telegram, name), attribute_name)
                        attribute_name_item = QStandardItem(f"{attribute_name}:")
                        attribute_name_item.setFlags(Qt.NoItemFlags)
                        attribute_value_item = QStandardItem(f"{str(attribute_value)}")
                        attribute_value_item.setFlags(Qt.NoItemFlags)
                        item.appendRow([attribute_name_item, attribute_value_item])

    def update_outputs_gui(self):
        """Updates the treeview content"""
        if self.tgh is None:
            return
        
        outputs_root_index = self.model.index(1, 0)
        self.tgh.update_io()
                
        for row in range(self.model.rowCount(outputs_root_index)):
            output_item_index = self.model.index(row, 0, outputs_root_index)  
            output_item = self.model.itemFromIndex(output_item_index)  
            j = 16

            for child_row in range(output_item.rowCount()):
                child_item = output_item.child(child_row)
                text = child_item.text()
                name = text.split(":")[0]
                j = j - 1

                if isinstance(getattr(self.tgh.telegram, output_item.text()),BitwiseWord) == True:
                    
                    if bin(int(getattr(self.tgh.telegram,output_item.text())))[2:].zfill(16)[j] == "1":
                        child_item.setText(f"{name}")
                        child_item.setCheckState(Qt.PartiallyChecked)
                    else:
                        child_item.setText(f"{name}")
                        child_item.setCheckState(Qt.Unchecked)
                else: 
                    child_item.setText(f"{name}:")
                    child_item2 = child_item.parent().child(child_item.row(), 1)
                    child_item2.setText(f"{getattr(getattr(self.tgh.telegram, output_item.text()), name)}")

        self.treeView.viewport().update()

    def on_item_clicked(self, index):
        """Item click callback for handling item click events

        Parameters:
            index (QModelIndex): Index of the clicked item
        """
        inputs_root_index = self.model.index(0, 0)
        parent_index = index.parent()
        grandparent_index = parent_index.parent()
    
        if grandparent_index == inputs_root_index:
            item = self.treeView.model().itemFromIndex(index)
            attribute_name = item.parent().text()
            child_attribute_name = item.text().split(":")[0].strip()

            if isinstance(getattr(self.tgh.telegram, item.parent().text()),BitwiseWord) == True:
                current_value = getattr(getattr(self.tgh.telegram, attribute_name), child_attribute_name)
                new_value = not current_value
                setattr(getattr(self.tgh.telegram, attribute_name), child_attribute_name, new_value)
                Logging.logger.info(f"Attribute '{attribute_name}.{child_attribute_name}' value changed to: {new_value}")
                self.tgh.update_io()
                item.setText(f"{child_attribute_name}")
                item.setCheckState(Qt.PartiallyChecked if new_value else Qt.Unchecked)
    
    def on_item_changed(self, index):
        """Item changed callback for handling item changed events

        Parameters:
            index (QModelIndex): Index of the changed item
        """
        inputs_root_index = self.model.index(0, 0)
        item = self.treeView.model().itemFromIndex(index)
        attribute_name = item.parent().text()
        current_value = item.text()
        child_attribute_name = "value"

        if inputs_root_index == item.parent().parent().index():

            if isinstance(getattr(self.tgh.telegram, item.parent().text()),BitwiseWord) == False:
                setattr(getattr(self.tgh.telegram, attribute_name), child_attribute_name, int(current_value))
                Logging.logger.info(f"Attribute '{attribute_name}.{child_attribute_name}' value changed to: {current_value}")
                self.tgh.update_io()
