"""Model for the processdata treeview."""

from dataclasses import fields

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt, QTimer

from edcon.gui.pyqt_helpers import bold_string
from edcon.utils.logging import Logging
from edcon.profidrive.words import BitwiseWord

class ProcessDataTreeViewModel(QStandardItemModel):
    """Defines the process data treeview model."""

    def __init__(self, tgh, label_fault_string, expand_button, tree_view):
        super().__init__()
        if tgh is None:
            raise ValueError("tgh cannot be None")
        self.label_fault_string = label_fault_string
        self.tgh = tgh
        self.setColumnCount(3)
        self.dataChanged.connect(self.on_data_changed)
        self.tree_view = tree_view

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_input_tree)
        self.timer.timeout.connect(self.update_output_tree)
        self.timer.start(100)

        self.populate()

        expand_button.clicked.connect(self.expand_all_button_clicked)

    def clear(self):
        """Clears the treeview."""
        super().clear()
        self.timer.stop()
        self.tgh.shutdown()
        self.tgh = None

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

    def append_word_item(self, root, name, readonly=False):
        """Append word item to provided root.

        Parameters:
            root(Qstandarditem): root item to append to
            name(string): name of bit item
            value(bool): value of bit item
            readonly(bool): read only
        """
        word_item = QStandardItem(name)
        word_item.setFlags(Qt.NoItemFlags)
        word = getattr(self.tgh.telegram, name)
        hex_string_item = QStandardItem(str(hex(int(word))))
        bin_string_item = QStandardItem(str(bin(int(word))))
        value_item_editable = QStandardItem("0")
        value_item_no_flags = QStandardItem("0")
        place_holder_item = QStandardItem()
        hex_string_item.setFlags(Qt.NoItemFlags)
        bin_string_item.setFlags(Qt.NoItemFlags)
        value_item_no_flags.setFlags(Qt.NoItemFlags)
        place_holder_item.setFlags(Qt.NoItemFlags)

        if self.is_bitwise_word(name):
            root.appendRow([word_item, hex_string_item, bin_string_item])
        else:
            if root.text() != "Outputs":
                root.appendRow([word_item, value_item_no_flags, place_holder_item])
            else:
                root.appendRow([word_item, value_item_editable, place_holder_item])

        item_name_list = [x.name for x in fields(word)]

        for item_name in item_name_list:
            item_value = getattr(word, item_name)
            if self.is_bitwise_word(name):
                self.append_bitwise_word_item(
                    word_item, item_name, item_value, readonly
                )

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

    def update_input_tree(self):
        """Updates the content of inputs tree"""
        self.tgh.update_inputs()

        input_word_items = [
            self.input_root_item.child(idx)
            for idx in range(self.input_root_item.rowCount())
        ]

        for word_item in input_word_items:
            input_items = [word_item.child(row) for row in range(word_item.rowCount())]
            word_name = word_item.text()
            word = getattr(self.tgh.telegram, word_name)
            if self.is_bitwise_word(word_name):
                bin_string_item = word_item.parent().child(word_item.row(), 2)
                bin_string_item.setText(str(bin(int(word))))

                hex_string_item = word_item.parent().child(word_item.row(), 1)
                hex_string_item.setText(str(hex(int(word))))

            else:
                item_value = getattr(word, "value")
                input_value = word_item.parent().child(word_item.row(), 1)
                input_value.setText(f"{item_value}")

            for item in input_items:
                if self.is_bitwise_word(word_name):
                    item_value = getattr(word, item.text())
                    if item_value:
                        item.setCheckState(Qt.PartiallyChecked)
                    else:
                        item.setCheckState(Qt.Unchecked)
        self.layoutChanged.emit()

    def update_output_tree(self):
        """Updates the content of inputs tree"""
        self.tgh.update_outputs()

        output_word_items = [
            self.output_root_item.child(idx)
            for idx in range(self.output_root_item.rowCount())
        ]

        for word_item in output_word_items:
            word_name = word_item.text()
            word = getattr(self.tgh.telegram, word_name)
            if self.is_bitwise_word(word_name):
                bin_string_item = word_item.parent().child(word_item.row(), 2)
                bin_string_item.setText(str(bin(int(word))))

                hex_string_item = word_item.parent().child(word_item.row(), 1)
                hex_string_item.setText(str(hex(int(word))))
        self.layoutChanged.emit()

    def on_data_changed(self, index):
        """Item changed callback for handling item changed events

        Parameters:
            index (QModelIndex): Index of the item that changed
        """

        if self.tgh.telegram.zsw1.fault_present:
            self.show_fault_string_label()
        else:
            self.hide_fault_string_label()

        item = self.itemFromIndex(index)
        item_text = item.text()
        # Ignore if item is not a child of Outputs
        if (
            index.parent().parent() != self.output_root_item.index()
            and index.parent() != self.output_root_item.index()
            or item_text.startswith("0x")
            and all(c in "0123456789ABCDEFabcdef" for c in item_text[2:])
            or item.index().column() == 2
        ):
            return

        # True if PartiallyChecked, False otherwise
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
            return

        word_name = item.parent().text()
        if word_name != "Outputs":
            if self.is_bitwise_word(word_name):
                word = getattr(self.tgh.telegram, word_name)
                item_name = item.text()
                new_value = item.checkState() != Qt.Unchecked
        else:
            word_name = item.parent().child(item.row(), 0).text()
            word = getattr(self.tgh.telegram, word_name)
            item_name = "value"
            new_value = int(item.text())

        setattr(word, item_name, new_value)
        Logging.logger.info(
            "Attribute '%s.%s' value changed to: '%s'", word_name, item_name, new_value
        )
        self.tgh.update_outputs()

    def show_fault_string_label(self):
        """Show fault string in label"""
        fault_string = self.tgh.fault_string()
        self.label_fault_string.setText(bold_string(f"{fault_string}", "red"))

    def hide_fault_string_label(self):
        """Hide fault string label"""
        self.label_fault_string.setText("")

    def expand_all_button_clicked(self):
        """Expand the whole treeview"""
        self.tree_view.expandAll()
