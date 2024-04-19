"""CLI tool that performs a sequence on Telegram1 and EDrive classes."""

import sys
from edcon.edrive.telegram1_handler import Telegram1Handler
from edcon.edrive.com_modbus import ComModbus
from edcon.edrive.com_ethernetip import ComEthernetip


def add_tg1_parser(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_tg1 = subparsers.add_parser("tg1")
    parser_tg1.set_defaults(func=tg1_func)
    parser_tg1.add_argument(
        "-s",
        "--speed-setpoint",
        default="2000",
        help="Speed setpoint to use (default: %(default)s).",
    )


def tg1_func(args):
    """Executes subcommand based on provided arguments"""
    # Initialize driver
    com = (
        ComEthernetip(args.ip_address)
        if args.ethernetip
        else ComModbus(args.ip_address)
    )
    with Telegram1Handler(com, config_mode="write") as tg1:
        if not tg1.acknowledge_faults():
            sys.exit(1)
        if not tg1.enable_powerstage():
            sys.exit(1)
        if not tg1.velocity_task(int(args.speed_setpoint), duration=3.0):
            sys.exit(1)
