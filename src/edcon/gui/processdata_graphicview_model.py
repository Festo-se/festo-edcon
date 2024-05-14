from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QGraphicsPathItem
from PyQt5.QtCore import QRectF, QTimer, QPointF,Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPainterPath

# Constants for dimensions and colors
SCENE_WIDTH, SCENE_HEIGHT = 800, 800
STATE_WIDTH, STATE_HEIGHT = 200, 80
STATE_COLOR = "white"
TEXT_OFFSET_X, TEXT_OFFSET_Y = 100, 40
ARROW_COLOR = "black"
ARROW_WIDTH = 2
ARROW_HEAD_WIDTH, ARROW_HEAD_HEIGHT = 8, 5

class StateDiagram():
    def __init__(self,graphic_view_widget,button_show_graphicview, com):
        super().__init__()
        self.graphic_view_widget = graphic_view_widget
        self.graphic_view_widget.setVisible(False)
        self.button_show_graphicview = button_show_graphicview
        self.com = com
        self.current_state = None
        self.scene = QGraphicsScene()
        self.graphic_view_widget.setScene(self.scene)
        self.setup_scene()
        self.setup_states()
        self.setup_arrows()
        self.button_show_graphicview.clicked.connect(self.show_or_hide_graphicview)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_current_state)
        self.timer.start(100)

    def update_current_state(self):
        if self.com is not None:
            self.current_state = self.com.read_pnu(12316)
            self.update_active_state(self.current_state)
    
    def show_or_hide_graphicview(self):
        self.graphic_view_widget.setVisible(not self.graphic_view_widget.isVisible())

    def setup_scene(self):
        self.scene.setSceneRect(0, 0, SCENE_WIDTH, SCENE_HEIGHT)
        self.graphic_view_widget.setSceneRect(self.scene.sceneRect())
        self.graphic_view_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.graphic_view_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def setup_states(self):
        self.states = []
        vertical_spacing = 150
        for i in range(4):
            label = ["S1: Switching On Inhibited", "S2: Ready For Switching On", "S3: Switched On", "S4: Operation"][i]

            if label != "S52: Quick Stop" and label != "S51: Ramp Stop":
                pos = QPointF(300, i * (STATE_HEIGHT + vertical_spacing))
                state = QGraphicsRectItem(QRectF(0, 0, STATE_WIDTH, STATE_HEIGHT))
                state.setPos(pos)
                state.setBrush(QBrush(QColor(STATE_COLOR)))
                state.setPen(QPen(QColor(ARROW_COLOR), ARROW_WIDTH))
                self.states.append(state)
                self.scene.addItem(state)
                text = QGraphicsTextItem(label)
                text.setPos(pos + QPointF(STATE_WIDTH / 2 - text.boundingRect().width() / 2,
                                        STATE_HEIGHT / 2 - text.boundingRect().height() / 2))
                self.scene.addItem(text)

    def add_arrow(self, start, end, condition_left, condition_right, offset):
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
        arrow_positions = [
            ((300 + STATE_WIDTH / 2, STATE_HEIGHT + 150 - ARROW_HEAD_HEIGHT),(300 + STATE_WIDTH / 2,  STATE_HEIGHT)),
            ((300 + STATE_WIDTH / 2, STATE_HEIGHT * 2 + 300 - ARROW_HEAD_HEIGHT),(300 + STATE_WIDTH / 2,STATE_HEIGHT * 2 + 150)),
            ((300 + STATE_WIDTH / 2, STATE_HEIGHT * 3 + 450 - ARROW_HEAD_HEIGHT),(300 + STATE_WIDTH / 2, STATE_HEIGHT * 3 + 300))
        ]
        conditions_left = [
            ["OFF", "AND No Coast Stop","AND No Quick Stop", "STW1.0=false","STW1.1=true","STW1.2=true"],
            ["ON", "STW1.0=true"],
            ["Enable Operation", "STW1.3=true"]
        ]
        conditions_right = [
            ["Coast Stop", "OR Quick Stop","STW1.1=false", "OR STW1.2=false"],
            ["OFF", "STW1.0=false"],
            ["Disable Operation", "STW1.3=false"]
        ]
        for (start, end), conditions_left_single, conditions_right_single in zip(arrow_positions, conditions_left, conditions_right):
            condition_left = "\n".join(conditions_left_single)
            condition_right = "\n".join(conditions_right_single)
            right = ""
            left = ""
            self.add_arrow(start, end, left, condition_right, offset=15)
            self.add_arrow(end, start, condition_left, right, offset=-45)

    def update_active_state(self,current_state):
        for state in self.states:
            state.setBrush(QBrush(QColor(STATE_COLOR)))

        if 0 <= current_state < len(self.states):
            self.states[current_state].setBrush(QBrush(QColor("light blue")))
