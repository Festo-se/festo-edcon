from edrive.edrive_ethernetip import EDriveEthernetip
from edrive.edrive_positioning import EDrivePositioning

edrive = EDriveEthernetip('192.168.0.51')
with EDrivePositioning(edrive) as pos:
    pos.request_plc_control()
    pos.acknowledge_faults()
    pos.enable_powerstage()
    pos.homing_task()
    pos.position_task(10000, 600000)
    pos.position_task(-5000, 50000)
    pos.position_task(30000, 600000, absolute=True)
