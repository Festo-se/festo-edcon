"""CLI Tool to read or write PNUs of a EDrive device."""
from edcon_tools.generic_bus_argparser import GenericBusArgParser
from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_ethernetip import EDriveEthernetip


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
    group_dtype = parser_read.add_mutually_exclusive_group(required=True)
    group_dtype.add_argument('-b', action='store_true',
                             help='read bool data')
    group_dtype.add_argument('-u8', action='store_true',
                             help='read uint8 data')
    group_dtype.add_argument('-i8', action='store_true',
                             help='read int8 data')
    group_dtype.add_argument('-i16', action='store_true',
                             help='read int16 data')
    group_dtype.add_argument('-i32', action='store_true',
                             help='read int32 data')
    group_dtype.add_argument('-i64', action='store_true',
                             help='read int64 data')
    group_dtype.add_argument('-f', action='store_true',
                             help='read float data')
    group_dtype.add_argument('-r', help='length of raw data to read')

    # Options for writing PNU
    parser_write = subparsers.add_parser('write')
    group_dtype = parser_write.add_mutually_exclusive_group(required=True)
    group_dtype.add_argument('-b', help='bool data to write')
    group_dtype.add_argument('-u8', help='uint8 data to write')
    group_dtype.add_argument('-i8', help='int8 data to write')
    group_dtype.add_argument('-i16', help='int16 data to write')
    group_dtype.add_argument('-i32', help='int32 data to write')
    group_dtype.add_argument('-i64', help='int64 data to write')
    group_dtype.add_argument('-f', help='float data to write')

    args = gparser.create()

    # Initialize driver
    if args.com_type == 'modbus':
        edrive = EDriveModbus(args.ip_address, flavour=args.flavour)
    elif args.com_type == 'ethernetip':
        edrive = EDriveEthernetip(args.ip_address)

    pnu = int(args.pnu)
    subindex = int(args.subindex)
    if args.subcommand == 'read':
        if args.b:
            value = edrive.read_pnu(pnu, subindex, '?')
        if args.u8:
            value = edrive.read_pnu(pnu, subindex, 'B')
        if args.i8:
            value = edrive.read_pnu(pnu, subindex, 'b')
        if args.i16:
            value = edrive.read_pnu(pnu, subindex, 'h')
        if args.i32:
            value = edrive.read_pnu(pnu, subindex, 'i')
        if args.i64:
            value = edrive.read_pnu(pnu, subindex, 'q')
        elif args.f:
            value = edrive.read_pnu(pnu, subindex, 'f')
        elif args.r:
            value = edrive.read_pnu_raw(
                pnu, subindex, num_elements=int(args.r))
            if value:
                print(f"Length: {len(value)}")
        print(f"Value: {value}")

    elif args.subcommand == 'write':
        if args.b:
            edrive.write_pnu(pnu, subindex, int(args.b), '?')
        if args.u8:
            edrive.write_pnu(pnu, subindex, int(args.u8), 'B')
        if args.i8:
            edrive.write_pnu(pnu, subindex, int(args.i8), 'b')
        if args.i16:
            edrive.write_pnu(pnu, subindex, int(args.i16), 'h')
        if args.i32:
            edrive.write_pnu(pnu, subindex, int(args.i32), 'i')
        if args.i64:
            edrive.write_pnu(pnu, subindex, int(args.i64), 'q')
        elif args.f:
            edrive.write_pnu(pnu, subindex, float(args.f), 'f')


if __name__ == "__main__":
    main()
