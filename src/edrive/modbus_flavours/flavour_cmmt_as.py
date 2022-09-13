"""
Contains FlavourCmmtAs class which contains the specific flavour for CMMT-AS drives.
"""
import logging

from pymodbus.mei_message import ReadDeviceInformationRequest
from edrive.modbus_flavours.flavour_base import FlavourBase

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


class FlavourCmmtAs(FlavourBase):
    """Class that contains the device specific access sequences for CMMT-AS drives."""

    def device_info(self):
        if self.dev_info_dict:
            return self.dev_info_dict

        self.dev_info_dict = {"pd_in_addr": 100,
                              "pd_out_addr": 0,
                              "timeout_addr": 400,
                              "pd_size": 56
                              }

        # Read device information
        rreq = ReadDeviceInformationRequest(0x1, 0)
        rres = self.modbus_client.execute(rreq)
        self.dev_info_dict["vendor_name"] = rres.information[0].decode('ascii')
        self.dev_info_dict["product_code"] = rres.information[1].decode(
            'ascii')
        self.dev_info_dict["revision"] = rres.information[2].decode('ascii')
        logging.info(f"Vendor Name: {self.dev_info_dict['vendor_name']}")
        logging.info(f"Product Code: {self.dev_info_dict['product_code']}")
        logging.info(f"Firmware Version: {self.dev_info_dict['revision']}")
        rreq = ReadDeviceInformationRequest(0x2, 0)
        rres = self.modbus_client.execute(rreq)
        self.dev_info_dict["vendor_url"] = rres.information[3].decode('ascii')
        self.dev_info_dict["product_name"] = rres.information[4].decode(
            'ascii')
        self.dev_info_dict["model_name"] = rres.information[5].decode('ascii')
        logging.info(f"Vendor URL: {self.dev_info_dict['vendor_url']}")
        logging.info(f"Product Name: {self.dev_info_dict['product_name']}")
        logging.info(f"Model Name: {self.dev_info_dict['model_name']}")

        return self.dev_info_dict

    def read_pnu(self, pnu: int, subindex: int = 0, num_elements: int = 1) -> bytes:
        try:
            self.modbus_client.write_register(REG_PNU_MAILBOX_PNU, pnu)
            self.modbus_client.write_register(
                REG_PNU_MAILBOX_SUBINDEX, subindex)
            self.modbus_client.write_register(
                REG_PNU_MAILBOX_NUM_ELEMENTS, num_elements)

            # Execute
            self.modbus_client.write_register(
                REG_PNU_MAILBOX_EXEC, PNU_MAILBOX_EXEC_READ)
            status = self.modbus_client.read_holding_registers(
                REG_PNU_MAILBOX_EXEC, 1).registers[0]

            if status != PNU_MAILBOX_EXEC_DONE:
                logging.error(f"Error reading PNU {pnu}, status: {status}")
                return None

            # Read available data length
            length = self.modbus_client.read_holding_registers(
                REG_PNU_MAILBOX_DATA_LEN, 1).registers[0]

            # Divide length by 2 because each register is 2 bytes
            indata = self.modbus_client.read_holding_registers(
                510, int((length+1)/2))

            # Convert to integer
            data = b''.join(reg.to_bytes(2, 'little')
                            for reg in indata.registers)
            return data

        except AttributeError:
            logging.error("Could not access PNU register")
            return None

    def write_pnu(self, pnu: int, subindex: int = 0, num_elements: int = 1,
                  value: bytes = b'\x00') -> bool:
        try:
            self.modbus_client.write_register(REG_PNU_MAILBOX_PNU, pnu)
            self.modbus_client.write_register(
                REG_PNU_MAILBOX_SUBINDEX, subindex)
            self.modbus_client.write_register(
                REG_PNU_MAILBOX_NUM_ELEMENTS, num_elements)
            self.modbus_client.write_register(
                REG_PNU_MAILBOX_DATA_LEN, len(value))

            # Convert to list of words
            word_list = [int.from_bytes(value[i:i+2], 'little')
                         for i in range(0, len(value), 2)]
            # Write data
            self.modbus_client.write_registers(510, word_list)

            # Execute
            self.modbus_client.write_register(
                REG_PNU_MAILBOX_EXEC, PNU_MAILBOX_EXEC_WRITE)
            status = self.modbus_client.read_holding_registers(
                REG_PNU_MAILBOX_EXEC, 1).registers[0]
            if status != PNU_MAILBOX_EXEC_DONE:
                logging.error(f"Error writing PNU {pnu}, status: {status}")
                return False
            return True

        except AttributeError:
            logging.error("Could not access PNU register")
            return False
