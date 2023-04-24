import time
from edcon.edrive.com_modbus import ComModbus
from edcon.edrive.motion_handler import MotionHandler
from edcon.utils.logging import Logging

# Enable loglevel info
Logging()

edrive = ComModbus('192.168.0.51')
with MotionHandler(edrive) as mot:
    mot.acknowledge_faults()
    mot.enable_powerstage()
    mot.referencing_task()

    mot.velocity_task(50000, 3.0)
    time.sleep(1.0)
    mot.velocity_task(-30000, 3.0)
