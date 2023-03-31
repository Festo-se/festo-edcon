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
    mot.referencing_task(use_homing_method=False)

    mot.velocity_task(50000, 3.0)
    time.sleep(1.0)
    mot.velocity_task(-30000, 3.0)
