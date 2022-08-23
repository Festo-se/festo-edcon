"""
Contains EDriveModbus class to configure and communicate with EDrive devices.

This implementation uses the pymodbus library
https://pymodbus.readthedocs.io/en/latest/index.html
"""
import threading
import logging
import time

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from edrive.edrive_base import EDriveBase
from edrive.modbus_flavours.modbus_flavours import modbus_flavours


class IOThread(threading.Thread):
    def __init__(self, edmb=None):
        self.edmb = edmb
        threading.Thread.__init__(self)

    def run(self):
        while self.edmb.io_thread_active:
            # Inputs
            indata = self.edmb.client.read_holding_registers(
                self.edmb.device_info["pd_in_addr"], int(self.edmb.device_info["pd_size"]/2))
            # Convert to bytes
            self.edmb.in_data = b''.join(reg.to_bytes(2, 'little')
                                         for reg in indata.registers)

            # Outputs
            word_list = [int.from_bytes(self.edmb.out_data[i:i+2], 'little')
                         for i in range(0, len(self.edmb.out_data), 2)]
            self.edmb.client.write_registers(self.edmb.device_info[
                "pd_out_addr"], word_list)
            time.sleep(self.edmb.cycle_time * 0.001)


class EDriveModbus(EDriveBase):
    """Class to configure and communicate with EDrive devices."""

    def __init__(self, ip_address, cycle_time: int = 10, timeout_ms=1000, flavour="CMMT-AS"):
        """Constructor of the EDriveModbus class.

        Parameters:
            ip_address (str): Required IP address as string e.g. ('192.168.0.1')
            timeout_ms (int): Modbus timeout (in ms) that should be configured on the slave
            flavour (str/dict/FlavourBase): May either be one of the built-in flavours as ``str``,
                a custom flavour as ``dict`` or ``FlavourBase`` deduced object.
                See :mod:`ModbusFlavours <edrive.modbus_flavours.modbus_flavours>`
                for built-in flavours
        """
        self.io_thread = None
        self.io_thread_active = False
        self.cycle_time = cycle_time

        logging.info(f"Starting Modbus connection on {ip_address}")
        self.client = ModbusClient(ip_address)
        self.client.connect()

        if isinstance(flavour, str):
            flavour = modbus_flavours()[flavour]
            self.flavour = flavour(self.client)
            self.device_info = self.flavour.device_info()

        elif isinstance(flavour, dict):
            self.device_info = flavour

        else:
            self.flavour = flavour(self.client)

        self.in_data = b'\x00' * self.device_info["pd_size"]
        self.out_data = b'\x00' * self.device_info["pd_size"]

        self.set_timeout(timeout_ms)

    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()

    def set_timeout(self, timeout_ms) -> bool:
        """Sets the modbus timeout to the provided value"""
        logging.info(f"Setting modbus timeout to {timeout_ms} ms")
        self.client.write_registers(
            self.device_info["timeout_addr"], [timeout_ms, 0])
        # Check if it actually succeeded
        indata = self.client.read_holding_registers(
            self.device_info["timeout_addr"], 1)
        if indata.registers[0] != timeout_ms:
            logging.error("Setting of modbus timeout was not successful")
            return False
        return True

    def read_pnu_raw(self, pnu: int, subindex: int = 0, num_elements: int = 1) -> bool:
        if hasattr(self, 'flavour'):
            return self.flavour.read_pnu(pnu, subindex, num_elements)
        return None

    def write_pnu_raw(self, pnu: int, subindex: int = 0, num_elements: int = 1,
                      value: bytes = b'\x00') -> bool:
        if hasattr(self, 'flavour'):
            return self.flavour.write_pnu(pnu, subindex, num_elements, value)
        return None

    def start_io(self):
        """Starts i/o data process"""
        self.io_thread = IOThread(self)
        self.io_thread_active = True
        self.io_thread.start()

    def stop_io(self):
        """Stops i/o data process"""
        self.send_io(b'\x00' * self.device_info["pd_size"])
        self.io_thread_active = False

    def send_io(self, data: bytes):
        """Sends data to the output"""
        # Convert to list of words
        self.out_data = data

    def recv_io(self) -> bytes:
        """Receives data from the input"""
        return self.in_data
