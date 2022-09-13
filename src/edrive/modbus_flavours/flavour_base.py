"""
Contains FlavourBase class which defines the required methods for device flavour classes.
"""


class FlavourBase():
    """Class that defines the interface of flavour classes."""

    def __init__(self, modbus_client):
        self.modbus_client = modbus_client
        self.dev_info_dict = {}

    def device_info(self) -> dict:
        """Executes the device specific sequence to read device info"""
        raise NotImplementedError

    def read_pnu(self, pnu: int, subindex: int = 0, num_elements: int = 1) -> bytes:
        """Executes the device specific sequence to read a PNU"""
        raise NotImplementedError

    def write_pnu(self, pnu: int, subindex: int = 0, num_elements: int = 1,
                  value: bytes = b'\x00') -> bool:
        """Executes the device specific sequence to write a PNU"""
        raise NotImplementedError
