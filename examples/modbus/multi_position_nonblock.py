import time
import logging
from edcon.edrive.com_modbus import ComModbus
from edcon.edrive.motion_handler import MotionHandler
from edcon.utils.logging import Logging

# Enable loglevel info
Logging()

# Create a list of all Modbus targets
coms = [ComModbus(ip_address='192.168.0.1'),
        ComModbus(ip_address='192.168.0.119')]
mots = [MotionHandler(com) for com in coms]

for mot in mots:
    mot.acknowledge_faults()
    mot.enable_powerstage()

for mot in mots:
    mot.position_task(10000000, 300000, nonblocking=True)
time.sleep(0.1)

while True:
    target_positions_reached = [mot.target_position_reached() for mot in mots]
    logging.info(f"Target positions reached: {target_positions_reached}")
    if all(target_positions_reached):
        break
    time.sleep(0.1)

for mot in mots:
    mot.shutdown()