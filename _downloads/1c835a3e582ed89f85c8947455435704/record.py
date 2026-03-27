import time
from edcon.edrive.com_modbus import ComModbus
from edcon.edrive.motion_handler import MotionHandler
from edcon.utils.logging import Logging

# Enable loglevel info
Logging()

edrive = ComModbus("192.168.0.1")
with MotionHandler(edrive) as mot:
    mot.acknowledge_faults()
    mot.enable_powerstage()
    mot.referencing_task()

    # toggle five times between records 1 and 2
    for i in range(5):
        mot.record_task(1)
        time.sleep(1)
        mot.record_task(2)
        time.sleep(1)

    mot.stop_motion_task()
    mot.disable_powerstage()
