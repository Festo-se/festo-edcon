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

    Type = namedtuple('Type', ['verbose_type', 'struct_char'])
    supported_types = {
        'b': Type('bool', '?'),
        'u8': Type('uint8', 'B'),
        'i8': Type('int8', 'b'),
        'u16': Type('uint16', 'H'),
        'i16': Type('int16', 'h'),
        'u32': Type('uint32', 'I'),
        'i32': Type('int32', 'i'),
        'u64': Type('uint64', 'Q'),
        'i64': Type('int64', 'q'),
        'f': Type('float', 'f'),
        'd': Type('double', 'd'),
    }
    # Options for reading PNU
    parser_read = subparsers.add_parser('read')
    group_dtype = parser_read.add_mutually_exclusive_group(required=True)
    for key, value in supported_types.items():
        group_dtype.add_argument(
            f'-{key}', f'--{value.verbose_type}', action='store_true', help=f'read {value.verbose_type} data')
    group_dtype.add_argument(
        '-r', '--raw', help='Raw read of provided number of items')

    # Options for writing PNU
    parser_write = subparsers.add_parser('write')
    group_dtype = parser_write.add_mutually_exclusive_group(required=True)
    for key, value in supported_types.items():
        group_dtype.add_argument(
            f'-{key}', f'--{value.verbose_type}', help=f'{value.verbose_type} data to write')

    args = gparser.create()

    # Initialize driver
    if args.com_type == 'modbus':
        edrive = EDriveModbus(args.ip_address, flavour=args.flavour)
    elif args.com_type == 'ethernetip':
        edrive = EDriveEthernetip(args.ip_address)

    pnu = int(args.pnu)
    subindex = int(args.subindex)
    if args.subcommand == 'read':
        for key, value in supported_types.items():
            if getattr(args, value.verbose_type):
                pnu_value = edrive.read_pnu(pnu, subindex, value.struct_char)
        if args.raw:
            pnu_value = edrive.read_pnu_raw(
                pnu, subindex, num_elements=int(args.raw))
            if value:
                print(f"Length: {len(value)}")
        print(f"Value: {pnu_value}")

    elif args.subcommand == 'write':
        for key, value in supported_types.items():
            type_arg = getattr(args, value.verbose_type)
            if type_arg:
                edrive.write_pnu(pnu, subindex, int(
                    type_arg), value.struct_char)


if __name__ == "__main__":
    main()
