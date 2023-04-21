from edcon.edrive.com_modbus import ComModbus
from edcon.edrive.motion import MotionExecutor
from edcon.utils.logging import Logging

# Enable loglevel info
Logging()

edrive = ComModbus('192.168.0.51')
with MotionExecutor(edrive) as mot:
    mot.acknowledge_faults()
    mot.enable_powerstage()
    mot.referencing_task()

    mot.position_task(100000, 600000)
    mot.position_task(-50000, 50000)
    mot.position_task(300000, 600000, absolute=True)
