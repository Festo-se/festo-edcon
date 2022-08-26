import time
from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_motion import EDriveMotion

edrive = EDriveModbus('192.168.0.51')
with EDriveMotion(edrive) as pos:
    pos.request_plc_control()
    pos.acknowledge_faults()
    pos.enable_powerstage()
    pos.referencing_task()

    # Enable continuous update so that new position tasks can be started while still in motion
    pos.configure_continuous_update(True)

    pos.position_task(-10000, 300000, absolute=True, nonblocking=True)
    time.sleep(1.0)
    pos.position_task(10000, 300000, absolute=True, nonblocking=True)
    time.sleep(1.0)
    pos.position_task(-10000, 300000, absolute=True, nonblocking=True)
    time.sleep(1.0)
    pos.position_task(10000, 300000, absolute=True, nonblocking=True)

    print("Waiting for target position...", end='')
    while not pos.tg111.zsw1.target_position_reached:
        pos.update_inputs()
    print("done!")
