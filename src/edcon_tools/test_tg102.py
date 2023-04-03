"""CLI tool that performs a sequence on Telegram102 and EDrive classes."""
import sys
import time
import math

from edcon_tools.generic_bus_argparser import GenericBusArgParser
from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_ethernetip import EDriveEthernetip
from profidrive.telegram102 import Telegram102


def main():
    """Parses command line arguments and run the example."""
    gparser = GenericBusArgParser('Control EDrive device using telegram 102.')
    gparser.add_argument('-s', '--speed-setpoint',
                         default="1000000000", help='Speed setpoint to use')
    gparser.add_argument('-m', '--moment-reduction',
                         default="0.0", help='Moment reduction to use in percent')
    gparser.add_argument('--sinusoidal', action="store_true",
                         help='Apply sinusoidal setpoint')

    args = gparser.create()

    if args.sinusoidal:
        def get_setpoint():
            return round(int(args.speed_setpoint) * math.sin(time.time()))
    else:
        def get_setpoint():
            return int(args.speed_setpoint)

    # Initialize driver
    if args.com_type == 'modbus':
        edrive = EDriveModbus(args.ip_address)
    elif args.com_type == 'ethernetip':
        edrive = EDriveEthernetip(args.ip_address)

    edrive.assert_selected_telegram(102)

    # Start process data
    edrive.start_io()

    tg102 = Telegram102()

    print("Enable plc control")
    tg102.stw1.control_by_plc = True
    edrive.send_io(tg102.output_bytes())
    time.sleep(0.1)

    print("Acknowledge any present faults")
    tg102.stw1.fault_ack = True
    edrive.send_io(tg102.output_bytes())
    time.sleep(0.1)

    print("Configure STW1 and MOMRED")
    tg102.stw1.no_coast_stop = True
    tg102.stw1.no_quick_stop = True
    tg102.stw1.enable_operation = True
    tg102.stw1.enable_ramp_generator = True
    tg102.stw1.unfreeze_ramp_generator = True
    tg102.stw1.fault_ack = False
    tg102.momred.value = round(16384.0 * float(args.moment_reduction) / 100.0)
    edrive.send_io(tg102.output_bytes())
    time.sleep(0.1)

    print("Check fault present bit", end='')
    tg102.input_bytes(edrive.recv_io())
    if tg102.zsw1.fault_present:
        print(" -> is present")
        edrive.stop_io()
        sys.exit(1)
    print(" -> cleared!")

    print("Enable Powerstage")
    tg102.stw1.on = True
    edrive.send_io(tg102.output_bytes())
    time.sleep(0.5)

    print("Enable Setpoint")
    tg102.stw1.setpoint_enable = True
    edrive.send_io(tg102.output_bytes())
    time.sleep(0.1)

    while True:
        try:
            tg102.nsoll_b.value = get_setpoint()
            edrive.send_io(tg102.output_bytes())
            tg102.input_bytes(edrive.recv_io())

            print(f"Setpoint:{tg102.nsoll_b}, Current:{tg102.nist_b}")

            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    edrive.stop_io()


if __name__ == "__main__":
    main()
