from edcon.edrive.com_modbus import ComModbus
from edcon.edrive.motion_handler import MotionHandler
from edcon.utils.logging import Logging
import time

# Enable loglevel info
Logging()

com = ComModbus("192.168.0.1")
base_velocity = com.read_pnu(12345)  # Read base velocity (P1.11280701)
# The following example assumes a rotative axis with factor group pos 10^-6 and vel 10^-3
com.write_pnu(12168, value=0.2)  # Set clamping torque to 0.2 Nm (P1.526801)
# Optionally configure the clamping torque windows
# com.write_pnu(11614, value=0.1)  # Monitoring window torque (P1.4668)
# Optionally also configure the monitoring windows for fix stop detection
# com.write_pnu(11635, value=0.1)  # Fixed stop detection damping time in seconds (P1.4693)
# com.write_pnu(11636, value=0.01)  # Limit value following error in revolutions (P1.4694)
with MotionHandler(com) as mot:
    mot.base_velocity = base_velocity
    mot.configure_traversing_to_fixed_stop(True)  # Enable traversing to fixed stop
    mot.acknowledge_faults()
    mot.enable_powerstage()
    if not mot.referenced():
        mot.referencing_task()

    # Move to position 100.0 with speed 6 rpm
    mot.position_task(100000000, 12000, nonblocking=True)
    while True:
        pos_str = f"{mot.current_position()*10e-6:.3f}"
        vel_str = f"{mot.current_velocity():.3f}"
        ct_str = f"{mot.clamping_torque_reached()}"
        fs_str = f"{mot.fix_stop_reached()}"
        print(
            f"Pos: {pos_str:>10} | Vel: {vel_str:>10} | Clamping torque: {ct_str:>5} | Fix stop: {fs_str:>5}"
        )
        if mot.fix_stop_reached():
            print("Fixed stop reached.")
            break
        if mot.target_position_reached():
            print("Target position reached without fixed stop.")
            break
        if mot.fault_present():
            print(f"{mot.fault_string()}")
            break
        time.sleep(0.1)
    mot.stop_motion_task()
