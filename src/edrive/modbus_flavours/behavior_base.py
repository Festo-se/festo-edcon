"""
Contains BehaviorBase class which defines the required methods for device behavior classes.
"""


class BehaviorBase():
    """Class that defines the interface of behavior classes."""

    def __init__(self, modbus_client):
        self.modbus_client = modbus_client

    def read_pnu(self, pnu: int, subindex: int = 0, num_elements: int = 1):
        """Executes the device specific sequence to read a PNU"""
        raise NotImplementedError

    def write_pnu(self, pnu: int, subindex: int = 0, num_elements: int = 1,
                  value: bytes = b'\x00'):
        """Executes the device specific sequence to write a PNU"""
        raise NotImplementedError
