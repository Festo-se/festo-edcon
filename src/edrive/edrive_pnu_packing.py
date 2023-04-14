"""Contains functions which provide mapping of PNU types."""
from collections import namedtuple
from importlib.resources import files
from functools import lru_cache
import csv
import struct
import logging

PNU_TYPE_TO_FORMAT_CHAR = {
    'BOOL': '?',
    'SINT': 'b',
    'INT': 'h',
    'DINT': 'i',
    'LINT': 'q',
    'USINT': 'B',
    'UINT': 'H',
    'UDINT': 'I',
    'ULINT': 'Q',
    'REAL': 'f'
}


@lru_cache
def read_pnu_type_map_file(pnu_type_map_file: str = None):
    """Creates a dict based on a provided PNU type map file

    Parameters:
        pnu_type_map_file (str): Optional file to use for mapping. 
                                 If nothing provided try to load mapping shipped with package.
    Returns:
        dict: With the first column values as keys and namedtuple values
    """
    if not pnu_type_map_file:
        pnu_type_map_file = files('edrive.data').joinpath('pnu_type_map.csv')

    with open(pnu_type_map_file, encoding='ascii') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        # Define a namedtuple where the header row determines the field names
        pnu_item = namedtuple('pnu_item', next(reader, None))
        # Create a dict where the first column determines the key
        pnu_type_dict = {int(row[0]): pnu_item(*row) for row in reader}
    return pnu_type_dict


def pnu_unpack(pnu: int, raw: bytes, forced_format: str = None, pnu_type_map_file: str = None):
    """Unpacks a raw byte value to specific type. The type can either be forced, 
       determined via a provided pnu_type_map_file or 
       is determined by the pnu_type_map_file shipped with the package.

    Parameters:
        pnu (int): PNU number of value that should be unpacked.
        raw (bytes): Raw bytes value that should be unpacked.
        forced_format (str): Optional format char (see struct) to force the unpacking strategy.
        pnu_type_map_file (str): Optional file name for pnu_type_map. 
                                 By default installed pnu_type_map file is used.
    Returns:
        value: Unpacked value with determined type
    """
    if not forced_format:
        pnu_type_map = read_pnu_type_map_file(pnu_type_map_file)
        pnu_data_type = pnu_type_map[pnu].data_type
        pnu_name = pnu_type_map[pnu].name
        logging.info(f"PNU {pnu} ({pnu_name}) is of type {pnu_data_type}")
        if 'STRING' in pnu_data_type:
            value = struct.unpack(f'{len(raw)}s', raw)[0]

        else:
            value = struct.unpack(
                PNU_TYPE_TO_FORMAT_CHAR[pnu_data_type], raw)[0]
    else:
        logging.info(f"PNU {pnu} forced to type ({forced_format})")

        if forced_format == 's':
            value = struct.unpack(f"{len(raw)}s", raw)[0]
        if forced_format == '?':
            value = struct.unpack('b', raw[0:1])[0]
        if forced_format == 'B':
            value = struct.unpack('B', raw[0:1])[0]
        if forced_format == 'b':
            value = struct.unpack('b', raw[0:1])[0]
        else:
            value = struct.unpack(forced_format, raw)[0]
    return value


def pnu_pack(pnu: int, value, forced_format: str = None, pnu_type_map_file: str = None) -> bytes:
    """Packs a provided value to raw bytes object. The type can either be forced, 
       determined via a provided pnu_type_map_file or 
       is determined by the pnu_type_map_file shipped with the package.

    Parameters:
        pnu (int): PNU number of value that should be unpacked.
        value: Value that should be packed.
        forced_format (str): Optional format char (see struct) to force the packing strategy.
        pnu_type_map_file (str): Optional file name for pnu_type_map. 
                                 By default installed pnu_type_map file is used.
    Returns:
        bytes: Packed value
    """
    if not forced_format:
        pnu_type_map = read_pnu_type_map_file(pnu_type_map_file)
        pnu_data_type = pnu_type_map[pnu].data_type
        pnu_name = pnu_type_map[pnu].name
        logging.info(f"PNU {pnu} ({pnu_name}) is of type {pnu_data_type}")

        if 'INT' in pnu_data_type:
            value = int(value)
        if 'REAL' in pnu_data_type:
            value = float(value)
        if 'STRING' in pnu_data_type:
            return struct.pack('s', bytes(value, encoding='ascii'))
        return struct.pack(PNU_TYPE_TO_FORMAT_CHAR[pnu_data_type], value)

    logging.info(f"PNU {pnu} forced to type ({forced_format})")
    return struct.pack(forced_format, value)
