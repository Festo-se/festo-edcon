"""CLI Tool to read or write PNUs of a EDrive device."""
from edcon_tools.generic_bus_argparser import GenericBusArgParser
from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_ethernetip import EDriveEthernetip
from collections import namedtuple


def main():
    """Parses command line arguments and reads PNU accordingly."""
    gparser = GenericBusArgParser('Access PNU on an EDrive device.')
    gparser.add_argument("-p", "--pnu", default=3490,
                         help="PNU to use for read/write")
    gparser.add_argument("-s", "--subindex", default=0,
                         help="Subindex to use for read/write")

    subparsers = gparser.add_subparsers(dest='subcommand', required=True,
                                        title='action commands',
                                        description="Action to perform on the PNU")

    # Options for reading PNU
    parser_read = subparsers.add_parser('read')
    parser_read.add_argument(
        '-r', '--raw', help='Raw read of provided number of items')

    # Options for writing PNU
    parser_write = subparsers.add_parser('write')
    parser_write.add_argument('value', help='Value to be written')

    args = gparser.create()

    # Initialize driver
    if args.com_type == 'modbus':
        edrive = EDriveModbus(args.ip_address)
    elif args.com_type == 'ethernetip':
        edrive = EDriveEthernetip(args.ip_address)

    pnu = int(args.pnu)
    subindex = int(args.subindex)
    if args.subcommand == 'read':
        if args.raw:
            pnu_value = edrive.read_pnu_raw(
                pnu, subindex, num_elements=int(args.raw))
            if value:
                print(f"Length: {len(value)}")
        else:
            pnu_value = edrive.read_pnu(pnu, subindex)
        print(f"Value: {pnu_value}")

    elif args.subcommand == 'write':
        edrive.write_pnu(pnu, subindex, args.value)


if __name__ == "__main__":
    main()
