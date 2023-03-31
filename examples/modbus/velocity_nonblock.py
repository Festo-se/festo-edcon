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
    mot.referencing_task()

    # Enable continuous update so that new position tasks can be started while still in motion
    mot.configure_continuous_update(True)

    mot.velocity_task(500000)
    time.sleep(1)
    mot.velocity_task(-100000)
    time.sleep(1)
    # Be aware that only changing the absolute velocity value update the ongoing task
    mot.velocity_task(100001)

    mot.wait_for_duration(3)
    mot.stop_motion_task()
