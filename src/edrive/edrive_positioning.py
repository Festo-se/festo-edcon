"""
Contains EDrivePositioning class to configure and control
EDrive devices in position mode.
"""
import time
import traceback
from profidrive.telegram111 import Telegram111
from profidrive.words import OVERRIDE, MDI_ACC, MDI_DEC
from edrive.edrive_base import EDriveBase


class EDrivePositioning:
    """
    This class is used to control the EDrive devices in position mode (telegram 111).
    It provides a set of functions to control the position of the EDrive using different modes.
    """
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
        """Convert the raw velocity to a scaled velocity"""
        return raw_velocity * self.base_speed / 1073741824.0 \
            if self.base_speed > 0 else raw_velocity

    def raw_velocity(self, velocity: int) -> int:
        """Convert the scaled velocity to a raw velocity"""
        return velocity * 1073741824.0 / self.base_speed \
            if self.base_speed > 0 else velocity

    def update_inputs(self):
        """Reads current input process data and updates telegram"""
        self.tg111.input_bytes(self.edrive.recv_io())

    def update_outputs(self, post_wait_ms=0):
        """Writes current telegram value to output process data

        Parameters:
        ------------
            post_wait_ms: int
                          Optional time in ms that should be waited after writing
        """
        self.edrive.send_io(self.tg111.output_bytes())
        if post_wait_ms:
            time.sleep(post_wait_ms)

    def update_io(self):
        """Updates process data in both directions (I/O)"""
        self.update_inputs()
        self.update_outputs()

    def ready_for_motion(self):
        """Gives information if motion tasks can be started"""
        self.update_inputs()
        return self.tg111.zsw1.ready_to_operate

    def current_position(self):
        """Read the current position"""
        self.update_inputs()
        return self.tg111.xist_a.value

    def current_velocity(self):
        """Read the current velocity"""
        self.update_inputs()
        return self.tg111.nist_b.value

    def configure_hardware_limit_switch(self, active):
        """Configures the hardware limit switch"""
        self.tg111.pos_stw2.activate_hardware_limit_switch = active

    def request_plc_control(self) -> bool:
        """Send telegram to request the control of the EDrive"""
        print("Request control by PLC")
        self.tg111.stw1.control_by_plc = True
        self.update_outputs(post_wait_ms=0.1)

        print("Check if PLC control is granted", end='')
        self.update_inputs()
        if not self.tg111.zsw1.control_requested:
            print(" -> failed")
            return False
        print(" -> success!")
        return True

    def acknowledge_faults(self) -> bool:
        """Send telegram to request the control of the EDrive"""
        print("Acknowledge any present faults")
        self.tg111.stw1.fault_ack = True
        self.update_outputs(post_wait_ms=0.1)

        self.tg111.stw1.fault_ack = False
        self.update_outputs(post_wait_ms=0.1)

        print("Check if fault bit is cleared", end='')
        self.update_inputs()
        if self.tg111.zsw1.fault_present:
            print(f" -> is present ({int(self.tg111.fault_code)})")
            return False
        print(" -> success!")
        return True

    def enable_powerstage(self) -> bool:
        """Send telegram to enable the power stage"""
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

    def position_task(self, position: int, velocity: int, absolute: bool = False,
                      setup: bool = False) -> bool:
        """Perform a position task with the given parameters"""
        print("Start traversing task", end='')
        if not self.ready_for_motion():
            print(" -> not ready for motion")
            return False
        print(" -> success!")

        self.tg111.mdi_tarpos.value = position
        self.tg111.mdi_velocity.value = self.raw_velocity(velocity)
        self.tg111.pos_stw1.activate_mdi = True
        self.tg111.pos_stw1.absolute_position = absolute
        self.tg111.pos_stw1.activate_setup = setup
        self.update_outputs(post_wait_ms=0.1)
        self.tg111.stw1.activate_traversing_task = True
        # Wait for traversing task to be started
        self.update_outputs(post_wait_ms=0.1)
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
        self.tg111.pos_stw1.activate_setup = False
        self.update_outputs(post_wait_ms=0.1)
        print("Target position reached")
        return True

    def homing_task(self) -> bool:
        """Perform the homing sequence"""
        print("Start homing task", end='')
        if not self.ready_for_motion():
            print(" -> not ready for motion")
            return False
        print(" -> success!")

        self.tg111.stw1.start_homing_procedure = True
        # Wait for homing task to be started
        self.update_outputs(post_wait_ms=0.1)
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
        self.update_outputs(post_wait_ms=0.1)
        print("Finished homing")
        return True

    def referencing_task(self):
        """Perform the referencing"""
        print("Set reference position")
        self.tg111.pos_stw2.set_reference_point = True
        self.update_outputs(post_wait_ms=0.1)

        # Reset bits
        self.tg111.pos_stw2.set_reference_point = False
        self.update_outputs(post_wait_ms=0.1)
        print("Finished referencing")

    def record_task(self, record_number: int) -> bool:
        """Perform a record task"""
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
        self.update_outputs(post_wait_ms=0.1)
        self.tg111.stw1.activate_traversing_task = True
        # Wait for record task to be started
        self.update_outputs(post_wait_ms=0.1)
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

    def jog_task(self, jog1=True, jog2=False, incremental=False, duration=1.0) -> bool:
        """Perform a jogging task with a given duration"""
        print("Start jogging task", end='')
        if not self.ready_for_motion():
            print(" -> not ready for motion")
            return False
        print(" -> success!")

        self.tg111.stw1.jog1_on = jog1
        self.tg111.stw1.jog2_on = jog2
        self.tg111.pos_stw2.incremental_jogging = incremental
        self.update_outputs(post_wait_ms=duration)

        self.tg111.stw1.jog1_on = False
        self.tg111.stw1.jog2_on = False
        self.update_outputs(post_wait_ms=0.1)
        print("Finished jogging task")
        return True

    def set_config_epos(self, config_epos: bytes):
        """
        Apply the configuration of the EPOS word to the internal telegram
        (ref. SINA_POS by Siemens)
        """
        self.tg111.stw1.no_coast_stop = config_epos[0] & 1 > 0
        self.tg111.stw1.no_quick_stop = config_epos[0] & 2 > 0
        self.tg111.pos_stw2.activate_software_limit_switch = config_epos[0] & 4 > 0
        self.tg111.pos_stw2.activate_hardware_limit_switch = config_epos[0] & 8 > 0
        self.tg111.pos_stw2.falling_edge_of_measuring_probe = config_epos[0] & 16 > 0
        self.tg111.pos_stw2.measuring_probe2_is_activated = config_epos[0] & 32 > 0
        self.tg111.stw1.change_record_no = config_epos[0] & 64 > 0
        self.tg111.pos_stw2.reserved1 = config_epos[0] & 128 > 0
        self.tg111.pos_stw1.continuous_update = config_epos[1] & 1 > 0
        self.tg111.stw2.reserved1 = config_epos[1] & 2 > 0
        self.tg111.stw2.reserved2 = config_epos[1] & 4 > 0
        self.tg111.stw2.reserved3 = config_epos[1] & 8 > 0
        self.tg111.stw2.reserved4 = config_epos[1] & 16 > 0
        self.tg111.stw2.reserved5 = config_epos[1] & 32 > 0
        self.tg111.stw2.parking_axis = config_epos[1] & 64 > 0
        self.tg111.stw1.open_holding_brake = config_epos[1] & 128 > 0
        self.tg111.stw1.reserved1 = config_epos[2] & 1 > 0
        self.tg111.stw1.reserved2 = config_epos[2] & 2 > 0
        self.tg111.pos_stw2.activate_tracking_mode = config_epos[2] & 4 > 0
        self.tg111.pos_stw1.reserved1 = config_epos[2] & 8 > 0
        self.tg111.pos_stw1.reserved2 = config_epos[2] & 16 > 0
        self.tg111.pos_stw1.reserved3 = config_epos[2] & 32 > 0
        self.tg111.pos_stw2.reserved9 = config_epos[2] & 64 > 0
        self.tg111.pos_stw2.reserved3 = config_epos[2] & 128 > 0
        self.tg111.pos_stw2.reserved4 = config_epos[3] & 1 > 0
        self.tg111.pos_stw2.reserved5 = config_epos[3] & 2 > 0
        self.tg111.pos_stw2.reserved8 = config_epos[3] & 4 > 0
        self.tg111.pos_stw2.reserved9 = config_epos[3] & 8 > 0
        self.tg111.stw2.reserved6 = config_epos[3] & 16 > 0
        self.tg111.stw2.reserved7 = config_epos[3] & 32 > 0
        self.tg111.stw2.traversing_fixed_stop = config_epos[3] & 64 > 0
        self.tg111.stw2.reserved8 = config_epos[3] & 128 > 0
