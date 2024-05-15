from importlib.resources import files
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import QPropertyAnimation, QPoint, Qt, pyqtSignal


class ToggleButtonModel(QPushButton):
    toggledState = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setCheckable(True)
        self.setMinimumSize(60, 30)

        self.label = QLabel("Off", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.move(2, 5)
        self.label.resize(25, 20)

        self.load_styles()

        self.animation = QPropertyAnimation(self.label, b"pos")
        self.animation.setDuration(200)
        self.toggled.connect(self.on_toggle)

    def load_styles(self):

        with open(
            files("edcon") / "gui" / "ui" / "toggle_button_styles.css", "r"
        ) as style_file:
            stylesheet = style_file.read()
        self.setStyleSheet(stylesheet)

    def on_toggle(self, checked):
        self.label.setText("On" if checked else "Off")
        self.animation.setEndValue(QPoint(33 if checked else 2, 5))
        self.animation.start()
        self.toggledState.emit(checked)
