
"""
Contains ParameterSet class which is used to represent parameter sets of EDrives.
"""
from edcon.utils.logging import Logging
from edcon.edrive.com_base import ComBase
from edcon.edrive.parameter_mapping import PnuMap

class ParameterValidator:
    """Class representing a parameter set."""
    @staticmethod
    def validate(com: ComBase, pnu: int, value) -> bool:
        """Asserts that the provided pnu is actually configured"""
        pnu_map = PnuMap()
        pnu_data_type = pnu_map[pnu].data_type
        pnu_name = pnu_map[pnu].name
        Logging.logger.info(f"Try to validate PNU {pnu} ({pnu_name}) of type {pnu_data_type}")

        configured_value = com.read_pnu(pnu)
        if not configured_value:
            Logging.logger.error(f"Could not validate {pnu} ({pnu_name})")
            return False

        assert configured_value == value, \
            f"Incorrect value configured on {pnu} ({pnu_name}) -> " \
            f"Expected: {value}, Actual: {configured_value}"
        Logging.logger.info(f"Correct value configured on {pnu} ({pnu_name}): {configured_value}")
        return True
