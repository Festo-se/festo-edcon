"""Setup code of the main window."""

from pathlib import PurePath
from importlib.resources import files
from collections import namedtuple

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from edcon.edrive.motion_handler import MotionHandler
from edcon.gui.pyqt_helpers import bold_string
from edcon.gui.toggle_button_model import ToggleButtonModel


class MotionTab(QWidget):
    """Defines the motion tab widget."""

    def __init__(self, get_com_function):
        super().__init__()
        loadUi(PurePath(files("edcon") / "gui" / "ui" / "motion_tab.ui"), self)
        self.get_com_function = get_com_function

        self.mot = None
        self.tgh = None
        self.position_scaling = None
        self.velocity_scaling = None

        self.toggle_button = ToggleButtonModel()
        self.horizontalLayout_2.insertWidget(0, self.toggle_button)
        self.toggle_button.toggledState.connect(self.on_powerstage_toggled)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_functions)
        self.timer.start(100)

    def update_functions(self):
        """Updates the content of display labels"""
        self.update_homing_status()
        self.update_current_position()
        self.update_current_velocity()

    def update_homing_status(self):
        """Updates the homing feedback label"""
        if self.mot is not None:
            if self.mot.referenced():
                self.label_homing_feedback.setText(
                    bold_string("valid", "green", font_size=16)
                )
            else:
                self.label_homing_feedback.setText(
                    bold_string("invalid", "red", font_size=16)
                )

    def update_current_position(self):
        """Updates the position display labels"""
        if self.mot is not None:
            current_position = self.mot.current_position() / self.position_scaling
            target_position = self.line_edit_pos_rev.text()
            self.label_current_position.setText(f"{current_position:.2f}")
            self.label_target_position.setText(f"{target_position}")

    def update_current_velocity(self):
        """Updates the content display labels"""
        if self.mot is not None:
            current_velocity = self.mot.current_velocity()
            target_velocity = self.line_edit_velocity.text()
            self.label_current_velocity.setText(f"{target_velocity}")
            self.label_target_velocity.setText(f"{current_velocity:.2f}")

    def on_powerstage_toggled(self, enable):
        """Powerstage toggle callback

        Parameters:
            enable (bool): Value determining whether the powerstage should be enabled
        """
        if enable:
            com = self.get_com_function()
            self.mot = MotionHandler(com, config_mode="write")
            self.mot.base_velocity = com.read_pnu(12345, 0)
            self.position_scaling = 1 / 10 ** com.read_pnu(11724, 0)
            self.velocity_scaling = 1 / 10 ** com.read_pnu(11725, 0)
            self.mot.acknowledge_faults()
            self.mot.enable_powerstage()
        else:
            self.mot.acknowledge_faults()
            self.mot.disable_powerstage()
            self.mot = None
        self.manage_button_connections(enable)

    def button_acknowledge_all_clicked(self):
        """Acknowledge button callback"""
        self.mot.acknowledge_faults()

    def button_start_homing_clicked(self):
        """Start homing button callback"""
        self.mot.referencing_task()

    def button_jog_negative_pressed(self):
        """Jog negative button pressed callback"""
        self.mot.jog_task(False, True, duration=0)

    def button_jog_positive_pressed(self):
        """Jog positive button pressed callback"""
        self.mot.jog_task(True, False, duration=0)

    def button_jog_released(self):
        """Jog button released callback"""
        self.mot.jog_task(False, False, duration=0)
        self.mot.stop_motion_task()

    def get_single_step_parameters(self):
        """Function returning the single step parameters position and velocity

        Returns:
            position (int): Single step position
            velocity (int): Single step velocity
        """
        single_step_text = self.line_edit_single_step.text()
        single_step_velocity_text = self.line_edit_single_step_velocity.text()
        if not single_step_text or not single_step_velocity_text:
            self.label_feedback.setText(
                bold_string(
                    "Single step position or velocity value missing",
                    "red",
                    font_size=16,
                )
            )
            return None, None
        self.label_feedback.setText(bold_string(""))

        position = int(int(single_step_text) * self.position_scaling)
        velocity = int(int(single_step_velocity_text) * self.velocity_scaling)
        return position, velocity

    def button_single_step_negative_clicked(self):
        """Single step negative button callback"""
        position, velocity = self.get_single_step_parameters()
        if position is None or velocity is None:
            return
        self.mot.position_task(-1 * position, velocity, nonblocking=True)

    def button_single_step_positive_clicked(self):
        """Single step positive button callback"""
        position, velocity = self.get_single_step_parameters()
        if position is None or velocity is None:
            return
        self.mot.position_task(position, velocity, nonblocking=True)

    def button_execute_clicked(self):
        """Execute button callback"""
        position_text = self.line_edit_pos_rev.text()
        velocity_text = self.line_edit_velocity.text()

        if not position_text or not velocity_text:
            self.label_feedback.setText(
                bold_string(
                    "Target position position or velocity value missing",
                    "red",
                    font_size=16,
                )
            )
            return
        self.label_feedback.setText(bold_string(""))

        velocity = int(int(velocity_text) * self.velocity_scaling)
        position = int(int(position_text) * self.position_scaling)
        self.mot.position_task(position, velocity, absolute=True, nonblocking=True)

    def button_pause_motion_clicked(self):
        """Pause button callback"""
        self.mot.pause_motion_task()

    def button_continue_motion_clicked(self):
        """Continue button callback"""
        self.mot.resume_motion_task()

    def button_stop_movement_clicked(self):
        """Stop movement button callback"""
        self.mot.stop_motion_task()

    def manage_button_connections(self, enable):
        """Manage button connections

        Parameters:
            enable (bool): Value determining whether the buttons should be enabled
        """
        SignalAssignment = namedtuple("SignalAssignment", "signal function")
        signal_assignment_list = [
            SignalAssignment(
                self.button_acknowledge_all.clicked, self.button_acknowledge_all_clicked
            ),
            SignalAssignment(
                self.button_start_homing.clicked, self.button_start_homing_clicked
            ),
            SignalAssignment(
                self.button_jog_negative.pressed, self.button_jog_negative_pressed
            ),
            SignalAssignment(
                self.button_jog_negative.released, self.button_jog_released
            ),
            SignalAssignment(
                self.button_jog_positive.pressed, self.button_jog_positive_pressed
            ),
            SignalAssignment(
                self.button_jog_positive.released, self.button_jog_released
            ),
            SignalAssignment(
                self.button_single_step_negative.clicked,
                self.button_single_step_negative_clicked,
            ),
            SignalAssignment(
                self.button_single_step_positive.clicked,
                self.button_single_step_positive_clicked,
            ),
            SignalAssignment(self.button_execute.clicked, self.button_execute_clicked),
            SignalAssignment(
                self.button_pause_motion.clicked, self.button_pause_motion_clicked
            ),
            SignalAssignment(
                self.button_continue_motion.clicked, self.button_continue_motion_clicked
            ),
            SignalAssignment(
                self.button_stop_movement.clicked, self.button_stop_movement_clicked
            ),
        ]

        for assignment in signal_assignment_list:
            if enable:
                assignment.signal.connect(assignment.function)
            else:
                assignment.signal.disconnect(assignment.function)
