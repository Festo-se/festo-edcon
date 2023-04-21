import time
import traceback
import logging
from collections.abc import Callable


class TelegramExecutor:
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
        return "Unknown"

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

    def plc_control_granted(self) -> bool:
        """Gives information in PLC control is granted

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

    def wait_for_condition(self, condition: Callable[[], bool] = None, timeout: float = 0.0,
                           info_string: Callable[[], str] = None) -> bool:
        """Waits for provided condition to be satisfied

        Parameter:
            condition (Callable): boolean condition function
            timeout (float): Time that should be waited for condition to be satisfied (in seconds)
            info_string (Callable): optional callback for string to print during wait process

        Returns:
            bool: True if succesful, False otherwise
        """
        start_time = time.time()
        while timeout == 0.0 or not time.time() - start_time > timeout:
            self.update_inputs()
            if condition and condition():
                return True
            if self.telegram.zsw1.fault_present:
                logging.error(self.fault_string())
                return False
            if info_string:
                logging.info(info_string())
        logging.error(f"Cancelled due to timeout after {timeout} s")
        return False

    def wait_for_duration(self, duration: float, info_string: Callable[[], str] = None) -> bool:
        """Waits for provided duration

        Parameter:
            duration (float): time that should be waited for
            info_string (Callable): optional callback for string to print during wait process

        Returns:
            bool: True if succesful, False otherwise
        """
        start_time = time.time()
        while duration == 0.0 or not time.time() - start_time > duration:
            self.update_inputs()
            if self.telegram.zsw1.fault_present:
                logging.error(self.fault_string())
                return False
            if info_string:
                logging.info(info_string())
        logging.info(f"Duration of {duration} seconds passed")
        return True

    def pulse_bit(self, toggle_func: Callable[[bool], None],
                  active_high: bool = True, pulse_width: float = 0.1):
        """Performs a toggling sequence on a provided toggle function

        Parameter:
            toggle_func (Callable): toggle function that changes a boolean value
            active_high (bool): Determines the direction of the pulse (positive or negative)
            active_high (float): Determines the width of the pulse in seconds
        """
        toggle_func(active_high)
        self.update_outputs()

        # Wait for trigger
        time.sleep(pulse_width)

        # Reset bits
        toggle_func(not active_high)
        self.update_outputs()

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

        self.pulse_bit(toggle_func)

        def cond():
            return not self.telegram.zsw1.fault_present

        if not self.wait_for_condition(cond, timeout):
            logging.error(
                f"Fault code: ({int(self.telegram.fault_code)})")
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

        self.pulse_bit(toggle_func, active_high=False)

        def cond():
            return self.telegram.zsw1.operation_enabled

        if not self.wait_for_condition(cond, timeout):
            logging.error("Operation inhibited")
            return False

        logging.info("[bold green]    -> success!", extra={"markup": True})
        return True

    def disable_powerstage(self) -> bool:
        """Send telegram to disable the power stage"""
        logging.info("Disable powerstage")
        self.telegram.stw1.on = False
        self.update_outputs()
