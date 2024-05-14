"""Setup code of the main window."""

from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
import threading
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QCoreApplication
from edcon.edrive.motion_handler import MotionHandler
from edcon.utils.logging import Logging
from edcon.gui.pyqt_helpers import bold_string
from edcon.gui.toggle_button_model import ToggleButtonModel

# Enable loglevel info
Logging()


class MotionTab(QWidget):
    """Defines the main window."""

    def __init__(self, get_com_function):
        super().__init__()
        loadUi(PurePath(files("edcon") / "gui" / "ui" / "motion_tab.ui"), self)
        self.get_com_function = get_com_function

        self.com = None
        self.mot = None
        self.tgh = None
        self.position_unit = 1000000
        self.velocity_unit = 1000

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_functions)
        self.timer.start(100)

        self.toggle_button = ToggleButtonModel()
        self.horizontalLayout_2.insertWidget(0, self.toggle_button)
        self.toggle_button.toggledState.connect(self.on_powerstage_toggled)

    def update_functions(self):
        self.update_actual_position()
        self.update_homing_status()
        self.update_actual_velocity()

    def manage_button_connections(self, is_on):
        if is_on:
            self.button_jog_positive.pressed.connect(self.button_jog_positive_pressed)
            self.button_jog_negative.pressed.connect(self.button_jog_negative_pressed)
            self.button_execute.clicked.connect(self.button_execute_clicked)
            self.button_acknowledge_all.clicked.connect(
                self.button_acknowledge_all_clicked
            )
            self.button_stop.clicked.connect(self.button_stop_clicked)
            self.button_stop_movement.clicked.connect(self.button_stop_movement_clicked)
            self.button_start_homing.clicked.connect(self.button_start_homing_clicked)
            self.button_single_step_negative.clicked.connect(
                self.button_single_step_negative_clicked
            )
            self.button_single_step_positive.clicked.connect(
                self.button_single_step_positive_clicked
            )
            self.button_pause_motion.clicked.connect(self.button_pause_motion_clicked)
            self.button_continue_motion.clicked.connect(
                self.button_continue_motion_clicked
            )
        else:
            self.button_jog_positive.pressed.disconnect(
                self.button_jog_positive_pressed
            )
            self.button_jog_negative.pressed.disconnect(
                self.button_jog_negative_pressed
            )
            self.button_execute.clicked.disconnect(self.button_execute_clicked)
            self.button_acknowledge_all.clicked.disconnect(
                self.button_acknowledge_all_clicked
            )
            self.button_stop.clicked.disconnect(self.button_stop_clicked)
            self.button_stop_movement.clicked.disconnect(
                self.button_stop_movement_clicked
            )
            self.button_start_homing.clicked.disconnect(
                self.button_start_homing_clicked
            )
            self.button_single_step_negative.clicked.disconnect(
                self.button_single_step_negative_clicked
            )
            self.button_single_step_positive.clicked.disconnect(
                self.button_single_step_positive_clicked
            )
            self.button_pause_motion.clicked.disconnect(
                self.button_pause_motion_clicked
            )
            self.button_continue_motion.clicked.disconnect(
                self.button_continue_motion_clicked
            )

    def on_powerstage_toggled(self, is_on):
        if self.com is None and is_on:
            self.com = self.get_com_function()
            self.mot = MotionHandler(self.com, config_mode="write")

        if is_on:
            self.mot.acknowledge_faults()
            self.mot.enable_powerstage()
            self.manage_button_connections(is_on)

        else:
            self.mot.acknowledge_faults()
            self.mot.disable_powerstage()
            self.manage_button_connections(is_on)
            self.mot = None
            self.com = None

    def button_jog_positive_pressed(self):
        while QApplication.mouseButtons():
            self.mot.jog_task(True, False, duration=0)
            QCoreApplication.processEvents()
        self.mot.stop_motion_task()

    def button_jog_negative_pressed(self):
        while QApplication.mouseButtons():
            self.mot.jog_task(False, True, duration=0)
            QCoreApplication.processEvents()
        self.mot.stop_motion_task()

    def position_task_absolute_thread(self, position, velocity):
        self.mot.position_task(int(position), int(velocity), absolute=True)

    def button_execute_clicked(self):
        velocity = int(self.line_edit_velocity.text()) * self.velocity_unit
        position = int(self.line_edit_pos_rev.text()) * self.position_unit

        if velocity and (position or position == 0):
            threading.Thread(
                target=self.position_task_absolute_thread, args=(position, velocity)
            ).start()
            self.label_target_position_feedback.setText(bold_string(""))

        else:
            self.label_target_position_feedback.setText(
                bold_string("velocity or position specification missing", "red")
            )

    def button_acknowledge_all_clicked(self):
        self.mot.acknowledge_faults()

    def button_stop_clicked(self):
        self.mot.stop_motion_task()

    def button_start_homing_clicked(self):
        self.mot.referencing_task()

    def button_stop_movement_clicked(self):
        self.mot.stop_motion_task()

    def button_single_step_positive_clicked(self):
        if self.line_edit_single_step.text() != "":
            position = self.position_unit * int(self.line_edit_single_step.text())
            threading.Thread(
                target=self.mot.position_task, args=(position, 600000)
            ).start()

        else:
            self.label_single_step_feedback.setText(
                bold_string("Relative position specification missing", "red")
            )

    def button_single_step_negative_clicked(self):
        if self.line_edit_single_step.text() != "":
            position = -1 * self.position_unit * int(self.line_edit_single_step.text())
            threading.Thread(
                target=self.mot.position_task, args=(position, 600000)
            ).start()

        else:
            self.label_single_step_feedback.setText(
                bold_string("Relative position specification missing", "red")
            )

    def button_pause_motion_clicked(self):
        self.mot.pause_motion_task()

    def button_continue_motion_clicked(self):
        self.mot.resume_motion_task()

    def update_actual_position(self):
        if self.mot is not None:
            current_position = self.mot.current_position() / 1000000
            target_position = self.line_edit_pos_rev.text()
            self.label_actual_position.setText(f"{current_position}")
            self.label_target_position.setText(f"{target_position}")

    def update_actual_velocity(self):
        if self.mot is not None:
            current_velocity = self.mot.current_velocity()
            target_velocity = self.line_edit_velocity.text()
            self.label_actual_velocity.setText(f"{target_velocity}")
            self.label_target_velocity.setText(f"{current_velocity}")

    def update_homing_status(self):
        if self.mot is not None:
            if self.mot.referenced():
                self.label_homing_feedback.setText(bold_string("valid", "green"))

            else:
                self.label_homing_feedback.setText(bold_string("invalid", "red"))
