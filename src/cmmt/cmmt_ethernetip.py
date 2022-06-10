"""
Contains CmmtEthernetip class to configure and communicate with CMMT devices.

This implementation uses the python-ethernetip library by
Sebastian Block (https://codeberg.org/paperwork/python-ethernetip)
"""
import logging

from cmmt.cmmt_base import CmmtBase
from boollist.boollist import bytes_to_boollist, boollist_to_bytes

import ethernetip

O_T_STD_PROCESS_DATA = 100  # Originator to Target
T_O_STD_PROCESS_DATA = 101  # Target to Originator
O_T_EXT_PROCESS_DATA = 110  # Originator to Target
T_O_EXT_PROCESS_DATA = 111  # Target to Originator


class CmmtEthernetip(CmmtBase):
    """Class to configure and communicate with CMMT devices."""

    def __init__(self, ip_address):
        logging.info(f"Starting EtherNet/IP connection on {ip_address}")
        self.eip = ethernetip.EtherNetIP(ip_address)

        self.connection = self.eip.explicit_conn(ip_address)
        self.connection.registerSession()

        # Read product name
        pkt = self.connection.listID()
        if pkt:
            logging.info(f"Product name: {pkt.product_name.decode()}")

        # read process data input size of CMMT from global system object
        # (obj 0x4, inst 100, attr 4)
        status, attribute = self.connection.getAttrSingle(
            0x4, O_T_STD_PROCESS_DATA, 4)
        if status == 0:
            self.insize = int.from_bytes(attribute, 'little')
            logging.info(
                f"Process data input size (data: {attribute}): {self.insize}")

        # read process data output size of CMMT from global system object
        # (obj 0x4, inst 101, attr 4)
        status, attribute = self.connection.getAttrSingle(
            0x4, T_O_STD_PROCESS_DATA, 4)
        if status == 0:
            self.outsize = int.from_bytes(attribute, 'little')
            logging.info(
                f"Process data output size (data: {attribute}): {self.outsize}")

        # read extended process data input size of CMMT from global system object
        # (obj 0x4, inst 110, attr 4)
        status, attribute = self.connection.getAttrSingle(
            0x4, O_T_EXT_PROCESS_DATA, 4)
        if status == 0:
            epd_insize = int.from_bytes(attribute, 'little')
            logging.info(
                f"Extended process data input size (data: {attribute}): {epd_insize}")

        # read extended process data output size of CMMT from global system object
        # (obj 0x4, inst 111, attr 4)
        status, attribute = self.connection.getAttrSingle(
            0x4, T_O_EXT_PROCESS_DATA, 4)
        if status == 0:
            epd_outsize = int.from_bytes(attribute, 'little')
            logging.info(
                f"Extended process data output size (data: {attribute}): {epd_outsize}")

    def read_pnu_raw(self, pnu: int, subindex: int = 0, num_elements: int = 1) -> bytes:
        """Reads a PNU from the CMMT without interpreting the data"""
        # read the PNU (CIP obj 0x401, inst {pnu}, attr {subindex})
        status, data = self.connection.getAttrSingle(0x401, pnu, subindex)
        if status != 0:
            logging.error(f"Error reading PNU {pnu}, status: {status}")
            return None
        return data

    def write_pnu_raw(self, pnu: int, subindex: int = 0, num_elements: int = 1,
                      value: bytes = b'\x00'):
        """Writes raw bytes to a PNU on the CMMT"""
        # write the PNU (CIP obj 0x401, inst {pnu}, attr {subindex})
        status, data = self.connection.setAttrSingle(
            0x401, pnu, subindex, value)

        if status != 0:
            logging.error(
                f"Error writing PNU {pnu}, status: {status}, data: {data}")

    def start_io(self, cycle_time: int = 10):
        """Configures and starts i/o data process"""

        logging.info(
            f"Configure i/o data with {self.insize} input bytes and {self.outsize} output bytes")
        self.eip.registerAssembly(
            ethernetip.EtherNetIP.ENIP_IO_TYPE_INPUT,
            self.insize, T_O_STD_PROCESS_DATA, self.connection)
        self.eip.registerAssembly(
            ethernetip.EtherNetIP.ENIP_IO_TYPE_OUTPUT,
            self.outsize, O_T_STD_PROCESS_DATA, self.connection)

        self.eip.startIO()
        # Start process with 10 ms input and 10 ms output frequency
        # torpi = device to python
        # otrpi = python to device
        status = self.connection.sendFwdOpenReq(
            T_O_STD_PROCESS_DATA, O_T_STD_PROCESS_DATA, 1, torpi=cycle_time, otrpi=cycle_time)
        if status != 0:
            logging.error(f"Could not open connection: {status}")
        self.connection.produce()

    def stop_io(self):
        """Stops i/o data process"""
        self.connection.stopProduce()
        self.connection.sendFwdCloseReq(
            T_O_STD_PROCESS_DATA, O_T_STD_PROCESS_DATA, 1)
        self.eip.stopIO()

    def send_io(self, data: bytes):
        """Sends data to the output"""
        self.connection.outAssem = bytes_to_boollist(data, self.outsize)

    def recv_io(self) -> bytes:
        """Receives data from the input"""
        return boollist_to_bytes(self.connection.inAssem)
