"""Example on how to use Telegram111 and Cmmt classes."""
import time
import logging
import argparse
import sys

from cmmt.cmmt_ethernetip import CmmtEthernetip
from cmmt.cmmt_modbus import CmmtModbus
from profidrive.telegram111 import Telegram111


def main():
    """Parses command line arguments and run the example."""
    parser = argparse.ArgumentParser(
        description='Control CMMT device using telegram 111.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--modbus', action='store_true',
                       help='Use Modbus communication')
    group.add_argument('--ethernetip', action='store_true',
                       help='Use EtherNet/IP communication')
    parser.add_argument(
        '-i', '--ip-address', default="192.168.0.51", help='IP address to connect to.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print additional information')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(message)s', level=logging.INFO)

    # Initialize driver
    if args.modbus:
        cmmt_driver = CmmtModbus(args.ip_address)
    elif args.ethernetip:
        cmmt_driver = CmmtEthernetip(args.ip_address)

    cmmt_driver.assert_selected_telegram(111)
    # Start process data
    cmmt_driver.start_io()

    tg111 = Telegram111()

    print("Enable plc control")
    tg111.stw1.control_by_plc = True
    cmmt_driver.send_io(tg111.output_bytes())
    time.sleep(0.1)

    print("Acknowledge any present faults")
    tg111.stw1.fault_ack = True
    cmmt_driver.send_io(tg111.output_bytes())
    time.sleep(0.1)

    print("Configure STW1 and OVERRIDE")
    tg111.stw1.no_coast_stop = True
    tg111.stw1.no_quick_stop = True
    tg111.stw1.enable_operation = True
    tg111.stw1.do_not_reject_traversing_task = True
    tg111.stw1.no_intermediate_stop = True
    tg111.stw1.fault_ack = False
    tg111.override.value = 16384
    cmmt_driver.send_io(tg111.output_bytes())
    time.sleep(0.1)

    print("Check fault present bit", end='')
    tg111.input_bytes(cmmt_driver.recv_io())
    if tg111.zsw1.fault_present:
        print(f" -> is present ({int(tg111.fault_code)})")
        cmmt_driver.stop_io()
        sys.exit(1)
    print(" -> cleared!")

    print("Enable Powerstage")
    tg111.stw1.on = True
    cmmt_driver.send_io(tg111.output_bytes())
    time.sleep(0.5)

    print("Start homing procedure")
    tg111.stw1.start_homing_procedure = True
    cmmt_driver.send_io(tg111.output_bytes())
    time.sleep(0.1)

    while tg111.zsw1.home_position_set:
        try:
            tg111.input_bytes(cmmt_driver.recv_io())
            time.sleep(0.1)

        except KeyboardInterrupt:
            print("Killed by user!")
            cmmt_driver.stop_io()
            sys.exit(1)

    while not tg111.zsw1.home_position_set:
        try:
            tg111.input_bytes(cmmt_driver.recv_io())
            time.sleep(0.1)

        except KeyboardInterrupt:
            print("Killed by user!")
            cmmt_driver.stop_io()
            sys.exit(1)

    print("Finished homing")

    tg111.stw1.start_homing_procedure = False
    cmmt_driver.send_io(tg111.output_bytes())
    time.sleep(0.1)

    print("Start traversing task")
    tg111.mdi_tarpos.value = 10000
    tg111.mdi_velocity.value = 1200000
    tg111.mdi_acc.value = 16384
    tg111.mdi_dec.value = 16384
    tg111.pos_stw1.activate_mdi = True
    tg111.stw1.activate_traversing_task = True
    cmmt_driver.send_io(tg111.output_bytes())
    time.sleep(0.1)

    while tg111.zsw1.target_position_reached:
        try:
            tg111.input_bytes(cmmt_driver.recv_io())
            time.sleep(0.1)

        except KeyboardInterrupt:
            print("Killed by user!")
            cmmt_driver.stop_io()
            sys.exit(1)

    while not tg111.zsw1.target_position_reached:
        try:
            tg111.input_bytes(cmmt_driver.recv_io())
            print(
                f"Target: {int(tg111.mdi_tarpos)}, Current: {int(tg111.xist_a)}")
            time.sleep(0.1)

        except KeyboardInterrupt:
            print("Killed by user!")
            cmmt_driver.stop_io()
            sys.exit(1)

    print("Target position reached")

    tg111.stw1.enable_operation = False
    cmmt_driver.send_io(tg111.output_bytes())
    time.sleep(0.1)

    cmmt_driver.stop_io()


if __name__ == "__main__":
    main()
