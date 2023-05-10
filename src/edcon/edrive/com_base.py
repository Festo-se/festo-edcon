"""Contains ComBase class which contains common code for EDrive communication drivers."""
import logging
from edcon.edrive.pnu_packing import pnu_pack, pnu_unpack


class ComBase:
    """Class that contains common functions for EDrive communication drivers."""

    def validate_selected_telegram(self, telegram_id: int):
        """Asserts that the selected telegram is actually configured on the EDrive"""
        # read the currently selected telegram (PNU 3490)
        configured_telegram_id = self.read_pnu(3490)

        if not configured_telegram_id:
            logging.warning("Could not verify correct telegram via PNU")
            return False

        assert configured_telegram_id == telegram_id, f"Incorrect telegram selected -> " \
            f"Expected: {telegram_id}, Actual: {configured_telegram_id}"
        logging.info(
            f"Correct telegram selected: {configured_telegram_id}")
        return True

    def read_pnu_raw(self, pnu: int, subindex: int = 0, num_elements: int = 1) -> bytes:
        """Reads a PNU from the EDrive without interpreting the data"""
        raise NotImplementedError

    def read_pnu(self, pnu: int, subindex: int = 0, forced_format=None):
        """Reads a PNU from the EDrive"""
        raw = self.read_pnu_raw(pnu, subindex)
        if raw:
            param = pnu_unpack(pnu, raw, forced_format)
            logging.info(f"Unpacked {raw} to {param}")

            return param

        logging.error(f"PNU {pnu} read failed")
        return None

    def write_pnu_raw(self, pnu: int, subindex: int = 0, num_elements: int = 1,
                      value: bytes = b'\x00') -> bool:
        """Writes raw bytes to a PNU on the EDrive"""
        raise NotImplementedError

    def write_pnu(self, pnu: int, subindex: int = 0, value=0, forced_format=None) -> bool:
        """Writes a value to a PNU to the EDrive"""
        raw = pnu_pack(pnu, value, forced_format)
        logging.info(f"Packed {value} to {raw}")
        if self.write_pnu_raw(pnu, subindex, value=raw):
            return True
        logging.error(f"PNU {pnu} write failed")
        return False

    def start_io(self):
        """Configures and starts i/o data process"""

    def stop_io(self):
        """Stops i/o data process"""

    def send_io(self, data: bytes, nonblocking: bool = False):
        """Sends data to the output

        Parameters:
            nonblocking (bool): If True, tasks returns immediately after starting the task.
                                Otherwise function awaits for finish (or fault).
        """
        raise NotImplementedError

    def recv_io(self, nonblocking: bool = False) -> bytes:
        """Receives data from the input

        Parameters:
            nonblocking (bool): If True, tasks returns immediately after starting the task.
                                Otherwise function awaits for finish (or fault).
        """
        raise NotImplementedError
