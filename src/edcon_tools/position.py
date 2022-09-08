"""CLI tool to execute positioning tasks using EDriveMotion."""
from edcon_tools.generic_bus_argparser import GenericBusArgParser
from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_ethernetip import EDriveEthernetip
from edrive.edrive_motion import EDriveMotion


def main():
    """Parses command line arguments and run the example."""
    gparser = GenericBusArgParser('Control EDrive device.')
    gparser.add_argument('-p', '--position', default="10000",
                         help='Target position to be reached')
    gparser.add_argument('-s', '--speed', default="600000",
                         help='Speed used for positioning task')
    gparser.add_argument('-a', '--absolute', action='store_true',
                         help='Use absolute positioning mode')
    gparser.add_argument('-r', '--reference', action='store_true',
                         help='Perform a referencing task before positioning task')

    args = gparser.create()

    # Initialize driver
    if args.com_type == 'modbus':
        edrive = EDriveModbus(args.ip_address, flavour=args.flavour)
    elif args.com_type == 'ethernetip':
        edrive = EDriveEthernetip(args.ip_address)

    with EDriveMotion(edrive) as mot:
        mot.acknowledge_faults()
        mot.enable_powerstage()

        if args.reference:
            mot.referencing_task()

        mot.position_task(position=int(args.position),
                          velocity=int(args.speed), absolute=args.absolute)


if __name__ == "__main__":
    main()
