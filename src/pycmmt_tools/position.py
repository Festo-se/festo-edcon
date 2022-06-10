"""Example on how to use CmmtPositionFunctionBlock."""

import sys
import argparse
import logging

from cmmt.cmmt_modbus import CmmtModbus
from cmmt.cmmt_ethernetip import CmmtEthernetip
from cmmt.cmmt_position_function_block import CmmtPositionFunctionBlock


def main():
    """Parses command line arguments and run the example."""
    parser = argparse.ArgumentParser(
        description='Control CMMT device.')
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

    try:
        fblock = CmmtPositionFunctionBlock(cmmt_driver)

        fblock.request_plc_control()
        fblock.acknowledge_faults()
        fblock.enable_powerstage()
        fblock.homing_task()
        fblock.position_task(position=10000, velocity=600000)

    except KeyboardInterrupt:
        print("Killed by user!")
        del fblock
        sys.exit(1)


if __name__ == "__main__":
    main()
