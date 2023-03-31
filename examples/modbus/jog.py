from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_motion import EDriveMotion
from edrive.edrive_logging import EDriveLogging

# Enable loglevel info
EDriveLogging()

edrive = EDriveModbus('192.168.0.51')
with EDriveMotion(edrive) as mot:
    mot.acknowledge_faults()
    mot.enable_powerstage()

    mot.jog_task(True, False, duration=3.0)
