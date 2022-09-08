from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_motion import EDriveMotion

edrive = EDriveModbus('192.168.0.51')
with EDriveMotion(edrive) as mot:
    mot.acknowledge_faults()
    mot.enable_powerstage()
    mot.referencing_task()

    mot.position_task(10000, 600000)
    mot.position_task(-5000, 50000)
    mot.position_task(30000, 600000, absolute=True)
