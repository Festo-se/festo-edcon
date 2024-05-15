"""Setup code of the main window."""

import threading
from pathlib import PurePath
from importlib.resources import files
from collections import namedtuple

# pylint: disable=import-error, no-name-in-module
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

        self.mot = None
        self.tgh = None
        self.position_unit = None
        self.velocity_unit = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_functions)
        self.timer.start(100)

        self.toggle_button = ToggleButtonModel()
        self.horizontalLayout_2.insertWidget(0, self.toggle_button)
        self.toggle_button.toggledState.connect(self.on_powerstage_toggled)

    def __del__(self):
        if self.mot is not None:
            self.mot = None

    def update_functions(self):
        self.update_actual_position()
        self.update_homing_status()
        self.update_actual_velocity()

    def manage_button_connections(self, enable):
        SignalAssignment = namedtuple("SignalAssignment", "signal function")

        signal_assignment_list = [
            SignalAssignment(
                self.button_start_homing.clicked, self.button_start_homing_clicked
            ),
            SignalAssignment(
                self.button_jog_positive.pressed, self.button_jog_positive_pressed
            ),
            SignalAssignment(
                self.button_jog_negative.pressed, self.button_jog_negative_pressed
            ),
            SignalAssignment(self.button_execute.clicked, self.button_execute_clicked),
            SignalAssignment(
                self.button_acknowledge_all.clicked, self.button_acknowledge_all_clicked
            ),
            SignalAssignment(self.button_stop.clicked, self.button_stop_clicked),
            SignalAssignment(
                self.button_stop_movement.clicked, self.button_stop_movement_clicked
            ),
            SignalAssignment(
                self.button_single_step_negative.clicked,
                self.button_single_step_negative_clicked,
            ),
            SignalAssignment(
                self.button_single_step_positive.clicked,
                self.button_single_step_positive_clicked,
            ),
            SignalAssignment(
                self.button_pause_motion.clicked, self.button_pause_motion_clicked
            ),
            SignalAssignment(
                self.button_continue_motion.clicked, self.button_continue_motion_clicked
            ),
        ]

        for assignment in signal_assignment_list:
            if enable:
                assignment.signal.connect(assignment.function)
            else:
                assignment.signal.disconnect(assignment.function)

    def on_powerstage_toggled(self, enable):
        if enable:
            com = self.get_com_function()
            self.mot = MotionHandler(com, config_mode="write")
            self.mot.base_velocity = com.read_pnu(12345, 0)
            self.velocity_unit = com.read_pnu(11725, 0)
            self.position_unit = com.read_pnu(11724, 0)
            self.mot.acknowledge_faults()
            self.mot.enable_powerstage()
        else:
            self.mot.acknowledge_faults()
            self.mot.disable_powerstage()
            self.mot = None
        self.manage_button_connections(enable)

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
        velocity = int(self.line_edit_velocity.text()) * int(
            1 / (10**self.velocity_unit)
        )
        position = int(self.line_edit_pos_rev.text()) * int(
            1 / (10**self.position_unit)
        )

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
            position = int(self.line_edit_single_step.text()) * int(
                1 / (10**self.position_unit)
            )
            velocity = int(1 / (10**self.velocity_unit)) * int(
                self.line_edit_single_step_velocity.text()
            )
            threading.Thread(
                target=self.mot.position_task, args=(position, velocity)
            ).start()

        else:
            self.label_single_step_feedback.setText(
                bold_string("Relative position specification missing", "red")
            )

    def button_single_step_negative_clicked(self):
        if self.line_edit_single_step.text() != "":
            position = (
                -1
                * int(self.line_edit_single_step.text())
                * int(1 / (10**self.position_unit))
            )
            velocity = int(1 / (10**self.velocity_unit)) * int(
                self.line_edit_single_step_velocity.text()
            )
            threading.Thread(
                target=self.mot.position_task, args=(position, velocity)
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
            current_position = self.mot.current_position() * (10**self.position_unit)
            target_position = self.line_edit_pos_rev.text()
            self.label_actual_position.setText(f"{current_position:.2f}")
            self.label_target_position.setText(f"{target_position}")

    def update_actual_velocity(self):
        if self.mot is not None:
            current_velocity = self.mot.current_velocity()
            target_velocity = self.line_edit_velocity.text()
            self.label_actual_velocity.setText(f"{target_velocity}")
            self.label_target_velocity.setText(f"{current_velocity:.2f}")

    def update_homing_status(self):
        if self.mot is not None:
            if self.mot.referenced():
                self.label_homing_feedback.setText(bold_string("valid", "green"))

            else:
                self.label_homing_feedback.setText(bold_string("invalid", "red"))
