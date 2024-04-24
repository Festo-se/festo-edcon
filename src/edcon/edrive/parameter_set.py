"""
Contains ParameterSet class which is used to represent parameter sets of EDrives.
"""

from edcon.edrive.parameter import Parameter
from edcon.edrive.parameter_mapping import ParameterMap
from edcon.utils.logging import Logging


class ParameterSet:
    """Class representing a parameter set."""

    def __init__(self, parameterset_file, strip_null_terminators=True) -> None:
        self.parameters = []
        with open(parameterset_file, "rb") as pfile:
            lines = pfile.readlines()

        start_idx = lines.index(b"----\r\n") + 1
        end_idx = start_idx + lines[start_idx:].index(b"----\r\n")

        for item in lines[start_idx:end_idx]:
            key, hex_value = item.decode().strip("P").split(";")
            value_raw = bytes.fromhex(hex_value.split("x")[1])[::-1]

            self.parameters.append(Parameter.from_uid_raw(key, value_raw))

        if strip_null_terminators:
            Logging.logger.info("Stripping null terminators from parameter set")
            self.strip_null_terminators()

    def __iter__(self):
        return iter(self.parameters)

    def __len__(self):
        return len(self.parameters)

    def _is_parameter_null_terminator(self, parameter: Parameter):
        """Determines if the parameter is a null terminator.

        Returns:
            bool: True if the parameter is a null terminator
        """
        parameter_map = ParameterMap()
        if not parameter.uid() in parameter_map:
            return None

        data_type = parameter_map[parameter.uid()].data_type
        if "STRING" in data_type:
            last_index = int(data_type.strip("STRING()")) - 1
            if parameter.subindex == last_index:
                Logging.logger.debug(
                    f"Parameter {parameter.uid()} is a null terminator"
                )
                return True
        return False

    def strip_null_terminators(self):
        """Removes all parameters from the parameter set that represent null terminators."""
        self.parameters = list(
            filter(lambda v: not self._is_parameter_null_terminator(v), self.parameters)
        )
