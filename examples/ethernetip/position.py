from edrive.edrive_ethernetip import EDriveEthernetip
from edrive.edrive_motion import EDriveMotion

edrive = EDriveEthernetip('192.168.0.51')
with EDriveMotion(edrive) as pos:
    pos.acknowledge_faults()
    pos.enable_powerstage()
    pos.referencing_task()

    pos.position_task(10000, 600000)
    pos.position_task(-5000, 50000)
    pos.position_task(30000, 600000, absolute=True)
