"""
Contains EDriveMotion class to configure and control
EDrive devices in position mode.
"""
import logging
import time
import traceback
from profidrive.telegram111 import Telegram111
from profidrive.words import OVERRIDE, MDI_ACC, MDI_DEC
from edrive.edrive_base import EDriveBase


class EDriveMotion:
    """
    This class is used to control the EDrive devices in position mode (telegram 111).
    It provides a set of functions to control the position of the EDrive using different modes.
    """
    # pylint: disable=too-many-public-methods

    over_v = property(fset=lambda self, value: setattr(
        self.tg111, 'override',
        OVERRIDE(int(16384*(value/100.0)))), doc="Override velocity in percent")
    over_acc = property(fset=lambda self, value: setattr(
        self.tg111, 'mdi_acc',
        MDI_ACC(int(16384*(value/100.0)))), doc="Override acceleration in percent")
    over_dec = property(fset=lambda self, value: setattr(
        self.tg111, 'mdi_dec',
        MDI_DEC(int(16384*(value/100.0)))), doc="Override deceleration in percent")

    def __init__(self, edrive: EDriveBase = None) -> None:
        self.tg111 = Telegram111()
        # Configure default values of the telegram
        self.tg111.stw1.control_by_plc = True
        self.tg111.stw1.no_coast_stop = True
        self.tg111.stw1.no_quick_stop = True
        self.tg111.stw1.enable_operation = True
        self.tg111.stw1.do_not_reject_traversing_task = True
        self.tg111.stw1.no_intermediate_stop = True

        self.over_v = 100.0
        self.over_acc = 100.0
        self.over_dec = 100.0

        self.base_velocity = 0

        self.edrive = edrive
        if edrive:
            self.edrive.start_io()

    def __del__(self):
        if self.edrive is not None:
            self.tg111.stw1.enable_operation = False
            self.update_outputs(post_wait_ms=0.1)
            self.edrive.stop_io()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trc_bck):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, trc_bck)

        self.__del__()
        return True

    def assert_pnu_integrity(self):
        """Asserts that crucial PNUs have values needed for operability with the motion module."""
        if self.edrive:
            return self.edrive.assert_selected_telegram(111)
        return False

    def scaled_velocity(self, raw_velocity: int) -> int:
        """Convert the raw velocity to a scaled velocity

        Parameters:
            raw_velocity (int): raw velocity to convert to scaled
        """
        return raw_velocity * self.base_velocity / 1073741824.0 \
            if self.base_velocity > 0 else raw_velocity

    def update_inputs(self):
        """Reads current input process data and updates telegram"""
        self.tg111.input_bytes(self.edrive.recv_io())

    def update_outputs(self, post_wait_ms=0):
        """Writes current telegram value to output process data

        Parameters:
            post_wait_ms (int): Optional time in ms that should be waited after writing
        """
        self.edrive.send_io(self.tg111.output_bytes())
        if post_wait_ms:
            time.sleep(post_wait_ms)

    def update_io(self):
        """Updates process data in both directions (I/O)"""
        self.update_inputs()
        self.update_outputs()

# Configuration of options

    def configure_coast_stop(self, active: bool):
        """Configures the coast stop option

        Parameters:
            active (bool): True => activate coasting, False => deactivate coasting
        """
        self.tg111.stw1.no_coast_stop = not active

    def configure_quick_stop(self, active: bool):
        """Configures the quick stop option

        Parameters:
            active (bool): True => activate quick stop, False => deactivate quick stop
        """
        self.tg111.stw1.no_quick_stop = not active

    def configure_hardware_limit_switch(self, active: bool):
        """Configures the hardware limit switch

        Parameters:
            active (bool): True => activate limit, False => deactivate limit
        """
        self.tg111.pos_stw2.activate_hardware_limit_switch = active

    def configure_software_limit_switch(self, active: bool):
        """Configures the software limit switch

        Parameters:
            active (bool): True => activate limit, False => deactivate limit
        """
        self.tg111.pos_stw2.activate_software_limit_switch = active

    def configure_measuring_probe(self, falling_edge: bool = False, measuring_probe: str = 'first'):
        """
        Configures the measuring probes.
        Be aware that only one probe is configurable simultaneously.
        In order to configure both probes:
            1. Configure probe 'first'
            2. Send using update_outputs()
            3. Configure probe 'second'

        Parameters:
            falling_edge (bool): Determines whether to trigger on rising or falling edge
            measuring_probe (str): One of ['first', 'second'], determines the probe to configure
        """
        assert measuring_probe in ['first', 'second']
        self.tg111.pos_stw2.falling_edge_of_measuring_probe = falling_edge
        self.tg111.pos_stw2.measuring_probe2_is_activated = measuring_probe == 'second'

    def configure_continuous_update(self, active: bool):
        """
        Configures the continuous update option i.e. setpoints are immediately updated without need
        of starting a new traversing task

        Parameters:
            active (bool): True => activate continuous update, False => deactivate continuous update
        """
        self.tg111.pos_stw1.continuous_update = active

    def configure_brake(self, active: bool):
        """Configures the holding brake

        Parameters:
            active (bool): True => activate brake, False => release brake
        """
        self.tg111.stw1.open_holding_brake = not active

    def configure_tracking_mode(self, active: bool):
        """Configures the tracking mode i.e. setpoint continuously tracks the current value

        Parameters:
            active (bool): True => activate tracking mode, False => deactivate tracking mode
        """
        self.tg111.pos_stw2.activate_tracking_mode = active

    def configure_traversing_to_fixed_stop(self, active: bool):
        """Configures the traversing to fixed stop option (drive maintains parametrized torque)

        Parameters:
            active (bool): True => activate fixed stop traveling, False => deactivate
        """
        self.tg111.stw2.traversing_fixed_stop = active

