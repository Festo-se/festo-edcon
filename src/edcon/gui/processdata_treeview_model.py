# pylint: disable=import-error, no-name-in-module
from dataclasses import fields
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt, QTimer
from edcon.utils.logging import Logging
from edcon.profidrive.words import BitwiseWord


class ProcessDataTreeViewModel(QStandardItemModel):
    """Defines the main window."""

    def __init__(self, tgh):
        super().__init__()
        if tgh is None:
            raise ValueError("tgh cannot be None")

        self.tgh = tgh
        self.setColumnCount(2)
        self.dataChanged.connect(self.on_item_changed)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_inputs_gui)
        self.timer.start(100)

        self.generate_treeview()

    def clear(self):
        super().clear()
        self.timer.stop()
        self.tgh.shutdown()
        self.tgh = None

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

    def is_bitwise_word(self, word_name):
        return isinstance(getattr(self.tgh.telegram, word_name), BitwiseWord)

    def append_bitwise_word_item(self, root, name, value, readonly=False):
        item = QStandardItem(f"{name}")
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setUserTristate(True)
        item.setCheckState(Qt.PartiallyChecked if value else Qt.Unchecked)
        if readonly:
            item.setCheckable(False)
        root.appendRow(item)

    def append_value_word_item(self, root, name, value, readonly=False):
        item = QStandardItem(f"{name}:")
        item.setFlags(Qt.NoItemFlags)
        value_item = QStandardItem(f"{str(value)}")
        if readonly:
            value_item.setFlags(Qt.NoItemFlags)
        root.appendRow([item, value_item])

    def append_word_item(self, root, name, readonly=False):
        word_item = QStandardItem(name)
        word_item.setFlags(Qt.NoItemFlags)
        root.appendRow(word_item)
        word = getattr(self.tgh.telegram, name)
        item_name_list = [x.name for x in fields(word)]

        for item_name in item_name_list:
            item_value = getattr(word, item_name)
            if self.is_bitwise_word(name):
                self.append_bitwise_word_item(
                    word_item, item_name, item_value, readonly
                )
            else:
                # Skip byte_size field
                if item_name == "byte_size":
                    continue
                self.append_value_word_item(word_item, item_name, item_value, readonly)

    def generate_treeview(self):
        """Generates a Treeview using the respective Telegram handler"""

        self.output_root_item = QStandardItem("Outputs")
        self.output_root_item.setFlags(Qt.NoItemFlags)
        self.appendRow(self.output_root_item)
        for name in self.output_word_names():
            self.append_word_item(self.output_root_item, name)

        self.input_root_item = QStandardItem("Inputs")
        self.input_root_item.setFlags(Qt.NoItemFlags)
        self.appendRow(self.input_root_item)
        for name in self.input_word_names():
            self.append_word_item(self.input_root_item, name, readonly=True)

        self.layoutChanged.emit()

    def update_inputs_gui(self):
        """Updates the treeview content"""
        self.tgh.update_inputs()

        input_word_items = [
            self.input_root_item.child(idx)
            for idx in range(self.input_root_item.rowCount())
        ]

        for word_item in input_word_items:
            input_items = [word_item.child(row) for row in range(word_item.rowCount())]
            for item in input_items:
                word_name = word_item.text()
                word = getattr(self.tgh.telegram, word_name)
                if self.is_bitwise_word(word_name):
                    item_value = getattr(word, item.text())
                    if item_value:
                        item.setCheckState(Qt.PartiallyChecked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                else:
                    item_value = getattr(word, "value")
                    input_value = item.parent().child(item.row(), 1)
                    input_value.setText(f"{item_value}")
        self.layoutChanged.emit()

    def on_item_changed(self, index):
        """Item changed callback for handling item changed events

        Parameters:
            index (QModelIndex): Index of the item that changed
        """
        # Ignore if item is not a child of Outputs
        if index.parent().parent() != self.output_root_item.index():
            return

        item = self.itemFromIndex(index)

        # True if PartiallyChecked, False otherwise
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
            return

        word_name = item.parent().text()
        word = getattr(self.tgh.telegram, word_name)
        if self.is_bitwise_word(word_name):
            item_name = item.text()
            new_value = item.checkState() != Qt.Unchecked
        else:
            item_name = "value"
            new_value = int(item.text())

        setattr(word, item_name, new_value)
        Logging.logger.info(
            f"Attribute '{word_name}.{item_name}' value changed to: {new_value}"
        )
        self.tgh.update_outputs()
