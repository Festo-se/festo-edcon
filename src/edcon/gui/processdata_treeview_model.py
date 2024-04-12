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
                attribute_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
                attribute_item.setCheckState(
                    Qt.PartiallyChecked
                    if getattr(getattr(self.tgh.telegram, name), attribute_name)
                    else Qt.Unchecked
                )
                if readonly:
                    attribute_item.setCheckable(False)
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

        root = QStandardItem("Outputs")
        root.setFlags(Qt.NoItemFlags)
        self.appendRow(root)
        for name in self.output_word_names():
            self.append_word_item(root, name)

        root = QStandardItem("Inputs")
        root.setFlags(Qt.NoItemFlags)
        self.appendRow(root)
        for name in self.input_word_names():
            self.append_word_item(root, name, readonly=True)

        self.layoutChanged.emit()

    def update_inputs_gui(self):
        """Updates the treeview content"""
        if self.tgh is None:
            return
        self.tgh.update_inputs()

        root_index = self.index(1, 0)

        for row in range(self.rowCount(root_index)):
            output_item_index = self.index(row, 0, root_index)
            output_item = self.itemFromIndex(output_item_index)
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
        self.layoutChanged.emit()

    def on_item_changed(self, index):
        """Item changed callback for handling item changed events

        Parameters:
            index (QModelIndex): Index of the item that changed
        """
        root_index = self.index(0, 0)
        if root_index == index.parent().parent():
            item = self.itemFromIndex(index)
            attribute_name = item.parent().text()
            if self.is_bitwise_word(attribute_name):
                child_attribute_name = item.text()
                new_value = not getattr(
                    getattr(self.tgh.telegram, attribute_name), child_attribute_name
                )
                item.setCheckState(Qt.PartiallyChecked if new_value else Qt.Unchecked)
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
