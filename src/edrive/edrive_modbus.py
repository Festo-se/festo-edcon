"""
Contains EDriveModbus class to configure and communicate with EDrive devices.

This implementation uses the pymodbus library
https://pymodbus.readthedocs.io/en/latest/index.html
"""
import logging

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.mei_message import ReadDeviceInformationRequest
from edrive.edrive_base import EDriveBase
from edrive.modbus_flavours.modbus_flavours import flavours


class EDriveModbus(EDriveBase):
    """Class to configure and communicate with EDrive devices."""

    def __init__(self, ip_address, timeout_ms=1000, flavour="CMMT-AS"):
        """Constructor of the EDriveModbus class.

            Parameters:
            ------------
                ip_address: str
                            Required IP address as string e.g. ('192.168.0.1')
                timeout_ms: int
                            Modbus timeout (in ms) that should be configured on the slave
                flavour: str/dict
                         Optional device flavour. May either be one of the built-in flavours as str
                         or a custom flavour as dict.
                         Currently built-in flavours: ['CMMT-AS','CPX-AP']
        """
        logging.info(f"Starting Modbus connection on {ip_address}")
        self.client = ModbusClient(ip_address)
        self.client.connect()

        if isinstance(flavour, str):
            flavour = flavours[flavour]

        self.reg_addr = flavour["registers"]
        try:
            self.behavior = flavour["behavior"](self.client)
        except KeyError:
            logging.warning(
                "No device behavior defined. PNU access is disqualified.")

        self.set_timeout(timeout_ms)

        # Read device information
        rreq = ReadDeviceInformationRequest(0x03, 0)
        rres = self.client.execute(rreq)

        if hasattr(rres, 'information'):
            logging.info(
                f"Vendor Name: {rres.information[0][0].decode('ascii')}")
            logging.info(
                f"Product Code: {rres.information[1][0].decode('ascii')}")
            logging.info(
                f"Firmware Version: {rres.information[2][0].decode('ascii')}")

            logging.info(
                f"Vendor URL: {rres.information[3][0].decode('ascii')}")
            logging.info(
                f"Product Name: {rres.information[4][0].decode('ascii')}")

        # How can we find out this information automatically?
        self.insize = 24  # Originator to Target
        self.outsize = 24   # Target to Originator
        self.epd_insize = 32  # Originator to Target
        self.epd_outsize = 32  # Target to Originator

    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()

    def set_timeout(self, timeout_ms) -> bool:
        """Sets the modbus timeout to the provided value"""
        logging.info(f"Setting modbus timeout to {timeout_ms} ms")
        self.client.write_registers(self.reg_addr["timeout"], [timeout_ms, 0])
        # Check if it actually succeeded
        indata = self.client.read_holding_registers(
            self.reg_addr["timeout"], 1)
        if indata.registers[0] != timeout_ms:
            logging.error("Setting of modbus timeout was not successful")
            return False
        return True

    def read_pnu_raw(self, pnu: int, subindex: int = 0, num_elements: int = 1) -> bool:
        if hasattr(self, "behavior"):
            return self.behavior.read_pnu(pnu, subindex, num_elements)
        return None

    def write_pnu_raw(self, pnu: int, subindex: int = 0, num_elements: int = 1,
                      value: bytes = b'\x00') -> bool:
        if hasattr(self, "behavior"):
            return self.behavior.write_pnu(pnu, subindex, num_elements, value)
        return None

    def stop_io(self):
        """Stops i/o data process"""
        self.send_io(b'\x00' * self.insize)

    def send_io(self, data: bytes):
        """Sends data to the output"""
        # Convert to list of words
        word_list = [int.from_bytes(data[i:i+2], 'little')
                     for i in range(0, len(data), 2)]
        self.client.write_registers(self.reg_addr["pd_out"], word_list)

    def recv_io(self) -> bytes:
        """Receives data from the input"""
        indata = self.client.read_holding_registers(
            self.reg_addr["pd_in"], int(self.outsize/2))
        # Convert to bytes
        data = b''.join(reg.to_bytes(2, 'little') for reg in indata.registers)
        return data
