"""CLI tool starts the gui"""

from edcon.gui.gui import start_gui


def add_gui_parser(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_gui = subparsers.add_parser("gui")
    parser_gui.set_defaults(func=gui_func)


def gui_func(args):
    """Executes subcommand based on provided arguments"""
    start_gui(args.ip_address)
