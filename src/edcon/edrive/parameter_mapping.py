"""Contains functions which provide mapping of PNU types."""
from collections import namedtuple
from importlib.resources import files
from functools import lru_cache
import csv


@lru_cache
def read_pnu_map_file(pnu_map_file: str = None):
    """Creates a dict based on a provided PNU type map file

    Parameters:
        pnu_map_file (str): Optional file to use for mapping. 
                                If nothing provided try to load mapping shipped with package.
    Returns:
        dict: With the first column values as keys and namedtuple values
    """
    if not pnu_map_file:
        pnu_map_file = files('edcon.edrive.data').joinpath('pnu_map.csv')
    with open(pnu_map_file, encoding='ascii') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        # Define a namedtuple where the header row determines the field names
        pnu_map_item = namedtuple('pnu_map_item', next(reader, None))
        return [pnu_map_item(*row) for row in reader]


class ParameterMap:
    """Class that provides a mapping from parameter id to pnu_map_item."""

    def __init__(self) -> None:
        pnu_list = read_pnu_map_file()
        self.mapping = {item.parameter_id: item for item in pnu_list}

    def __getitem__(self, parameter_id: str):
        """Determines the corresponding pnu_map_item from a provided parameter id

        Parameters:
            parameter_id (str): Parameter id of the PNU type to be determined.
        Returns:
            value: pnu_map_item
        """
        axis, parameter_id, instance, _ = parameter_id.strip('P').split('.')
        return self.mapping[f'{axis}.{parameter_id}.{instance}']

    def __len__(self):
        return len(self.mapping)


class PnuMap:
    """Class that provides a mapping from PNU to pnu_map_item."""

    def __init__(self) -> None:
        pnu_list = read_pnu_map_file()
        self.mapping = {int(item.pnu): item for item in pnu_list}

    def __getitem__(self, pnu: int):
        """Determines the corresponding pnu_map_item from a provided PNU number

        Parameters:
            pnu (int): PNU number.
        Returns:
            value: pnu_map_item
        """
        return self.mapping[pnu]

    def __len__(self):
        return len(self.mapping)
