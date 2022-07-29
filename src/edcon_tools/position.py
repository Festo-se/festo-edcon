"""Example on how to use EDrivePositioning."""

import argparse
import logging

from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_ethernetip import EDriveEthernetip
from edrive.edrive_positioning import EDrivePositioning


def main():
    """Parses command line arguments and run the example."""
    parser = argparse.ArgumentParser(
        description='Control EDrive device.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--modbus', action='store_true',
                       help='Use Modbus communication')
    group.add_argument('--ethernetip', action='store_true',
                       help='Use EtherNet/IP communication')
    parser.add_argument('-i', '--ip-address', default="192.168.0.51",
                        help='IP address to connect to.')
    parser.add_argument('-p', '--position', default="10000",
                        help='Target position to be reached')
    parser.add_argument('-s', '--speed', default="600000",
                        help='Speed used for positioning task')
    parser.add_argument('-a', '--absolute', action='store_true',
                        help='Use absolute positioning mode')
    parser.add_argument('--homing', action='store_true',
                        help='Peform homing before positioning task')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print additional information')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(message)s', level=logging.INFO)

    # Initialize driver
    if args.modbus:
        edrive = EDriveModbus(args.ip_address)
    elif args.ethernetip:
        edrive = EDriveEthernetip(args.ip_address)

    with EDrivePositioning(edrive) as edpos:
        edpos.request_plc_control()
        edpos.acknowledge_faults()
        edpos.enable_powerstage()

        if args.homing:
            edpos.homing_task()

        edpos.position_task(position=int(args.position),
                            velocity=int(args.speed), absolute=args.absolute)


if __name__ == "__main__":
    main()
