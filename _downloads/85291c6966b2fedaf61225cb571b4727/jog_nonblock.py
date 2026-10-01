import time
from edcon.edrive.com_modbus import ComModbus
from edcon.edrive.motion_handler import MotionHandler
from edcon.utils.logging import Logging

# Enable loglevel info
Logging()

com = ComModbus('192.168.0.1')
with MotionHandler(com) as mot:
    mot.acknowledge_faults()
    mot.enable_powerstage()

    mot.jog_task(True, False, duration=0.0)
    time.sleep(4)
    mot.jog_task(False, True, duration=0.0)
    time.sleep(4)

    mot.stop_motion_task()