# Reading current values
    def plc_control_granted(self) -> bool:
        """Gives information in PLC control is granted

        Returns:
            bool: True if succesful, False otherwise
        """
        logging.info("Check if PLC control is granted")
        self.update_inputs()
        if not self.tg111.zsw1.control_requested:
            logging.error("PLC control denied")
            return False
        logging.info("[bold green]    -> success!", extra={"markup": True})
        return True

    def ready_for_motion(self):
        """Gives information if motion tasks can be started

        Returns:
            bool: True if drive is ready for motion tasks, False otherwise
        """
        if not self.plc_control_granted():
            return False
        logging.info("Check if drive is ready for motion")
        self.update_inputs()
        if not self.tg111.zsw1.operation_enabled:
            logging.error("Drive not ready for motion")
            return False
        logging.info("[bold green]    -> success!", extra={"markup": True})
        return True

    def referenced(self):
        """Gives information if drive is referenced

        Returns:
            bool: True if drive home position is set, False otherwise
        """
        self.update_inputs()
        return self.tg111.zsw1.home_position_set

    def target_position_reached(self):
        """Gives information if drive has reached target position

        Returns:
            bool: True if drive target position is set, False otherwise
        """
        self.update_inputs()
        return self.tg111.zsw1.target_position_reached

    def stopped(self):
        """Gives information if drive is stopped

        Returns:
            bool: True if drive is stopped, False otherwise
        """
        self.update_inputs()
        return self.tg111.zsw1.drive_stopped

    def current_position(self):
        """Read the current position

        Returns:
            int: Current position in user units
        """
        self.update_inputs()
        return self.tg111.xist_a.value

    def current_velocity(self):
        """Read the current velocity

        Returns:
            int/float: In order to get the correct velocity, base_velocity needs to be provided.
                 If no base_velocity is given, returned value is raw and can be converted using
                 the following formula:

                 base_value_velocity = Base Value Velocity (parameterized on device)

                 current_velocity = raw_value * base_value_velocity / 0x40000000.
        """
        self.update_inputs()
        return self.scaled_velocity(self.tg111.nist_b.value)

    def wait_for_condition(self, condition) -> bool:
        """Waits for provided condition to be satisfied

        Parameter:
            condition (function): boolean condition function
        Returns:
            bool: True if succesful, False otherwise
        """
        self.update_inputs()
        while not condition():
            self.update_inputs()
            if self.tg111.zsw1.fault_present:
                logging.error(
                    f"Cancelled due to fault {int(self.tg111.fault_code)}")
                return False

            logging.info(
                f"Target: {int(self.tg111.mdi_tarpos)}, Current: {int(self.tg111.xist_a)}")
            time.sleep(0.1)
        return True

    def wait_for_duration(self, duration: float) -> bool:
        """Waits for provided duration

        Parameter:
            duration (float): time that should be waited for
        Returns:
            bool: True if succesful, False otherwise
        """
        start_time = time.time()

        def cond():
            return time.time() - start_time > duration
        if not self.wait_for_condition(cond):
            return False
        logging.info(f"Duration of {duration} seconds passed")
        return True

    def wait_for_reference(self) -> bool:
        """Waits for drive to be referenced

        Returns:
            bool: True if succesful, False otherwise
        """
        def cond():
            return self.tg111.zsw1.home_position_set
        if not self.wait_for_condition(cond):
            return False
        logging.info("Reference position set")
        return True

    def wait_for_target_position(self) -> bool:
        """Waits for target position to be reached

        Returns:
            bool: True if succesful, False otherwise
        """
        def cond():
            return self.tg111.zsw1.target_position_reached
        if not self.wait_for_condition(cond):
            return False
        logging.info("Target position reached")
        return True

    def wait_for_stop(self) -> bool:
        """Waits for target position to be reached

        Returns:
            bool: True if succesful, False otherwise
        """
        def cond():
            return self.tg111.zsw1.drive_stopped
        if not self.wait_for_condition(cond):
            return False
        logging.info("Drive stopped")
        return True

