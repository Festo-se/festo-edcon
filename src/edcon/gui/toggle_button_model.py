"""Model for the toggle button."""

from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import QPropertyAnimation, QPoint, Qt, pyqtSignal


class ToggleButtonModel(QPushButton):
    """Defines the toggle button model."""

    # pylint: disable=too-few-public-methods

    toggledState = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setCheckable(True)
        self.setMinimumSize(60, 30)

        self.label = QLabel("Off", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.move(2, 5)
        self.label.resize(25, 20)

        style_file_path = files("edcon") / "gui" / "ui" / "toggle_button_styles.css"
        with open(style_file_path, "r", encoding="utf-8") as style_file:
            self.setStyleSheet(style_file.read())

        self.animation = QPropertyAnimation(self.label, b"pos")
        self.animation.setDuration(200)
        self.toggled.connect(self.on_toggle)

    def on_toggle(self, checked):
        """Callback for toggle signal of the button."""
        self.label.setText("On" if checked else "Off")
        self.animation.setEndValue(QPoint(33 if checked else 2, 5))
        self.animation.start()
        self.toggledState.emit(checked)
