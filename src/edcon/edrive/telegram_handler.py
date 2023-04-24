"""Class definition containing generic telegram execution functions."""

import time
import traceback
import logging
from edcon.utils.func_helpers import func_sequence, wait_until


class TelegramHandler:
    """Basic class for executing telegrams."""

    def __init__(self, telegram, edrive) -> None:
        self.telegram = telegram

        # Configure generic values of the telegram
        self.telegram.stw1.control_by_plc = True
        self.telegram.stw1.no_coast_stop = True
        self.telegram.stw1.no_quick_stop = True
        self.telegram.stw1.enable_operation = True

        # Telegram 1/102
        # self.telegram.stw1.enable_ramp_generator = True
        # self.telegram.stw1.unfreeze_ramp_generator = True

        self.edrive = edrive
        # Start process data
        self.edrive.start_io()

    def __del__(self):
        if self.edrive is not None:
            self.telegram.stw1.enable_operation = False
            self.edrive.send_io(self.telegram.output_bytes())
            time.sleep(0.1)
            self.edrive.stop_io()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trc_bck):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, trc_bck)

        self.__del__()
        return True

    def update_inputs(self):
        """Reads current input process data and updates telegram"""
        self.telegram.input_bytes(self.edrive.recv_io())

    def update_outputs(self):
        """Writes current telegram value to output process data
        """
        self.edrive.send_io(self.telegram.output_bytes())

    def update_io(self):
        """Updates process data in both directions (I/O)"""
        self.update_inputs()
        self.update_outputs()

    def fault_string(self) -> str:
        """Returns string containing fault reason

        Returns:
            str: String containing the fault reason
        """
        return "Unknown fault"

    def fault_present(self) -> bool:
        """Gives information whether a fault is present

        Returns:
            bool: True if fault presens, False otherwise
        """
        self.update_inputs()
        if self.telegram.zsw1.fault_present:
            logging.error("Fault bit is present")
            return True
        return False

    def plc_control_granted(self) -> bool:
        """Gives information if PLC control is granted

        Returns:
            bool: True if succesful, False otherwise
        """
        logging.info("Check if PLC control is granted")

        self.update_inputs()
        if not self.telegram.zsw1.control_requested:
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
        if not self.telegram.zsw1.operation_enabled:
            logging.error("Drive not ready for motion")
            return False
        logging.info("[bold green]    -> success!", extra={"markup": True})
        return True

    def configure_coast_stop(self, active: bool):
        """Configures the coast stop option

        Parameters:
            active (bool): True => activate coasting, False => deactivate coasting
        """
        self.telegram.stw1.no_coast_stop = not active

    def configure_quick_stop(self, active: bool):
        """Configures the quick stop option

        Parameters:
            active (bool): True => activate quick stop, False => deactivate quick stop
        """
        self.telegram.stw1.no_quick_stop = not active

    def configure_brake(self, active: bool):
        """Configures the holding brake

        Parameters:
            active (bool): True => activate brake, False => release brake
        """
        self.telegram.stw1.open_holding_brake = not active

    def acknowledge_faults(self, timeout: float = 5.0) -> bool:
        """Send telegram to acknowledge present faults of the EDrive

        Parameter:
            timeout (float): time that should be waited for acknowledgement

        Returns:
            bool: True if succesful, False otherwise
        """
        logging.info("Acknowledge any present faults")

        def toggle_func(value):
            self.telegram.stw1.fault_ack = value
            self.update_outputs()

        func_sequence(toggle_func, [True, False])

        def cond():
            return not self.telegram.zsw1.fault_present

        if not wait_until(cond, self.fault_present, timeout,
                          error_string=self.fault_string):
            return False

        logging.info("[bold green]    -> success!", extra={"markup": True})
        return True

    def enable_powerstage(self, timeout: float = 1.0) -> bool:
        """Send telegram to enable the power stage

        Parameter:
            timeout (float): time that should be waited for enabling

        Returns:
            bool: True if succesful, False otherwise
        """
        if not self.plc_control_granted():
            return False
        logging.info("Enable powerstage")

        # Toggle to low (in case it is already True)
        def toggle_func(value):
            self.telegram.stw1.on = value
            self.update_outputs()

        func_sequence(toggle_func, [False, True])

        def cond():
            return self.telegram.zsw1.operation_enabled

        if not wait_until(cond, self.fault_present, timeout,
                          error_string=self.fault_string):
            logging.error("Operation inhibited")
            return False

        logging.info("[bold green]    -> success!", extra={"markup": True})
        return True

    def disable_powerstage(self) -> bool:
        """Send telegram to disable the power stage"""
        logging.info("Disable powerstage")
        self.telegram.stw1.on = False
        self.update_outputs()
