from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
from dataclasses import fields
from PyQt5.QtWidgets import QWidget, QHeaderView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt, QTimer
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
        self.timer.timeout.connect(self.update_inputs_gui)
        self.timer.start(100)

    def select_telegramhandler(self):
        """Select a Telegram handler from the combobox."""
        selected_item_name = self.comboBox.currentText()

        if self.tgh is not None:
            self.tgh.shutdown()
            self.tgh = None

        if selected_item_name == "None":
            self.model.clear()
            self.tgh = None

        elif selected_item_name == "Telegram1":
            self.model.clear()
            com = self.get_com_function()
            com.write_pnu(3490, value=1)
            self.tgh = Telegram1Handler(com)
            self.generate_treeview()

        elif selected_item_name == "Telegram9":
            self.model.clear()
            com = self.get_com_function()
            com.write_pnu(3490, value=9)
            self.tgh = Telegram9Handler(com)
            self.generate_treeview()

        elif selected_item_name == "Telegram102":
            self.model.clear()
            com = self.get_com_function()
            com.write_pnu(3490, value=102)
            self.tgh = Telegram102Handler(com)
            self.generate_treeview()

        elif selected_item_name == "Telegram111":
            self.model.clear()
            com = self.get_com_function()
            com.write_pnu(3490, value=111)
            self.tgh = Telegram111Handler(com)
            self.generate_treeview()

    def output_word_names(self):
        in_and_outputs = [x.name for x in fields(self.tgh.telegram)]
        return [
            x
            for x in in_and_outputs
            if getattr(self.tgh.telegram, x) in self.tgh.telegram.outputs()
        ]

    def input_word_names(self):
        in_and_outputs = [x.name for x in fields(self.tgh.telegram)]
        return [
            x
            for x in in_and_outputs
            if getattr(self.tgh.telegram, x) in self.tgh.telegram.inputs()
        ]

    def is_bitwise_word(self, name):
        return isinstance(getattr(self.tgh.telegram, name), BitwiseWord)

    def append_word_item(self, root, name, readonly=False):
        item = QStandardItem(name)
        item.setFlags(Qt.NoItemFlags)
        root.appendRow(item)
        attribute_name_list = [x.name for x in fields(getattr(self.tgh.telegram, name))]

        for attribute_name in attribute_name_list:
            if self.is_bitwise_word(item.text()):
                attribute_item = QStandardItem(f"{attribute_name}")
                attribute_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                attribute_item.setCheckable(False)
                attribute_item.setCheckState(
                    Qt.PartiallyChecked
                    if getattr(getattr(self.tgh.telegram, name), attribute_name)
                    else Qt.Unchecked
                )
                item.appendRow(attribute_item)
            else:
                if attribute_name == "byte_size":
                    continue
                attribute_value = getattr(
                    getattr(self.tgh.telegram, name), attribute_name
                )
                attribute_name_item = QStandardItem(f"{attribute_name}:")
                attribute_name_item.setFlags(Qt.NoItemFlags)
                attribute_value_item = QStandardItem(f"{str(attribute_value)}")
                if readonly:
                    attribute_value_item.setFlags(Qt.NoItemFlags)
                item.appendRow([attribute_name_item, attribute_value_item])

    def generate_treeview(self):
        """Generates a Treeview using the respective Telegram handler"""
        self.model.setColumnCount(2)
        self.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        root = QStandardItem("Outputs")
        root.setFlags(Qt.NoItemFlags)
        self.model.appendRow(root)
        for name in self.output_word_names():
            self.append_word_item(root, name)

        root = QStandardItem("Inputs")
        root.setFlags(Qt.NoItemFlags)
        self.model.appendRow(root)
        for name in self.input_word_names():
            self.append_word_item(root, name, readonly=True)

    def update_inputs_gui(self):
        """Updates the treeview content"""
        if self.tgh is None:
            return
        self.tgh.update_inputs()

        root_index = self.model.index(1, 0)

        for row in range(self.model.rowCount(root_index)):
            output_item_index = self.model.index(row, 0, root_index)
            output_item = self.model.itemFromIndex(output_item_index)
            j = 16

            for child_row in range(output_item.rowCount()):
                child_item = output_item.child(child_row)
                text = child_item.text()
                name = text.split(":")[0]
                j = j - 1

                if (
                    isinstance(
                        getattr(self.tgh.telegram, output_item.text()), BitwiseWord
                    )
                    == True
                ):

                    if (
                        bin(int(getattr(self.tgh.telegram, output_item.text())))[
                            2:
                        ].zfill(16)[j]
                        == "1"
                    ):
                        child_item.setText(f"{name}")
                        child_item.setCheckState(Qt.PartiallyChecked)
                    else:
                        child_item.setText(f"{name}")
                        child_item.setCheckState(Qt.Unchecked)
                else:
                    child_item.setText(f"{name}:")
                    child_item2 = child_item.parent().child(child_item.row(), 1)
                    child_item2.setText(
                        f"{getattr(getattr(self.tgh.telegram, output_item.text()), name)}"
                    )

        self.treeView.viewport().update()

    def on_item_clicked(self, index):
        root_index = self.model.index(0, 0)
        if root_index == index.parent().parent():
            item = self.treeView.model().itemFromIndex(index)
            attribute_name = item.parent().text()
            if self.is_bitwise_word(attribute_name):
                item.setCheckState(not item.checkState())

    def on_item_changed(self, index):
        """Item changed callback for handling item changed events

        Parameters:
            index (QModelIndex): Index of the item that changed
        """
        root_index = self.model.index(0, 0)
        if root_index == index.parent().parent():
            item = self.treeView.model().itemFromIndex(index)
            attribute_name = item.parent().text()
            if self.is_bitwise_word(attribute_name):
                child_attribute_name = item.text()
                new_value = not getattr(
                    getattr(self.tgh.telegram, attribute_name), child_attribute_name
                )
            else:
                child_attribute_name = "value"
                new_value = int(item.text())
            setattr(
                getattr(self.tgh.telegram, attribute_name),
                child_attribute_name,
                new_value,
            )
            Logging.logger.info(
                f"Attribute '{attribute_name}.{child_attribute_name}' value changed to: {new_value}"
            )
            self.tgh.update_outputs()
