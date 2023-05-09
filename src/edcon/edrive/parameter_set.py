
"""
Contains ParameterSet class which is used to represent parameter sets of EDrives.
"""

from collections import namedtuple


class ParameterSet:
    """Class representing a parameter set."""

    def __init__(self, parameterset_file) -> None:
        parameter_item = namedtuple(
            'parameter_item', ['axis', 'uid', 'instance', 'subindex', 'value'])

        self.parameters = {}
        with open(parameterset_file, 'rb') as pfile:
            lines = pfile.readlines()

        start_idx = lines.index(b'----\r\n') + 1
        end_idx = start_idx + lines[start_idx:].index(b'----\r\n')

        for item in lines[start_idx:end_idx]:
            key, hex_value = item.decode().strip('P').split(';')

            axis, uid, instance, subindex = key.split('.')
            value = bytes.fromhex(hex_value.split('x')[1])

            self.parameters[key] = parameter_item(
                axis, uid, instance, subindex, value)

    def __getitem__(self, item):
        return self.parameters[item.strip('P')]

    def __setitem__(self, item, value):
        self.parameters[item.strip('P')] = value
