import time
from contextlib import ExitStack
import logging
from rich.logging import RichHandler
from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_motion import EDriveMotion

# Enable loglevel info
logging.basicConfig(level=logging.INFO,
                    format='%(message)s',
                    datefmt="[%X]",
                    handlers=[RichHandler()])

# Create a list of all Modbus targets
edrives = [EDriveModbus(ip_address='192.168.0.1'),
           EDriveModbus(ip_address='192.168.0.119')]

with ExitStack() as stack:
    mots = [stack.enter_context(EDriveMotion(edrive)) for edrive in edrives]

    for mot in mots:
        mot.acknowledge_faults()
        mot.enable_powerstage()

    for mot in mots:
        mot.position_task(1000000, 300000, nonblocking=True)
    time.sleep(0.1)

    while True:
        for mot in mots:
            mot.update_inputs()

        target_positions_reached = [
            mot.target_position_reached() for mot in mots]
        logging.info(f"Target positions reached: {target_positions_reached}")
        if all(target_positions_reached):
            break

        time.sleep(0.1)
