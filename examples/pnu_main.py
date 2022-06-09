"""CLI Tool to read or write PNUs of a CMMT device."""

import argparse
import logging

from cmmt.cmmt_modbus import CmmtModbus
from cmmt.cmmt_ethernetip import CmmtEthernetip


def main():
    """Parses command line arguments and reads PNU accordingly."""
    parser = argparse.ArgumentParser(
        description='Read a PNU from a CMMT device.')
    parser.add_argument('-c', '--com', choices=['modbus', 'ethernetip'], default='modbus',
                        help='Communication mode to use (default: %(default)s)')
    parser.add_argument('-i', '--ip-address', default="192.168.0.51",
                        help='IP address to connect to.')
    parser.add_argument("-p", "--pnu", default=3490,
                        help="PNU to use for read/write")
    parser.add_argument("-s", "--subindex", default=0,
                        help="Subindex to use for read/write")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print additional information')

    subparsers = parser.add_subparsers(dest='subcommand', required=True,
                                       description="Action to perform",
                                       help="Action to perform on the PNU")

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

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(message)s', level=logging.INFO)

    # Initialize driver
    if args.com == 'modbus':
        cmmt_driver = CmmtModbus(args.ip_address)
    elif args.com == 'ethernetip':
        cmmt_driver = CmmtEthernetip(args.ip_address)

    pnu = int(args.pnu)
    subindex = int(args.subindex)
    if args.subcommand == 'read':
        if args.b:
            value = cmmt_driver.read_pnu(pnu, subindex, '?')
        if args.u8:
            value = cmmt_driver.read_pnu(pnu, subindex, 'B')
        if args.i8:
            value = cmmt_driver.read_pnu(pnu, subindex, 'b')
        if args.i16:
            value = cmmt_driver.read_pnu(pnu, subindex, 'h')
        if args.i32:
            value = cmmt_driver.read_pnu(pnu, subindex, 'i')
        if args.i64:
            value = cmmt_driver.read_pnu(pnu, subindex, 'q')
        elif args.f:
            value = cmmt_driver.read_pnu(pnu, subindex, 'f')
        elif args.r:
            value = cmmt_driver.read_pnu_raw(
                pnu, subindex, num_elements=int(args.r))
            print(int(args.r))
            print(f"Length: {len(value)}")
        print(f"Value: {value}")

    elif args.subcommand == 'write':
        if args.b:
            cmmt_driver.write_pnu(pnu, subindex, int(args.b), '?')
        if args.u8:
            cmmt_driver.write_pnu(pnu, subindex, int(args.u8), 'B')
        if args.i8:
            cmmt_driver.write_pnu(pnu, subindex, int(args.i8), 'b')
        if args.i16:
            cmmt_driver.write_pnu(pnu, subindex, int(args.i16), 'h')
        if args.i32:
            cmmt_driver.write_pnu(pnu, subindex, int(args.i32), 'i')
        if args.i64:
            cmmt_driver.write_pnu(pnu, subindex, int(args.i64), 'q')
        elif args.f:
            cmmt_driver.write_pnu(pnu, subindex, float(args.f), 'f')


if __name__ == "__main__":
    main()
