"""
Contains Parameter class which is used to represent a parameter of EDrives.
"""

from dataclasses import dataclass
from typing import Any
from edcon.edrive.parameter_mapping import ParameterMap
from edcon.edrive.pnu_packing import pnu_pack, pnu_unpack


@dataclass
class Parameter:
    """Class representing a parameter."""

    axis: int
    data_id: int
    instance: int
    subindex: int
    value_raw: bytes

    @classmethod
    def from_uid(cls, uid: str, value: Any):
        """Function to create a Parameter by providing a uid and value.

        Parameters:
            uid (str): uid of the parameter
            value (Any): value of the parameter

        Returns:
            Parameter object
        """
        axis, data_id, instance, subindex = uid.strip("P").split(".")
        inst = cls(int(axis), int(data_id), int(instance), int(subindex), None)
        inst.value = value
        return inst

    @classmethod
    def from_uid_raw(cls, uid: str, value_raw: bytes):
        """Function to create a Parameter by providing a uid and value.

        Parameters:
            uid (str): uid of the parameter
            value_raw (bytes): value of the parameter

        Returns:
            Parameter object
        """
        axis, data_id, instance, subindex = uid.strip("P").split(".")
        return cls(int(axis), int(data_id), int(instance), int(subindex), value_raw)

    @property
    def value(self) -> Any:
        """Returns the value of the parameter.

        Returns:
            Any: Value in correct data type
        """
        parameter_map = ParameterMap()
        pnu = parameter_map[self.uid()].pnu
        return pnu_unpack(pnu, self.value_raw)

    @value.setter
    def value(self, value: Any):
        parameter_map = ParameterMap()
        pnu = parameter_map[self.uid()].pnu
        self.value_raw = pnu_pack(pnu, value)

    def uid(self) -> str:
        """Returns the uid of the parameter.

        Returns:
            str: uid
        """
        return f"{self.axis}.{self.data_id}.{self.instance}.{self.subindex}"
