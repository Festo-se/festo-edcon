"""View for the state diagram."""
import pyqtgraph as pg
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QColor, QPen, QBrush


class StateDiagram(pg.ViewBox):
    """Initializes the StateDiagram with a viewbox and sets up states and arrows."""

    def __init__(self):
        """Initializes the StateDiagram with a viewbox and sets up states and arrows."""
        super().__init__()
        self.setAspectLocked()
        self.setBackgroundColor("w")
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
            ("OFF\nAND No Coast Stop\nAND No Quick Stop\nSTW1.0=false\nSTW1.1=true\nSTW1.2=true", 
             "Coast Stop\nOR Quick Stop\nSTW1.1=false\nOR STW1.2=false"),
            ("ON\nSTW1.0=true", "OFF\nSTW1.0=false"),
            ("Enable Operation\nSTW1.3=true", "Disable Operation\nSTW1.3=false"),
        ]
        self.create_states()
        self.create_arrows()
        self.resizeEvent = self.on_resize # pylint: disable=invalid-name

    def create_states(self):
        """Sets up and adds labeled state rectangles to the scene at specified positions."""
        for state, data in self.states.items():
            self._create_state_item(state, data["pos"], data["label"])

    def _create_state_item(self, state, pos, label):
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
        self.addItem(rect)
        self.rects[state] = rect

        text = pg.TextItem(label, anchor=(0.5, 0.5), color="white")
        text.setPos(x, y)
        self.addItem(text)
        self.texts[state] = text

    def create_arrows(self):
        """Sets up the positions for the arrows and their conditions at the correct places."""
        for (start, end), (condition_left, condition_right) in zip(self.arrows, self.conditions):
            self._create_arrow_items(start, end, condition_left, condition_right)

    def _create_arrow_items(self, start, end, condition_left, condition_right):
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
        self._draw_arrow(start_pos, end_pos, condition_left, condition_right)

    def _draw_arrow(self, start_pos, end_pos, condition_left, condition_right):
        """
        Draws an arrow between two positions with conditions.

        Args:
            start_pos (tuple): The (x, y) position of the starting state.
            end_pos (tuple): The (x, y) position of the ending state.
            condition_left (str): The condition text on the left side of the arrow.
            condition_right (str): The condition text on the right side of the arrow.
        """
        self._draw_line(start_pos, end_pos)
        self._draw_text((start_pos[0] + end_pos[0]) / 2 - 150, (start_pos[1] + end_pos[1]) / 2, condition_left)
        self._draw_text((start_pos[0] + end_pos[0]) / 2 + 150, (start_pos[1] + end_pos[1]) / 2, condition_right)

    def _draw_line(self, start_pos, end_pos):
        """
        Draws a line between two positions with arrowheads.

        Args:
            start_pos (tuple): The (x, y) position of the starting point.
            end_pos (tuple): The (x, y) position of the ending point.
        """
        self.addItem(pg.PlotCurveItem([start_pos[0], start_pos[0]], [start_pos[1] - 40, end_pos[1] + 40], pen=pg.mkPen(color=(0, 0, 0), width=2)))
        arrow_down = pg.ArrowItem(angle=-90, pen={"color": "k", "width": 2}, brush="k")
        arrow_down.setPos(start_pos[0], end_pos[1] + 40)
        self.addItem(arrow_down)

        self.addItem(pg.PlotCurveItem([end_pos[0] + 10, start_pos[0] + 10], [end_pos[1] + 40, start_pos[1] - 40], pen=pg.mkPen(color=(0, 0, 0), width=2)))
        arrow_up = pg.ArrowItem(angle=90, pen={"color": "k", "width": 2}, brush="k")
        arrow_up.setPos(end_pos[0] + 10, start_pos[1] - 40)
        self.addItem(arrow_up)

    def _draw_text(self, x, y, text_content):
        """
        Draws text at a specified position.

        Args:
            x (float): The x-coordinate of the text position.
            y (float): The y-coordinate of the text position.
            text_content (str): The content of the text.
        """
        text = pg.TextItem(text_content, anchor=(0.5, 0.5), color=(0, 0, 0))
        text.setPos(x, y)
        self.addItem(text)

    def on_resize(self, event):
        """Handles the resize event and updates text sizes accordingly."""
        self.update_text_sizes()
        super().resizeEvent(event)

    def update_text_sizes(self):
        """Updates the text sizes based on the current window dimensions."""
        scale_factor = min(self.width(), self.height()) / 900
        for state, text in self.texts.items():
            text.setHtml(f'<div style="font-size: {14 * scale_factor}pt; color: white;">{self.states[state]["label"]}</div>')

    def update_state(self, current_state):
        """
        Updates the active state in the state diagram.

        Args:
            current_state (int): The index of the state to be set as active.
        """
        for rect in self.rects.values():
            rect.setBrush(pg.mkBrush(200, 200, 200))
        state_key = list(self.states.keys())[current_state]
        self.rects[state_key].setBrush(pg.mkBrush(0, 170, 255))
    
