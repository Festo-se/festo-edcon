import time
from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_positioning import EDrivePositioning

edrive = EDriveModbus('192.168.0.51')
with EDrivePositioning(edrive) as pos:
    pos.request_plc_control()
    pos.acknowledge_faults()
    pos.enable_powerstage()
    pos.referencing_task()

    # Enable continuous update so that new position tasks can be started while still in motion
    pos.configure_continuous_update(True)

    pos.velocity_task(500000)
    time.sleep(1)
    pos.velocity_task(-100000)
    time.sleep(1)
    # Be aware that only changing the absolute velocity value update the ongoing task
    pos.velocity_task(100001)

    print("Wait for some time ...", end='')
    time.sleep(3)
    print("done!")
