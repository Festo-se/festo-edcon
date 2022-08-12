"""
Contains BehaviorCmmtAs class which contains the specific behavior for CMMT-AS drives.
"""
import logging

from edrive.modbus_flavours.behavior_base import BehaviorBase

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


class BehaviorCmmtAs(BehaviorBase):
    """Class that contains the device specific access sequences for CMMT-AS drives."""

    def read_pnu(self, pnu: int, subindex: int = 0, num_elements: int = 1):
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
                  value: bytes = b'\x00'):
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
            return True

        except AttributeError:
            logging.error("Could not access PNU register")
            return False
