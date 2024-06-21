"""CLI Tool that distributes subcommands"""

import logging
import argparse
from edcon.cli.position import add_position_parser
from edcon.cli.pnu import add_pnu_parser
from edcon.cli.parameter_set_load import add_parameter_set_load_parser
from edcon.cli.tg1 import add_tg1_parser
from edcon.cli.tg9 import add_tg9_parser
from edcon.cli.tg102 import add_tg102_parser
from edcon.cli.tg111 import add_tg111_parser
from edcon.utils.logging import Logging

# pylint: disable=duplicate-code
# CLI and GUI have similar options


def main():
    """Parses command line arguments and calls corresponding subcommand program."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--ip-address",
        default="192.168.0.1",
        help="IP address to connect to (default: %(default)s).",
    )

    parser.add_argument(
        "-q", "--quiet", action="store_true", help="suppress output verbosity"
    )

    # Bus specific options
    parser.add_argument(
        "--ethernetip",
        action="store_true",
        help="use EtherNet/IP (instead of ModbusTCP) as underlying communication.",
    )

    subparsers = parser.add_subparsers(
        dest="subcommand",
        required=True,
        title="subcommands",
        help="Subcommand that should be called",
    )

    # Options for position
    add_position_parser(subparsers)

    # Options for pnu
    add_pnu_parser(subparsers)

    # Options for parameter_set
    add_parameter_set_load_parser(subparsers)

    # Options for tg1
    add_tg1_parser(subparsers)

    # Options for tg9
    add_tg9_parser(subparsers)

    # Options for tg102
    add_tg102_parser(subparsers)

    # Options for tg111
    add_tg111_parser(subparsers)

    args = parser.parse_args()

    Logging(logging.WARNING if args.quiet else logging.INFO)

    args.func(args)


if __name__ == "__main__":
    main()
