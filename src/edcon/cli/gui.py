"""CLI tool starts the gui"""

import logging
from edcon.gui.gui import start_gui
from edcon.utils.logging import Logging
from edcon.utils.parser import Parser


def main():
    """Parses command line arguments and calls corresponding subcommand program."""
    parser = Parser()

    args = parser.parse_args()

    Logging(logging.WARNING if args.quiet else logging.INFO)

    start_gui(args.ip_address)


if __name__ == "__main__":
    main()
