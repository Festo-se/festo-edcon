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

    # Enable continuous update so that new position tasks can be started while still in motion
    mot.configure_continuous_update(True)

    mot.velocity_task(50000)
    time.sleep(1)
    mot.velocity_task(-10000)
    time.sleep(1)
    # Be aware that only changing the absolute velocity value update the ongoing task
    mot.velocity_task(10001)

    time.sleep(3)
    mot.stop_motion_task()
