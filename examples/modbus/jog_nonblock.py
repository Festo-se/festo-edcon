import time
from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_motion import EDriveMotion
from edrive.edrive_logging import EDriveLogging

# Enable loglevel info
EDriveLogging()

edrive = EDriveModbus('192.168.0.51')
with EDriveMotion(edrive) as mot:
    mot.acknowledge_faults()
    mot.enable_powerstage()

    mot.jog_task(True, False, duration=0.0)
    time.sleep(4)
    mot.jog_task(False, True, duration=0.0)
    time.sleep(4)

    mot.stop_motion_task()
