"""Example on how to use EDrivePositioning."""
from edcon_tools.generic_bus_argparser import GenericBusArgParser
from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_ethernetip import EDriveEthernetip
from edrive.edrive_positioning import EDrivePositioning


def main():
    """Parses command line arguments and run the example."""
    gparser = GenericBusArgParser('Control EDrive device.')
    gparser.add_argument('-p', '--position', default="10000",
                         help='Target position to be reached')
    gparser.add_argument('-s', '--speed', default="600000",
                         help='Speed used for positioning task')
    gparser.add_argument('-a', '--absolute', action='store_true',
                         help='Use absolute positioning mode')
    gparser.add_argument('--homing', action='store_true',
                         help='Perform homing before positioning task')

    args = gparser.create()

    # Initialize driver
    if args.com_type == 'modbus':
        edrive = EDriveModbus(args.ip_address, flavour=args.flavour)
    elif args.com_type == 'ethernetip':
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
