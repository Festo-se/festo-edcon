"""Scene for the state diagram."""

import pyqtgraph as pg
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QColor, QPen, QBrush


class StateDiagram(pg.GraphicsLayoutWidget):
    def __init__(
        self,
    ):
        super().__init__()
        self.view = self.addViewBox()
        self.view.setAspectLocked()
        self.view.setBackgroundColor("w")
        self.rects = {}
        self.texts = {}
        self.current_state = None
        self.create_states()
        self.create_arrows()
        self.resizeEvent = self.on_resize

    def create_states(self):
        """Sets up and adds labeled state rectangles to the scene at specified positions"""
        self.states = {
            "S1": {"label": "S1: Switching On Inhibited", "pos": (0, 0)},
            "S2": {"label": "S2: Ready For Switching On", "pos": (0, -150)},
            "S3": {"label": "S3: Switched On", "pos": (0, -300)},
            "S4": {"label": "S4: Operation", "pos": (0, -450)},
        }

        for state, data in self.states.items():
            x, y = data["pos"]
            rect = QGraphicsRectItem(-100, -40, 200, 80)
            rect.setPos(x, y)
            color = QColor(200, 200, 200)
            pen = QPen(QColor("#0056b3"))
            pen.setWidth(2)
            brush = QBrush(color)
            rect.setPen(pen)
            rect.setBrush(brush)
            self.view.addItem(rect)
            self.rects[state] = rect

            text = pg.TextItem(data["label"], anchor=(0.5, 0.5), color="white")
            text.setPos(x, y)
            self.view.addItem(text)
            self.texts[state] = text

    def create_arrows(self):
        """Setup the positions for the arrows and their conditions on the correct place"""

        arrows = [
            ("S1", "S2"),
            ("S2", "S3"),
            ("S3", "S4"),
        ]

        conditions = [
            (
                "OFF\nAND No Coast Stop\nAND No Quick Stop\nSTW1.0=false\nSTW1.1=true\nSTW1.2=true",
                "Coast Stop\nOR Quick Stop\nSTW1.1=false\nOR STW1.2=false",
            ),
            ("ON\nSTW1.0=true", "OFF\nSTW1.0=false"),
            ("Enable Operation\nSTW1.3=true", "Disable Operation\nSTW1.3=false"),
        ]

        for i, ((start, end), (condition_left, condition_right)) in enumerate(
            zip(arrows, conditions)
        ):
            start_pos = self.states[start]["pos"]
            end_pos = self.states[end]["pos"]

            # Arrow pointing down
            line_down = pg.PlotCurveItem(
                [start_pos[0], start_pos[0]],
                [start_pos[1] - 40, end_pos[1] + 40],
                pen=pg.mkPen(color=(0, 0, 0), width=2),
            )
            self.view.addItem(line_down)

            arrow_head_down = pg.ArrowItem(
                angle=-90, pen={"color": "k", "width": 2}, brush="k"
            )
            arrow_head_down.setPos(start_pos[0], end_pos[1] + 40)
            self.view.addItem(arrow_head_down)

            text_left = pg.TextItem(condition_left, anchor=(0.5, 0.5), color=(0, 0, 0))
            text_left.setPos(
                (start_pos[0] + end_pos[0]) / 2 - 150, (start_pos[1] + end_pos[1]) / 2
            )
            self.view.addItem(text_left)

            # Arrow pointing up
            line_up = pg.PlotCurveItem(
                [end_pos[0] + 10, start_pos[0] + 10],
                [end_pos[1] + 40, start_pos[1] - 40],
                pen=pg.mkPen(color=(0, 0, 0), width=2),
            )
            self.view.addItem(line_up)

            arrow_head_up = pg.ArrowItem(
                angle=90, pen={"color": "k", "width": 2}, brush="k"
            )
            arrow_head_up.setPos(end_pos[0] + 10, start_pos[1] - 40)
            self.view.addItem(arrow_head_up)

            text_right = pg.TextItem(
                condition_right, anchor=(0.5, 0.5), color=(0, 0, 0)
            )
            text_right.setPos(
                (start_pos[0] + end_pos[0]) / 2 + 150, (start_pos[1] + end_pos[1]) / 2
            )
            self.view.addItem(text_right)

    def on_resize(self, event):
        """Handles the resize event and updates text sizes accordingly."""
        self.update_text_sizes()
        super().resizeEvent(event)

    def update_text_sizes(self):
        """Updates the text sizes based on the current window dimensions."""
        width = self.width()
        height = self.height()
        scale_factor = min(width, height) / 900
        for state, text in self.texts.items():
            label_html = f'<div style="font-size: {14 * scale_factor}pt; color: white;">{self.states[state]["label"]}</div>'
            text.setHtml(label_html)

    def update(self, current_state):
        """Update the active state in state diagram

        Parameters:
            current_state: State to be set as active
        """
        for rect in self.rects.values():
            rect.setBrush(pg.mkBrush(200, 200, 200))

        state_keys = list(self.states.keys())  # This will be ["S1", "S2", "S3", "S4"]
        if 0 <= current_state < len(state_keys):
            state_key = state_keys[current_state]
            self.rects[state_key].setBrush(pg.mkBrush(0, 170, 255))
