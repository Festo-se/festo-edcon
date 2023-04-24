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

    mot.position_task(-100000, 300000, absolute=True, nonblocking=True)
    time.sleep(1.0)
    mot.position_task(100000, 300000, absolute=True, nonblocking=True)
    time.sleep(1.0)
    mot.position_task(-100000, 300000, absolute=True, nonblocking=True)
    time.sleep(1.0)
    mot.position_task(1000000, 300000, absolute=True, nonblocking=True)

    mot.wait_for_target_position()
