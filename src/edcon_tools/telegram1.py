"""Example on how to use Telegram101 and EDrive classes."""
import sys
import argparse
import logging
import time
import math

from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_ethernetip import EDriveEthernetip
from profidrive.telegram1 import Telegram1


def main():
    """Parses command line arguments and run the example."""
    parser = argparse.ArgumentParser(
        description='Control EDrive device using telegram 1.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--modbus', action='store_true',
                       help='Use Modbus communication')
    group.add_argument('--ethernetip', action='store_true',
                       help='Use EtherNet/IP communication')
    parser.add_argument(
        '-i', '--ip-address', default="192.168.0.51", help='IP address to connect to.')
    parser.add_argument(
        '-s', '--speed-setpoint', default="8192", help='Speed setpoint to use')
    parser.add_argument('--sinusoidal', action="store_true",
                        help='Apply sinusoidal setpoint')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print additional information')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(message)s', level=logging.INFO)

    if args.sinusoidal:
        def get_setpoint():
            return round(int(args.speed_setpoint) * math.sin(time.time()))
    else:
        def get_setpoint():
            return int(args.speed_setpoint)

    # Initialize driver
    if args.modbus:
        edrive = EDriveModbus(args.ip_address)
    elif args.ethernetip:
        edrive = EDriveEthernetip(args.ip_address)

    edrive.assert_selected_telegram(1)

    # Start process data
    edrive.start_io()

    tg1 = Telegram1()

    print("Enable plc control")
    tg1.stw1.control_by_plc = True
    edrive.send_io(tg1.output_bytes())
    time.sleep(0.1)

    print("Acknowledge any present faults")
    tg1.stw1.fault_ack = True
    edrive.send_io(tg1.output_bytes())
    time.sleep(0.1)

    print("Configure STW1")
    tg1.stw1.no_coast_stop = True
    tg1.stw1.no_quick_stop = True
    tg1.stw1.enable_operation = True
    tg1.stw1.enable_ramp_generator = True
    tg1.stw1.unfreeze_ramp_generator = True
    tg1.stw1.fault_ack = False
    edrive.send_io(tg1.output_bytes())
    time.sleep(0.1)

    print("Check fault present bit", end='')
    tg1.input_bytes(edrive.recv_io())
    if tg1.zsw1.fault_present:
        print(" -> is present")
        edrive.stop_io()
        sys.exit(1)
    print(" -> cleared!")

    print("Enable Powerstage")
    tg1.stw1.on = True
    edrive.send_io(tg1.output_bytes())
    time.sleep(0.5)

    print("Enable Setpoint")
    tg1.stw1.setpoint_enable = True
    edrive.send_io(tg1.output_bytes())
    time.sleep(0.1)

    while True:
        try:
            tg1.nsoll_a.value = get_setpoint()
            edrive.send_io(tg1.output_bytes())
            tg1.input_bytes(edrive.recv_io())

            print(f"Setpoint:{tg1.nsoll_a}, Current:{tg1.nist_a}")

            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    edrive.stop_io()


if __name__ == "__main__":
    main()
