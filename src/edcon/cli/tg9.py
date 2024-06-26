"""CLI tool that performs a sequence on Telegram9 and EDrive classes."""

import sys
from edcon.edrive.telegram9_handler import Telegram9Handler
from edcon.edrive.com_modbus import ComModbus
from edcon.edrive.com_ethernetip import ComEthernetip


def add_tg9_parser(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_tg9 = subparsers.add_parser("tg9")
    parser_tg9.set_defaults(func=tg9_func)

    parser_tg9.add_argument(
        "-p",
        "--position",
        default="10000",
        help="Target position to be reached (default: %(default)s).",
    )


def tg9_func(args):
    """Executes subcommand based on provided arguments"""
    # Initialize driver
    com = (
        ComEthernetip(args.ip_address)
        if args.ethernetip
        else ComModbus(args.ip_address)
    )
    with Telegram9Handler(com, config_mode="write") as tg9:
        if not tg9.acknowledge_faults():
            sys.exit(1)
        if not tg9.enable_powerstage():
            sys.exit(1)
        if not tg9.referencing_task():
            sys.exit(1)
        tg9.position_task(position=int(args.position), velocity=600000)
