import time
from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_motion import EDriveMotion

edrive = EDriveModbus('192.168.0.51')
with EDriveMotion(edrive) as pos:
    pos.request_plc_control()
    pos.acknowledge_faults()
    pos.enable_powerstage()

    pos.jog_task(True, False, duration=0.0)
    time.sleep(4)
    pos.jog_task(False, True, duration=0.0)
    time.sleep(4)
