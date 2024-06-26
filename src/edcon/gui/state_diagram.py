"""View for the state diagram."""

from pyqtgraph import (
    GraphicsLayoutWidget,
    TextItem,
    PlotCurveItem,
    ArrowItem,
    mkPen,
    mkBrush,
)
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QColor, QPen, QBrush


class StateDiagram(GraphicsLayoutWidget):
    """Initializes the StateDiagram with a viewbox and sets up states and arrows."""

    def __init__(self):
        """Initializes the StateDiagram with a viewbox and sets up states and arrows."""
        super().__init__()
        self.setBackground(0.90)
        self.view_box = self.addViewBox()
        self.view_box.setAspectLocked()
        self.view_box.setBackgroundColor(0.90)
        self.rects = {}
        self.texts = {}
        self.states = {
            "S1": {"label": "S1: Switching On Inhibited", "pos": (0, 0)},
            "S2": {"label": "S2: Ready For Switching On", "pos": (0, -150)},
            "S3": {"label": "S3: Switched On", "pos": (0, -300)},
            "S4": {"label": "S4: Operation", "pos": (0, -450)},
        }
        self.arrows = [("S1", "S2"), ("S2", "S3"), ("S3", "S4")]
        self.conditions = [
            (
                "OFF\nAND No Coast Stop\nAND No Quick Stop\nSTW1.0=false\nSTW1.1=true\nSTW1.2=true",
                "Coast Stop\nOR Quick Stop\nSTW1.1=false\nOR STW1.2=false",
            ),
            ("ON\nSTW1.0=true", "OFF\nSTW1.0=false"),
            ("Enable Operation\nSTW1.3=true", "Disable Operation\nSTW1.3=false"),
        ]
        self.create_states()
        self.create_transitions()

    def create_state_item(self, state, pos, label):
        """
        Creates a state item with a rectangle and label.

        Args:
            state (str): The state key.
            pos (tuple): The (x, y) position of the state.
            label (str): The label text of the state.
        """
        x, y = pos
        rect = QGraphicsRectItem(-100, -40, 200, 80)
        rect.setPos(x, y)
        rect.setPen(QPen(QColor("#0056b3"), 2))
        rect.setBrush(QBrush(QColor(200, 200, 200)))
        self.view_box.addItem(rect)
        self.rects[state] = rect

        text = TextItem(label, anchor=(0.5, 0.5), color="white")
        text.setPos(x, y)
        self.view_box.addItem(text)
        self.texts[state] = text

    def create_states(self):
        """Sets up and adds labeled state rectangles to the scene at specified positions."""
        for state, data in self.states.items():
            self.create_state_item(state, data["pos"], data["label"])

    def draw_arrow(self, start_pos, end_pos):
        """
        Draws a line between two positions with arrowheads.

        Args:
            start_pos (tuple): The (x, y) position of the starting point.
            end_pos (tuple): The (x, y) position of the ending point.
        """
        self.view_box.addItem(
            PlotCurveItem(
                [start_pos[0], start_pos[0]],
                [start_pos[1] - 40, end_pos[1] + 40],
                pen=mkPen(color=(0, 0, 0), width=2),
            )
        )
        arrow_down = ArrowItem(angle=-90, pen={"color": "k", "width": 2}, brush="k")
        arrow_down.setPos(start_pos[0], end_pos[1] + 40)
        self.view_box.addItem(arrow_down)

        self.view_box.addItem(
            PlotCurveItem(
                [end_pos[0] + 10, start_pos[0] + 10],
                [end_pos[1] + 40, start_pos[1] - 40],
                pen=mkPen(color=(0, 0, 0), width=2),
            )
        )
        arrow_up = ArrowItem(angle=90, pen={"color": "k", "width": 2}, brush="k")
        arrow_up.setPos(end_pos[0] + 10, start_pos[1] - 40)
        self.view_box.addItem(arrow_up)

    def draw_condition(self, x, y, text_content):
        """
        Draws text at a specified position.

        Args:
            x (float): The x-coordinate of the text position.
            y (float): The y-coordinate of the text position.
            text_content (str): The content of the text.
        """
        text = TextItem(text_content, anchor=(0.5, 0.5), color=(0, 0, 0))
        text.setPos(x, y)
        self.view_box.addItem(text)

    def create_transition_items(self, start, end, condition_left, condition_right):
        """
        Creates arrow items between two states with conditions.

        Args:
            start (str): The starting state key.
            end (str): The ending state key.
            condition_left (str): The condition text on the left side of the arrow.
            condition_right (str): The condition text on the right side of the arrow.
        """
        start_pos = self.states[start]["pos"]
        end_pos = self.states[end]["pos"]
        self.draw_arrow(start_pos, end_pos)
        self.draw_condition(
            (start_pos[0] + end_pos[0]) / 2 - 150,
            (start_pos[1] + end_pos[1]) / 2,
            condition_left,
        )
        self.draw_condition(
            (start_pos[0] + end_pos[0]) / 2 + 150,
            (start_pos[1] + end_pos[1]) / 2,
            condition_right,
        )

    def create_transitions(self):
        """Sets up the positions for the arrows and their conditions at the correct places."""
        for (start, end), (condition_left, condition_right) in zip(
            self.arrows, self.conditions
        ):
            self.create_transition_items(start, end, condition_left, condition_right)

    def update_state(self, current_state):
        """
        Updates the active state in the state diagram.

        Args:
            current_state (int): The index of the state to be set as active.
        """
        for rect in self.rects.values():
            rect.setBrush(mkBrush(200, 200, 200))
        state_key = list(self.states.keys())[current_state]
        self.rects[state_key].setBrush(mkBrush(0, 170, 255))

    # pylint: disable=invalid-name
    # PyQt API naming
    def resizeEvent(self, ev):
        """Handles the resize event and updates text sizes accordingly."""
        if ev is not None:
            scale_factor = min(self.width(), self.height()) / 900
            for state, text in self.texts.items():
                text.setHtml(
                    f'<div style="font-size: {14 * scale_factor}pt; \
                            color: white;">{self.states[state]["label"]}</div>'
                )
        super().resizeEvent(ev)
