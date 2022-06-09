"""Contains CmmtBase class which contains common code for CMMT communication drivers."""
import logging
import struct


class CmmtBase:
    """Class that contains common functions for CMMT communication drivers."""

    def assert_selected_telegram(self, telegram_id: int):
        """Asserts that the selected telegram is actually configured on the CMMT"""
        # read the currently selected telegram (inst 3490)
        configured_telegram_id = self.read_pnu(3490)

        assert configured_telegram_id == telegram_id, f"Incorrect telegram selected -> " \
            f"Expected: {telegram_id}, Actual: {configured_telegram_id}"

        logging.info(f"Correct telegram selected: {configured_telegram_id}")

    def configure_homing(self, axis_zero_point_offset=1.0):
        """Configures homing procedure"""
        logging.info(
            f"Configure axis zero point offset: {axis_zero_point_offset}")
        self.write_pnu(11734, 0, int(1e9 * axis_zero_point_offset), 'q')

    def read_pnu_raw(self, pnu: int, subindex: int = 0, num_elements: int = 1) -> bytes:
        """Reads a PNU from the CMMT without interpreting the data"""
        raise NotImplementedError

    def read_pnu(self, pnu: int, subindex: int = 0, format_char='h'):
        """Reads a PNU from the CMMT"""
        raw = self.read_pnu_raw(pnu, subindex)
        if format_char == 's':
            param = struct.unpack(f"{len(raw)}s", raw)[0]
        elif format_char == '?':
            param = struct.unpack('b', raw[0:1])[0]
        elif format_char == 'B':
            param = struct.unpack('B', raw[0:1])[0]
        elif format_char == 'b':
            param = struct.unpack('b', raw[0:1])[0]
        else:
            param = struct.unpack(format_char, raw)[0]
        logging.info(
            f"Read PNU {pnu} (subindex: {subindex}): {param} "
            f"(raw: {raw})")
        return param

    def write_pnu_raw(self, pnu: int, subindex: int = 0, num_elements: int = 1,
                      value: bytes = b'\x00'):
        """Writes raw bytes to a PNU on the CMMT"""
        raise NotImplementedError

    def write_pnu(self, pnu: int, subindex: int = 0, value=0, format_char='h'):
        """Writes a value to a PNU to the CMMT"""
        raw = struct.pack(format_char, value)
        self.write_pnu_raw(pnu, subindex, value=raw)
        logging.info(
            f"Written PNU {pnu} (subindex: {subindex}): {value} "
            f"(raw: {raw})")

    def start_io(self, cycle_time: int = 10):
        """Configures and starts i/o data process"""

    def stop_io(self):
        """Stops i/o data process"""

    def send_io(self, data: bytes):
        """Sends data to the output"""
        raise NotImplementedError

    def recv_io(self) -> bytes:
        """Receives data from the input"""
        raise NotImplementedError
