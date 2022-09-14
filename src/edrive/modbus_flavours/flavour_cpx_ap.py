"""
Contains FlavourCpxAp class which contains the specific flavour for CPX-AP drives.
"""
import logging

from edrive.modbus_flavours.flavour_base import FlavourBase


class FlavourCpxAp(FlavourBase):
    """Class that contains the device specific access sequences for CPX-AP drives."""

    def device_info(self):
        if self.dev_info_dict:
            return self.dev_info_dict

        self.dev_info_dict = {"pd_in_addr": 5000,
                              "pd_out_addr": 0,
                              "timeout_addr": 14000,
                              "pd_size": 56  # Read from modbus register
                              }

        # Read device information

        return self.dev_info_dict

    def read_pnu(self, pnu: int, subindex: int = 0, num_elements: int = 1) -> bytes:
        logging.error("Could not access PNU register")

    def write_pnu(self, pnu: int, subindex: int = 0, num_elements: int = 1,
                  value: bytes = b'\x00') -> bool:
        logging.error("Could not access PNU register")
        return False
