"""Model for the processdata."""

from dataclasses import fields
from enum import Enum

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt

from edcon.utils.logging import Logging
from edcon.profidrive.words import BitwiseWord


class BasicState(Enum):
    SWITCHING_ON_INHIBITED = 0
    READY_FOR_SWITCHING_ON = 1
    SWITCHED_ON = 2
    OPERATION = 3
    UNDEFINED = 7


class ProcessDataModel(QStandardItemModel):
    """Defines the process data model."""

    def __init__(self, tgh):
        super().__init__()
        if tgh is None:
            raise ValueError("tgh cannot be None")

        self.setColumnCount(3)
        self.tgh = tgh
        self.dataChanged.connect(self.on_data_changed)

        self.populate()

    def clear(self):
        """Clears the treeview."""
        super().clear()
        self.tgh.shutdown()
        self.tgh = None

    def fault_string(self):
        """Returns the fault string."""
        if self.tgh is not None and self.tgh.telegram.zsw1.fault_present:
            return self.tgh.fault_string()
        return ""

    def basic_state(self):
        stw1 = [
            self.tgh.telegram.stw1.on,
            self.tgh.telegram.stw1.no_coast_stop,
            self.tgh.telegram.stw1.no_quick_stop,
            self.tgh.telegram.stw1.enable_operation,
        ]

        if (
            self.tgh.telegram.zsw1.fault_present
            or not self.tgh.telegram.zsw1.ready_to_switch_on
        ):
            return BasicState.SWITCHING_ON_INHIBITED
        elif not stw1[0] and stw1[1] and stw1[2]:
            return BasicState.READY_FOR_SWITCHING_ON
        elif stw1[0] and stw1[1] and stw1[2] and not stw1[3]:
            return BasicState.SWITCHED_ON
        elif stw1[0] and stw1[1] and stw1[2] and stw1[3]:
            return BasicState.OPERATION

        return BasicState.SWITCHING_ON_INHIBITED

    def word_names(self, word_list):
        """Returns a list of names of words provided in word_list.

        Parameters:
            word_list(list): list of word objects to get names from
        Returns:
            iter: iterator of word names
        """
        word_names = [x.name for x in fields(self.tgh.telegram)]
        return filter(
            lambda x: getattr(self.tgh.telegram, x) in word_list,
            word_names,
        )

    def is_bitwise_word(self, word_name):
        """Returns True if telegram attribute word_name is an BitwiseWord.

        Parameters:
            word_name(string): word name

        Returns:
            bool: True if word is Bitwiseword
        """
        return isinstance(getattr(self.tgh.telegram, word_name), BitwiseWord)

    def append_bitwise_word_item(self, root, name, value, readonly=False):
        """Append a bitwise word item to provided root.

        Parameters:
            root(Qstandarditem): root item to append to
            name(string): name of bit item
            value(bool): value of bit item
            readonly(bool): read only
        """
        item = QStandardItem(f"{name}")
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setUserTristate(True)
        item.setCheckState(Qt.PartiallyChecked if value else Qt.Unchecked)
        if readonly:
            item.setCheckable(False)
        root.appendRow(item)

    def append_value_word_item(self, root, name, value, readonly=False):
        """Append value word item to provided root.

        Parameters:
            root(Qstandarditem): root item to append to
            name(string): name of bit item
            value(bool): value of bit item
            readonly(bool): read only
        """
        item = QStandardItem(f"{name}:")
        item.setFlags(Qt.NoItemFlags)
        value_item = QStandardItem(f"{str(value)}")
        if readonly:
            value_item.setFlags(Qt.NoItemFlags)
        root.appendRow([item, value_item])

    def append_word_item(self, root, name, readonly=False):
        """Append word item to provided root.

        Parameters:
            root(Qstandarditem): root item to append to
            name(string): name of bit item
            value(bool): value of bit item
            readonly(bool): read only
        """
        word = getattr(self.tgh.telegram, name)
        word_item = QStandardItem(name)
        word_item.setFlags(Qt.NoItemFlags)
        hex_string_item = QStandardItem(hex(int(word)))
        hex_string_item.setFlags(Qt.NoItemFlags)
        bin_string_item = QStandardItem(bin(int(word)))
        bin_string_item.setFlags(Qt.NoItemFlags)

        if self.is_bitwise_word(name):
            root.appendRow([word_item, hex_string_item, bin_string_item])
        else:
            root.appendRow(word_item)

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

    def populate(self):
        """Populates a treeview model using the respective telegram handler"""

        self.output_root_item = QStandardItem("Outputs")
        self.output_root_item.setFlags(Qt.NoItemFlags)
        self.appendRow(self.output_root_item)
        for name in self.word_names(self.tgh.telegram.outputs()):
            self.append_word_item(self.output_root_item, name)

        self.input_root_item = QStandardItem("Inputs")
        self.input_root_item.setFlags(Qt.NoItemFlags)
        self.appendRow(self.input_root_item)
        for name in self.word_names(self.tgh.telegram.inputs()):
            self.append_word_item(self.input_root_item, name, readonly=True)

        self.layoutChanged.emit()

    def update_bitwise_words(self):
        output_word_items = [
            [
                self.output_root_item.child(ridx, cidx)
                for cidx in range(self.output_root_item.columnCount())
            ]
            for ridx in range(self.output_root_item.rowCount())
        ]
        input_word_items = [
            [
                self.input_root_item.child(ridx, cidx)
                for cidx in range(self.input_root_item.columnCount())
            ]
            for ridx in range(self.input_root_item.rowCount())
        ]
        for word_item in output_word_items + input_word_items:
            word_name = word_item[0].text()
            word = getattr(self.tgh.telegram, word_name)
            if self.is_bitwise_word(word_name):
                word_item[1].setText(hex(int(word)))
                word_item[2].setText(bin(int(word)))

    def on_data_changed(self, index):
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
        self.update_bitwise_words()
        Logging.logger.info(
            f"Attribute '{word_name}.{item_name}' value changed to: {new_value}"
        )
        self.tgh.update_outputs()

    def update(self):
        """Updates the content of inputs tree"""
        self.tgh.update_inputs()

        self.update_bitwise_words()
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
