"""CLI Tool that distributes subcommands"""
import argparse
import logging
from edcon.cli.position import add_position_args
from edcon.cli.pnu import add_pnu_args
from edcon.cli.tg1 import add_tg1_args
from edcon.cli.tg9 import add_tg9_args
from edcon.cli.tg102 import add_tg102_args
from edcon.cli.tg111 import add_tg111_args
from edcon.utils.logging import Logging
from edcon.edrive.com_modbus import ComModbus
from edcon.edrive.com_ethernetip import ComEthernetip


def main():
    """Parses command line arguments and calls corresponding subcommand program."""
    # Bus agnostic options
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-i', '--ip-address', default="192.168.0.51", help='IP address to connect to.')

    # Bus specific options
    parser.add_argument('--ethernetip', action='store_true',
                        help='use EtherNet/IP (instead of ModbusTCP) as underlying communication.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')

    subparsers = parser.add_subparsers(dest='subcommand', required=True,
                                       title='subcommands',
                                       help="Subcommand that should be called")

    # Options for position
    add_position_args(subparsers)

    # Options for pnu
    add_pnu_args(subparsers)

    # Options for tg1
    add_tg1_args(subparsers)

    # Options for tg9
    add_tg9_args(subparsers)

    # Options for tg102
    add_tg102_args(subparsers)

    # Options for tg111
    add_tg111_args(subparsers)

    args = parser.parse_args()
    if args.verbose:
        Logging(logging.INFO)
    else:
        Logging(logging.WARNING)

    # Initialize driver
    if args.ethernetip:
        edrive = ComEthernetip(args.ip_address)
    else:
        edrive = ComModbus(args.ip_address)

    args.func(edrive, args)


if __name__ == "__main__":
    main()
