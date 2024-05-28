"""Model for the processdata graphicview."""

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtWidgets import (
    QGraphicsScene,
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGraphicsPathItem,
)
from PyQt5.QtCore import QRectF, QTimer, QPointF, Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPainterPath

# Constants for dimensions and colors
SCENE_WIDTH, SCENE_HEIGHT = 800, 775
STATE_WIDTH, STATE_HEIGHT = 200, 80
STATE_COLOR = "white"
TEXT_OFFSET_X, TEXT_OFFSET_Y = 100, 40
ARROW_COLOR = "black"
ARROW_WIDTH = 2
ARROW_HEAD_WIDTH, ARROW_HEAD_HEIGHT = 8, 5


class StateDiagram:
    """Defines the process data graphicview model."""

    def __init__(
        self,
        tgh,
        graphic_view_widget,
        button_show_graphicview,
    ):
        super().__init__()
        self.graphic_view_widget = graphic_view_widget
        self.graphic_view_widget.setVisible(False)
        self.tgh = tgh
        self.current_state = None
        self.scene = QGraphicsScene()
        self.graphic_view_widget.setScene(self.scene)
        button_show_graphicview.clicked.connect(self.show_or_hide_graphicview)
        self.setup_scene()
        self.setup_states()
        self.setup_arrows()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_active_state)
        self.timer.start(100)

    def show_or_hide_graphicview(self):
        """Show graphicview button callback"""
        self.graphic_view_widget.setVisible(not self.graphic_view_widget.isVisible())

    def setup_scene(self):
        """Sets the scene dimensions and configures the scroll bar policies"""
        self.scene.setSceneRect(0, 0, SCENE_WIDTH, SCENE_HEIGHT)
        self.graphic_view_widget.setSceneRect(self.scene.sceneRect())
        self.graphic_view_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.graphic_view_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def setup_states(self):
        """Sets up and adds labeled state rectangles to the scene at specified positions"""
        self.states = []
        vertical_spacing = 150
        for i in range(4):
            label = [
                "S1: Switching On Inhibited",
                "S2: Ready For Switching On",
                "S3: Switched On",
                "S4: Operation",
            ][i]

            if label not in ("S52: Quick Stop", "S51: Ramp Stop"):
                pos = QPointF(300, i * (STATE_HEIGHT + vertical_spacing))
                state = QGraphicsRectItem(QRectF(0, 0, STATE_WIDTH, STATE_HEIGHT))
                state.setPos(pos)
                state.setBrush(QBrush(QColor(STATE_COLOR)))
                state.setPen(QPen(QColor(ARROW_COLOR), ARROW_WIDTH))
                self.states.append(state)
                self.scene.addItem(state)
                text = QGraphicsTextItem(label)
                text.setPos(
                    pos
                    + QPointF(
                        STATE_WIDTH / 2 - text.boundingRect().width() / 2,
                        STATE_HEIGHT / 2 - text.boundingRect().height() / 2,
                    )
                )
                self.scene.addItem(text)

    def add_arrow(self, start, end, condition_left, condition_right):
        """Adds arrows and their conditions on the correct place

        Parameters:
            start(int): starting point
            end(int):   ending point
            condition_left(str): condition on the left side
            condition_right(str): condition on the right side
            offset(int)
        """
        if condition_left == "":
            offset = 15
        else:
            offset = -45
        # Adjust starting and ending points based on offset for parallel arrows
        start = QPointF(start[0] + offset, start[1])
        end = QPointF(end[0] + offset, end[1])

        # Create the main line of the arrow
        path = QPainterPath(start)
        path.lineTo(end)
        arrow = QGraphicsPathItem(path)
        arrow.setPen(QPen(QColor(ARROW_COLOR), ARROW_WIDTH))
        self.scene.addItem(arrow)

        # Create the arrow head at the end point
        arrow_head = QPainterPath()
        if offset > 0:
            # Arrow head pointing downwards
            arrow_head.moveTo(end)
            arrow_head.lineTo(end + QPointF(-ARROW_HEAD_WIDTH, ARROW_HEAD_HEIGHT))
            arrow_head.lineTo(end + QPointF(ARROW_HEAD_WIDTH, ARROW_HEAD_HEIGHT))
        else:
            # Arrow head pointing upwards
            arrow_head.moveTo(end)
            arrow_head.lineTo(end + QPointF(-ARROW_HEAD_WIDTH, -ARROW_HEAD_HEIGHT))
            arrow_head.lineTo(end + QPointF(ARROW_HEAD_WIDTH, -ARROW_HEAD_HEIGHT))
        arrow_head.closeSubpath()  # Close the path to make a solid triangle
        arrow_item = QGraphicsPathItem(arrow_head)
        arrow_item.setBrush(QColor(ARROW_COLOR))
        self.scene.addItem(arrow_item)

        text_left = QGraphicsTextItem(condition_left)
        mid_point_left = (start + end) / 2  # Calculate midpoint for text placement
        text_left.setPos(mid_point_left + QPointF(-120, -50))  # Adjust text position
        self.scene.addItem(text_left)

        text_right = QGraphicsTextItem(condition_right)
        mid_point_right = (start + end) / 2  # Calculate midpoint for text placement
        text_right.setPos(mid_point_right + QPointF(15, -50))  # Adjust text position
        self.scene.addItem(text_right)

    def setup_arrows(self):
        """ ""Setup the positions for the arrows"""
        arrow_positions = [
            (
                (300 + STATE_WIDTH / 2, STATE_HEIGHT + 150 - ARROW_HEAD_HEIGHT),
                (300 + STATE_WIDTH / 2, STATE_HEIGHT),
            ),
            (
                (300 + STATE_WIDTH / 2, STATE_HEIGHT * 2 + 300 - ARROW_HEAD_HEIGHT),
                (300 + STATE_WIDTH / 2, STATE_HEIGHT * 2 + 150),
            ),
            (
                (300 + STATE_WIDTH / 2, STATE_HEIGHT * 3 + 450 - ARROW_HEAD_HEIGHT),
                (300 + STATE_WIDTH / 2, STATE_HEIGHT * 3 + 300),
            ),
        ]
        conditions_left = [
            [
                "OFF",
                "AND No Coast Stop",
                "AND No Quick Stop",
                "STW1.0=false",
                "STW1.1=true",
                "STW1.2=true",
            ],
            ["ON", "STW1.0=true"],
            ["Enable Operation", "STW1.3=true"],
        ]
        conditions_right = [
            ["Coast Stop", "OR Quick Stop", "STW1.1=false", "OR STW1.2=false"],
            ["OFF", "STW1.0=false"],
            ["Disable Operation", "STW1.3=false"],
        ]
        for (start, end), conditions_left_single, conditions_right_single in zip(
            arrow_positions, conditions_left, conditions_right
        ):
            condition_left = "\n".join(conditions_left_single)
            condition_right = "\n".join(conditions_right_single)
            right = ""
            left = ""
            self.add_arrow(start, end, left, condition_right)
            self.add_arrow(end, start, condition_left, right)

    def update_active_state(self):
        """Update the active state in state diagram

        Parameters:
            current_state(int): value for the state diagram
        """
        bit_word_stw1 = self.tgh.telegram.stw1
        bit_word_zsw1 = self.tgh.telegram.zsw1
        stw1_bit0 = getattr(bit_word_stw1, "on")
        stw1_bit1 = getattr(bit_word_stw1, "no_coast_stop")
        stw1_bit2 = getattr(bit_word_stw1, "no_quick_stop")
        stw1_bit3 = getattr(bit_word_stw1, "enable_operation")
        zsw1_bit0 = getattr(bit_word_zsw1, "ready_to_switch_on")
        zsw1_bit3 = getattr(bit_word_zsw1, "fault_present")

        if not zsw1_bit3:
            if zsw1_bit0:
                if not stw1_bit0 and (not stw1_bit1 or not stw1_bit2):
                    self.current_state = 0
                elif not stw1_bit0 and stw1_bit1 and stw1_bit2:
                    self.current_state = 1
                elif stw1_bit0 and stw1_bit1 and stw1_bit2 and not stw1_bit3:
                    self.current_state = 2
                elif stw1_bit0 and stw1_bit1 and stw1_bit2 and stw1_bit3:
                    self.current_state = 3
            else:
                self.current_state = 0
        else:
            self.current_state = 7 #fault present

        for state in self.states:
            state.setBrush(QBrush(QColor(STATE_COLOR)))

        if 0 <= self.current_state < len(self.states):
            self.states[self.current_state].setBrush(QBrush(QColor("light blue")))
