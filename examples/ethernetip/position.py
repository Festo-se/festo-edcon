from edcon.edrive.com_ethernetip import ComEthernetip
from edcon.edrive.motion_handler import MotionHandler
from edcon.utils.logging import Logging

# Enable loglevel info
Logging()

com = ComEthernetip('192.168.0.1')
with MotionHandler(com) as pos:
    pos.acknowledge_faults()
    pos.enable_powerstage()
    pos.referencing_task()

    pos.position_task(10000, 600000)
    pos.position_task(-5000, 50000)
    pos.position_task(30000, 600000, absolute=True)