# Telegram Sequences

    def trigger_record_change(self):
        """Triggers the change to the next record of the record sequence"""
        logging.info("Set record change bit")
        self.tg111.stw1.change_record_no = True
        self.update_outputs(post_wait_ms=0.1)

        # Reset bits
        self.tg111.stw1.change_record_no = False
        self.update_outputs(post_wait_ms=0.1)
        logging.info("Finished record change")

    def acknowledge_faults(self, timeout: float = 5.0) -> bool:
        """Send telegram to request the control of the EDrive

        Parameter:
            timeout (float): time that should be waited for acknowledgement
        Returns:
            bool: True if succesful, False otherwise
        """
        logging.info("Acknowledge any present faults")
        self.tg111.stw1.fault_ack = True
        self.update_outputs(post_wait_ms=0.1)

        self.tg111.stw1.fault_ack = False
        self.update_outputs(post_wait_ms=0.1)

        logging.info("Wait for fault bit to be cleared")
        start_time = time.time()
        while not time.time() - start_time > timeout:
            self.update_inputs()
            if not self.tg111.zsw1.fault_present:
                logging.info("[bold green]    -> success!",
                             extra={"markup": True})
                return True
        logging.error(f"Fault is still present ({int(self.tg111.fault_code)})")
        return False

    def enable_powerstage(self) -> bool:
        """Send telegram to enable the power stage

        Returns:
            bool: True if succesful, False otherwise
        """
        if not self.plc_control_granted():
            return False
        logging.info("Enable Powerstage")

        self.update_inputs()
        if self.tg111.zsw1.operation_enabled:
            # Toggle (in case it is already True)
            self.tg111.stw1.on = False
            self.update_outputs(post_wait_ms=0.1)

        self.tg111.stw1.on = True
        self.update_outputs(post_wait_ms=0.5)

        logging.info("Check if powerstage is enabled")
        self.update_inputs()
        if not self.tg111.zsw1.operation_enabled:
            logging.error("Enabling of powerstage is inhibited")
            return False
        logging.info("[bold green]    -> success!", extra={"markup": True})
        return True

    def stop_motion_task(self):
        """Stops any currently active motion task"""
        logging.info("Stopping motion")
        # Reset activate_traversing_task bit to prepare for next time
        self.tg111.stw1.activate_traversing_task = False

        # Reset jog bits (in case jogging motion was performed)
        self.tg111.stw1.jog1_on = False
        self.tg111.stw1.jog2_on = False

        # Reset referencing bits (in case referencing motion was performed)
        self.tg111.stw1.start_homing_procedure = False
        self.tg111.pos_stw2.set_reference_point = False

        # Actual stop command
        self.tg111.stw1.do_not_reject_traversing_task = False
        self.update_outputs(post_wait_ms=0.1)
        self.tg111.stw1.do_not_reject_traversing_task = True

        self.wait_for_stop()

    def pause_motion_task(self):
        """Pauses any currently active motion task"""
        logging.info("Pausing motion")
        # Reset activate_traversing_task bit to prepare for next time
        self.tg111.stw1.activate_traversing_task = False

        # Actual pause command
        self.tg111.stw1.no_intermediate_stop = False
        self.update_outputs(post_wait_ms=0.1)

        self.wait_for_stop()

    def resume_motion_task(self):
        """Resumes any currently active motion task"""
        logging.info("Resuming motion")
        self.tg111.stw1.no_intermediate_stop = True
        self.update_outputs(post_wait_ms=0.1)

