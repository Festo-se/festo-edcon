"""
Contains ParameterSet class which is used to represent parameter sets of EDrives.
"""

from typing import Any
from edcon.utils.logging import Logging
from edcon.edrive.com_base import ComBase
from edcon.edrive.parameter_mapping import ParameterMap
from edcon.edrive.parameter import Parameter


class ParameterHandler:
    """Class for parameter handling activities."""

    def __init__(self, com: ComBase):
        self.com = com
        self.parameter_map = ParameterMap()

    def _check_parameter_uid(self, parameter_uid: str):
        if parameter_uid in self.parameter_map:
            return True
        Logging.logger.warning(
            f"Skipping parameter {parameter_uid} as it is not available in parameter_map.\n"
            f"Possible remedies:\n"
            f"1. Upgrade the parameter map (by upgrading the python package).\n"
            f"2. Downgrade the firmware version and corresponding parameter set."
        )
        return False

    def validate(self, parameter_uid: str, value: Any) -> bool:
        """Asserts that the provided pnu is actually configured"""
        if not self._check_parameter_uid(parameter_uid):
            return False
        pnu = int(self.parameter_map[parameter_uid].pnu)
        pnu_name = self.parameter_map[parameter_uid].name
        pnu_data_type = self.parameter_map[parameter_uid].data_type
        Logging.logger.info(
            f"Try to validate PNU {pnu} ({pnu_name}) of type {pnu_data_type}"
        )

        configured_value = self.com.read_pnu(pnu)
        if not configured_value:
            Logging.logger.error(f"Could not validate PNU {pnu} ({pnu_name})")
            return False

        assert configured_value == value, (
            f"Incorrect value configured on {pnu} ({pnu_name}) -> "
            f"Expected: {value}, Actual: {configured_value}"
        )
        Logging.logger.info(
            f"Correct value configured on {pnu} ({pnu_name}): {configured_value}"
        )
        return True

    def read(self, parameter_uid: str, subindex: int = 0):
        """Read value from parameter_uid"""
        if not self._check_parameter_uid(parameter_uid):
            return False
        pnu = self.parameter_map[parameter_uid].pnu
        value_raw = self.com.read_pnu_raw(pnu=pnu, subindex=subindex)
        return Parameter.from_uid_raw(parameter_uid, value_raw)

    def write(self, parameter: Parameter) -> bool:
        """Write value to parameter_uid"""
        if not self._check_parameter_uid(parameter.uid()):
            return False
        pnu = self.parameter_map[parameter.uid()].pnu
        return self.com.write_pnu_raw(
            pnu=pnu, subindex=parameter.subindex, value=parameter.value_raw
        )
