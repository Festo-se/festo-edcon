"""Contains EDrivePnuTypeMap class which contains mapping of PNU types."""
from collections import namedtuple
from importlib.resources import files
import csv
from functools import lru_cache
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
    if not pnu_type_map_file:
        pnu_type_map_file = files('edrive.data').joinpath('pnu_type_map.csv')

    with open(pnu_type_map_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        # Define a namedtuple where the header row determines the field names
        pnu_item = namedtuple('pnu_item', next(reader, None))
        # Create a dict where the first column determines the key
        pnu_type_dict = {int(row[0]): pnu_item(*row) for row in reader}
    return pnu_type_dict


def pnu_unpack(pnu: int, raw: bytes, forced_format=None, pnu_type_map_file: str = None):
    if not forced_format:
        pnu_type_map = read_pnu_type_map_file(pnu_type_map_file)
        pnu_data_type = pnu_type_map[pnu].data_type
        pnu_name = pnu_type_map[pnu].name
        logging.info(f"PNU {pnu} ({pnu_name}) is of type {pnu_data_type}")
        if 'STRING' in pnu_data_type:
            return struct.unpack(f'{len(raw)}s', raw)[0]

        return struct.unpack(PNU_TYPE_TO_FORMAT_CHAR[pnu_data_type], raw)[0]

    logging.info(f"PNU {pnu} forced to type ({forced_format})")
    if forced_format == 's':
        return struct.unpack(f"{len(raw)}s", raw)[0]
    if forced_format == '?':
        return struct.unpack('b', raw[0:1])[0]
    if forced_format == 'B':
        return struct.unpack('B', raw[0:1])[0]
    if forced_format == 'b':
        return struct.unpack('b', raw[0:1])[0]
    return struct.unpack(forced_format, raw)[0]


def pnu_pack(pnu: int, value, forced_format=None, pnu_type_map_file: str = None) -> bytes:

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
