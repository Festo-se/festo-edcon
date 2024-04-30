"""CLI tool starts the gui"""

import argparse
import logging
from edcon.gui.gui import start_gui
from edcon.utils.logging import Logging


def main():
    """Parses command line arguments and calls corresponding subcommand program."""
    # Bus agnostic options
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

    args = parser.parse_args()
    if args.quiet:
        Logging(logging.WARNING)
    else:
        Logging(logging.INFO)

    start_gui(args.ip_address)


if __name__ == "__main__":
    main()
