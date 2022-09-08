"""
Contains EDriveMotion class to configure and control
EDrive devices in position mode.
"""
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

        self.base_speed = 0

        self.edrive = edrive
        if edrive:
            self.edrive.assert_selected_telegram(111)
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

    def scaled_velocity(self, raw_velocity: int) -> int:
        """Convert the raw velocity to a scaled velocity

        Parameters:
            raw_velocity (int): raw velocity to convert to scaled
        """
        return raw_velocity * self.base_speed / 1073741824.0 \
            if self.base_speed > 0 else raw_velocity

    def raw_velocity(self, velocity: int) -> int:
        """
        Convert the scaled velocity to a raw velocity

        Parameters:
            velocity (int): scaled velocity to convert to raw
        """
        return velocity * 1073741824.0 / self.base_speed \
            if self.base_speed > 0 else velocity

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
        print("Check if PLC control is granted", end='')
        self.update_inputs()
        if not self.tg111.zsw1.control_requested:
            print(" -> failed")
            return False
        print(" -> success!")
        return True

    def ready_for_motion(self):
        """Gives information if motion tasks can be started

        Returns:
            bool: True if ready to operate, False otherwise
        """
        if not self.plc_control_granted():
            return False
        print("Check if drive is ready for motion", end='')
        self.update_inputs()
        return self.tg111.zsw1.ready_to_operate

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
            int: Current velocity unit is in percent of base speed if given.
                 If no base_speed is given, value is in user units scaled by the parametrized
                 base speed / 0x4000.
        """
        self.update_inputs()
        return self.scaled_velocity(self.tg111.nist_b.value)

# Telegram Sequences

    def trigger_record_change(self):
        """Triggers the change to the next record of the record sequence"""
        print("Set record change bit")
        self.tg111.stw1.change_record_no = True
        self.update_outputs(post_wait_ms=0.1)

        # Reset bits
        self.tg111.stw1.change_record_no = False
        self.update_outputs(post_wait_ms=0.1)
        print("Finished record change")

    def acknowledge_faults(self, timeout: float = 5.0) -> bool:
        """Send telegram to request the control of the EDrive

        Parameter:
            timeout (float): time that should be waited for acknowledgement
        Returns:
            bool: True if succesful, False otherwise
        """
        print("Acknowledge any present faults")
        self.tg111.stw1.fault_ack = True
        self.update_outputs(post_wait_ms=0.1)

        self.tg111.stw1.fault_ack = False
        self.update_outputs(post_wait_ms=0.1)

        print("Wait for fault bit to be cleared", end='')
        start_time = time.time()
        while not time.time() - start_time > timeout:
            self.update_inputs()
            if not self.tg111.zsw1.fault_present:
                print(" -> success!")
                return True
        print(f" -> is still present ({int(self.tg111.fault_code)})")
        return False

    def enable_powerstage(self) -> bool:
        """Send telegram to enable the power stage

        Returns:
            bool: True if succesful, False otherwise
        """
        if not self.plc_control_granted():
            return False
        print("Enable Powerstage")
        # Toggle (in case it is already True)
        self.tg111.stw1.on = False
        self.update_outputs(post_wait_ms=0.1)
        self.tg111.stw1.on = True
        self.update_outputs(post_wait_ms=0.5)

        print("Check if powerstage is enabled", end='')
        self.update_inputs()
        if not self.tg111.zsw1.ready_to_switch_on:
            print(" -> inhibited")
            return False
        print(" -> success!")
        return True

    def stop_motion_task(self):
        """Stops any currently active motion task"""

        # Reset bits
        self.tg111.pos_stw1.activate_mdi = False
        self.tg111.pos_stw1.absolute_position = False
        self.tg111.pos_stw1.activate_setup = False
        self.tg111.pos_stw1.positioning_direction0 = False
        self.tg111.pos_stw1.positioning_direction1 = False
        self.tg111.stw1.activate_traversing_task = False
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
        print("Start traversing task", end='')
        if not self.ready_for_motion():
            print(" -> not ready for motion")
            return False
        print(" -> success!")

        self.tg111.mdi_tarpos.value = position
        self.tg111.mdi_velocity.value = self.raw_velocity(velocity)
        self.tg111.pos_stw1.activate_mdi = True
        self.tg111.pos_stw1.absolute_position = absolute
        self.tg111.stw1.activate_traversing_task = True
        self.update_outputs()

        if nonblocking:
            return True

        # Wait for traversing task to be started
        time.sleep(0.1)
        self.update_inputs()

        while not self.tg111.zsw1.target_position_reached:
            self.update_inputs()
            if self.tg111.zsw1.fault_present:
                print(
                    f"Cancelled task due to fault {int(self.tg111.fault_code)}")
                return False

            print(
                f"Target: {int(self.tg111.mdi_tarpos)}, Current: {int(self.tg111.xist_a)}")
            time.sleep(0.1)

        # Reset bits
        self.tg111.pos_stw1.activate_mdi = False
        self.tg111.stw1.activate_traversing_task = False
        self.update_outputs(post_wait_ms=0.1)
        print("Target position reached")
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
        print("Start velocity task", end='')
        if not self.ready_for_motion():
            print(" -> not ready for motion")
            return False
        print(" -> success!")

        self.tg111.mdi_velocity.value = self.raw_velocity(abs(velocity))
        self.tg111.pos_stw1.activate_mdi = True
        self.tg111.pos_stw1.absolute_position = True
        self.tg111.pos_stw1.activate_setup = True
        self.tg111.pos_stw1.positioning_direction0 = velocity > 0
        self.tg111.pos_stw1.positioning_direction1 = velocity < 0
        self.tg111.stw1.activate_traversing_task = True
        self.update_outputs()

        if duration == 0:
            return True

        # Wait for traversing task to be started
        time.sleep(0.1)
        self.update_inputs()

        start_time = time.time()
        while not time.time() - start_time > duration:
            self.update_inputs()
            if self.tg111.zsw1.fault_present:
                print(
                    f"Cancelled task due to fault {int(self.tg111.fault_code)}")
                return False

            print(
                f"Target: {int(self.scaled_velocity(self.tg111.mdi_velocity))}, "
                f"Current: {self.current_velocity()}")
            time.sleep(0.1)

        # Reset bits
        self.tg111.pos_stw1.activate_mdi = False
        self.tg111.pos_stw1.absolute_position = False
        self.tg111.pos_stw1.activate_setup = False
        self.tg111.pos_stw1.positioning_direction0 = False
        self.tg111.pos_stw1.positioning_direction1 = False
        self.tg111.stw1.activate_traversing_task = False
        self.update_outputs(post_wait_ms=0.1)

        # Wait for drive to finish motion
        while not self.tg111.zsw1.drive_stopped:
            self.update_inputs()
            if self.tg111.zsw1.fault_present:
                print(
                    f"Cancelled task due to fault {int(self.tg111.fault_code)}")
                return False
            print(
                f"Target: {int(self.tg111.mdi_velocity)}, Current: {self.current_velocity()}")
            time.sleep(0.1)

        print("Finished velocity task")
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
            print("Start homing task using the homing method", end='')
            if not self.ready_for_motion():
                print(" -> not ready for motion")
                return False
            print(" -> success!")
            self.tg111.stw1.start_homing_procedure = True
        else:
            print("Start homing task using current position -> success!")
            self.tg111.pos_stw2.set_reference_point = True

        self.update_outputs()

        if nonblocking:
            return True

        # Wait for homing task to be started
        time.sleep(0.1)
        self.update_inputs()

        while not self.tg111.zsw1.home_position_set:
            self.update_inputs()
            if self.tg111.zsw1.fault_present:
                print(
                    f"Cancelled task due to fault {int(self.tg111.fault_code)}")
                return False
            time.sleep(0.1)

        # Reset bits
        self.tg111.stw1.start_homing_procedure = False
        self.tg111.pos_stw2.set_reference_point = False
        self.update_outputs(post_wait_ms=0.1)
        print("Finished homing")
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
        print("Start record task", end='')
        if not self.ready_for_motion():
            print(" -> not ready for motion")
            return False
        print(" -> success!")

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

        # Wait for record task to be started
        time.sleep(0.1)
        self.update_inputs()

        while not self.tg111.zsw1.target_position_reached:
            self.update_inputs()
            if self.tg111.zsw1.fault_present:
                print(
                    f"Cancelled task due to fault {int(self.tg111.fault_code)}")
                return False
            time.sleep(0.1)

        # Reset bits
        self.tg111.stw1.activate_traversing_task = False
        self.update_outputs(post_wait_ms=0.1)
        print("Finished record task")
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
        print("Start jogging task", end='')
        if not self.ready_for_motion():
            print(" -> not ready for motion")
            return False
        print(" -> success!")

        self.tg111.stw1.jog1_on = jog_positive
        self.tg111.stw1.jog2_on = jog_negative
        self.tg111.pos_stw2.incremental_jogging = incremental
        self.update_outputs()

        if duration == 0:
            return True

        time.sleep(duration)

        self.tg111.stw1.jog1_on = False
        self.tg111.stw1.jog2_on = False
        self.update_outputs(post_wait_ms=0.1)
        print("Finished jogging task")
        return True
