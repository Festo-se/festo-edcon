"""
Contains EDriveModbus class to configure and communicate with EDrive devices.

This implementation uses the pymodbus library
https://pymodbus.readthedocs.io/en/latest/index.html
"""
import logging

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.mei_message import ReadDeviceInformationRequest
from edrive.edrive_base import EDriveBase

REG_SLAVE_INPUT_DATA = 0
REG_SLAVE_OUTPUT_DATA = 100
REG_MODBUS_TIMEOUT = 400
REG_PNU_MAILBOX_PNU = 500
REG_PNU_MAILBOX_SUBINDEX = 501
REG_PNU_MAILBOX_NUM_ELEMENTS = 502
REG_PNU_MAILBOX_EXEC = 503
REG_PNU_MAILBOX_DATA_LEN = 504
REG_PNU_MAILBOX_DATA = 510

PNU_MAILBOX_EXEC_READ = 0x01
PNU_MAILBOX_EXEC_WRITE = 0x02
PNU_MAILBOX_EXEC_ERROR = 0x03
PNU_MAILBOX_EXEC_DONE = 0x10


class EDriveModbus(EDriveBase):
    """Class to configure and communicate with EDrive devices."""

    def __init__(self, ip_address, timeout_ms=1000):
        logging.info(f"Starting Modbus connection on {ip_address}")
        self.client = ModbusClient(ip_address)
        self.client.connect()

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
        self.client.close()

    def set_timeout(self, timeout_ms) -> bool:
        """Sets the modbus timeout to the provided value"""
        logging.info(f"Setting modbus timeout to {timeout_ms} ms")
        self.client.write_registers(REG_MODBUS_TIMEOUT, [timeout_ms])
        # Check if it actually succeeded
        indata = self.client.read_holding_registers(REG_MODBUS_TIMEOUT, 1)
        if indata.registers[0] != timeout_ms:
            logging.error("Setting of modbus timeout was not successful")
            return False
        return True

    def read_pnu_raw(self, pnu: int, subindex: int = 0, num_elements: int = 1) -> bytes:
        """Reads a PNU from the EDrive without interpreting the data"""
        try:
            self.client.write_register(REG_PNU_MAILBOX_PNU, pnu)
            self.client.write_register(REG_PNU_MAILBOX_SUBINDEX, subindex)
            self.client.write_register(
                REG_PNU_MAILBOX_NUM_ELEMENTS, num_elements)

            # Execute
            self.client.write_register(
                REG_PNU_MAILBOX_EXEC, PNU_MAILBOX_EXEC_READ)
            status = self.client.read_holding_registers(
                REG_PNU_MAILBOX_EXEC, 1).registers[0]

            if status != PNU_MAILBOX_EXEC_DONE:
                logging.error(f"Error reading PNU {pnu}, status: {status}")
                return None

            # Read available data length
            length = self.client.read_holding_registers(
                REG_PNU_MAILBOX_DATA_LEN, 1).registers[0]

            # Divide length by 2 because each register is 2 bytes
            indata = self.client.read_holding_registers(510, int((length+1)/2))

            # Convert to integer
            data = b''.join(reg.to_bytes(2, 'little')
                            for reg in indata.registers)
            return data

        except AttributeError:
            logging.error("Could not access PNU register")
            return None

    def write_pnu_raw(self, pnu: int, subindex: int = 0, num_elements: int = 1,
                      value: bytes = b'\x00') -> bool:
        """Writes raw bytes to a PNU on the EDrive"""
        try:
            self.client.write_register(REG_PNU_MAILBOX_PNU, pnu)
            self.client.write_register(REG_PNU_MAILBOX_SUBINDEX, subindex)
            self.client.write_register(
                REG_PNU_MAILBOX_NUM_ELEMENTS, num_elements)
            self.client.write_register(REG_PNU_MAILBOX_DATA_LEN, len(value))

            # Convert to list of words
            word_list = [int.from_bytes(value[i:i+2], 'little')
                         for i in range(0, len(value), 2)]
            # Write data
            self.client.write_registers(510, word_list)

            # Execute
            self.client.write_register(
                REG_PNU_MAILBOX_EXEC, PNU_MAILBOX_EXEC_WRITE)
            status = self.client.read_holding_registers(
                REG_PNU_MAILBOX_EXEC, 1).registers[0]
            if status != PNU_MAILBOX_EXEC_DONE:
                logging.error(f"Error writing PNU {pnu}, status: {status}")
            return True

        except AttributeError:
            logging.error("Could not access PNU register")
            return False

    def stop_io(self):
        """Stops i/o data process"""
        self.send_io(b'\x00' * self.insize)

    def send_io(self, data: bytes):
        """Sends data to the output"""
        # Convert to list of words
        word_list = [int.from_bytes(data[i:i+2], 'little')
                     for i in range(0, len(data), 2)]
        self.client.write_registers(REG_SLAVE_INPUT_DATA, word_list)

    def recv_io(self) -> bytes:
        """Receives data from the input"""
        indata = self.client.read_holding_registers(
            REG_SLAVE_OUTPUT_DATA, int(self.outsize/2))
        # Convert to bytes
        data = b''.join(reg.to_bytes(2, 'little') for reg in indata.registers)
        return data
