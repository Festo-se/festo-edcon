import time
from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_motion import EDriveMotion

edrive = EDriveModbus('192.168.0.51')
with EDriveMotion(edrive) as mot:
    mot.acknowledge_faults()
    mot.enable_powerstage()
    mot.referencing_task()

    # Enable continuous update so that new position tasks can be started while still in motion
    mot.configure_continuous_update(True)

    mot.position_task(-10000, 300000, absolute=True, nonblocking=True)
    time.sleep(1.0)
    mot.position_task(10000, 300000, absolute=True, nonblocking=True)
    time.sleep(1.0)
    mot.position_task(-10000, 300000, absolute=True, nonblocking=True)
    time.sleep(1.0)
    mot.position_task(10000, 300000, absolute=True, nonblocking=True)

    print("Waiting for target position...", end='')
    mot.wait_for_target_position()
    print("done!")