# Motion tasks

    def position_task(self, position: int, velocity: int, absolute: bool = False,
                      nonblocking: bool = False) -> bool:
        """Perform a position task with the given parameters

        Parameters:
            position (int): position setpoint in user units (depends on parametrization)
            velocity (int): velocity setpoint in user units (depends on parametrization)
            absolute (bool): If true, position is considered absolute,
                             otherwise relative to starting position
            nonblocking (bool): If True, tasks returns immediately after starting the task.
                                Otherwise function awaits for finish (or fault).

        Returns:
            bool: True if succesful, False otherwise
        """
        if not self.ready_for_motion():
            return False
        logging.info("Start traversing task")

        self.tg111.mdi_tarpos.value = position
        self.tg111.mdi_velocity.value = velocity
        self.tg111.pos_stw1.activate_mdi = True
        self.tg111.pos_stw1.absolute_position = absolute
        self.tg111.stw1.activate_traversing_task = True
        self.update_outputs()

        if nonblocking:
            return True

        # Wait for task to be started
        time.sleep(0.1)

        if not self.wait_for_target_position():
            return False
        self.stop_motion_task()
        logging.info("Finished position task")
        return True

    def velocity_task(self, velocity: int, duration: float = 0.0) -> bool:
        """Perform a velocity task with the given parameters using setup mode.

        Parameters:
            velocity (int): velocity setpoint in user units (depends on parametrization).
                            The sign determines the direction of the motion.
            duration (float): Optional duration in seconds.
                              A duration of 0 starts the task and returns immediately.

        Returns:
            bool: True if succesful, False otherwise
        """
        if not self.ready_for_motion():
            return False
        logging.info("Start velocity task")

        self.tg111.mdi_velocity.value = abs(velocity)
        self.tg111.pos_stw1.activate_mdi = True
        self.tg111.pos_stw1.absolute_position = True
        self.tg111.pos_stw1.activate_setup = True
        self.tg111.pos_stw1.positioning_direction0 = velocity > 0
        self.tg111.pos_stw1.positioning_direction1 = velocity < 0
        self.tg111.stw1.activate_traversing_task = True
        self.update_outputs()

        if duration == 0:
            return True

        # Wait for task to be started
        time.sleep(0.1)

        if not self.wait_for_duration(duration):
            return False
        self.stop_motion_task()
        logging.info("Finished velocity task")
        return True

    def referencing_task(self, use_homing_method: bool = False, nonblocking: bool = False) -> bool:
        """Perform the referencing sequence. If successful, the drive is referenced afterwards.

        Parameters:
            use_homing_method (bool): If True, the configured homing method is executed.
            nonblocking (bool): If True, tasks returns immediately after starting the task.
                                Otherwise function awaits for finish (or fault).
        Returns:
            bool: True if succesful, False otherwise
        """

        if use_homing_method:
            if not self.ready_for_motion():
                return False
            logging.info("Start homing task using the homing method")
            self.tg111.stw1.start_homing_procedure = True
        else:
            logging.info(
                "Start homing task using current position")
            self.tg111.pos_stw2.set_reference_point = True

        self.update_outputs()

        if nonblocking:
            return True

        # Wait for task to be started
        time.sleep(0.1)

        if not self.wait_for_reference():
            return False
        self.stop_motion_task()
        logging.info("Finished referencing task")
        return True

    def record_task(self, record_number: int, nonblocking: bool = True) -> bool:
        """Perform a preconfigured record task by providing the corresponding record number

        Parameters:
            record_number (int): The record number determining the record table entry that should be
                                 executed.
            nonblocking (bool): If True, tasks returns immediately after starting the task.
                                Otherwise function awaits for finish (or fault).

        Returns:
            bool: True if succesful, False otherwise
        """
        if not self.ready_for_motion():
            return False
        logging.info("Start record task")

        self.tg111.pos_stw1.record_table_selection0 = record_number & 1 > 0
        self.tg111.pos_stw1.record_table_selection1 = record_number & 2 > 0
        self.tg111.pos_stw1.record_table_selection2 = record_number & 4 > 0
        self.tg111.pos_stw1.record_table_selection3 = record_number & 8 > 0
        self.tg111.pos_stw1.record_table_selection4 = record_number & 16 > 0
        self.tg111.pos_stw1.record_table_selection5 = record_number & 32 > 0
        self.tg111.pos_stw1.record_table_selection6 = record_number & 64 > 0
        self.tg111.stw1.activate_traversing_task = True
        self.update_outputs()

        if nonblocking:
            return True

        # Wait for task to be started
        time.sleep(0.1)

        if not self.wait_for_target_position():
            return False
        self.stop_motion_task()
        logging.info("Finished record task")
        return True

    def jog_task(self, jog_positive: bool = True, jog_negative: bool = False,
                 incremental: bool = False, duration: float = 0.0) -> bool:
        """Perform a jogging task with a given duration.
            Please note that the jogging motion stops if jog_positive and jog_negative are equal.

        Parameters:
            jog_positive (bool): If true, jog in positive direction.
            jog_negative (bool): If true, jog in negative direction.

            duration (float): Optional duration in seconds.
                              A duration of 0 starts the task and returns immediately.

        Returns:
            bool: True if succesful, False otherwise
        """
        if not self.ready_for_motion():
            return False
        logging.info("Start jogging task")

        self.tg111.stw1.jog1_on = jog_positive
        self.tg111.stw1.jog2_on = jog_negative
        self.tg111.pos_stw2.incremental_jogging = incremental
        self.update_outputs()

        if duration == 0:
            return True

        if not self.wait_for_duration(duration):
            return False
        self.stop_motion_task()
        logging.info("Finished jogging task")
        return True
