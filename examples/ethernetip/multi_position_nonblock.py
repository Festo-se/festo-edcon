import time
from edcon.utils.logging import Logging
from edcon.edrive.com_ethernetip import ComEthernetip
from edcon.edrive.motion_handler import MotionHandler
from edcon.utils.logging import Logging

# Enable loglevel info
Logging()

# Create a list of all Modbus targets
coms = [ComEthernetip(ip_address='192.168.0.2'),
        ComEthernetip(ip_address='192.168.0.51')]
mots = [MotionHandler(com) for com in coms]

for mot in mots:
    mot.acknowledge_faults()
    mot.enable_powerstage()
    if not mot.referenced():
        mot.referencing_task()

for mot in mots:
    mot.position_task(10000000, 300000, nonblocking=True)
time.sleep(0.1)

while True:
    target_positions_reached = [mot.target_position_reached() for mot in mots]
    Logging.logger.info(f"Target positions reached: {target_positions_reached}")
    if all(target_positions_reached):
        break
    time.sleep(0.1)

for mot in mots:
    mot.shutdown()