"""CLI tool that performs a sequence on Telegram9 and EDrive classes."""
import sys
from edcon.edrive.telegram_executors.telegram9_executor import Telegram9Executor


def add_tg9_args(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_tg9 = subparsers.add_parser('tg9')
    parser_tg9.set_defaults(func=tg9_func)

    parser_tg9.add_argument('-p', '--position', default="10000",
                            help='Target position to be reached')


def tg9_func(edrive, args):
    """Executes subcommand based on provided arguments"""
    with Telegram9Executor(edrive) as tg9:
        if not tg9.acknowledge_faults():
            sys.exit(1)
        if not tg9.enable_powerstage():
            sys.exit(1)
        if not tg9.referencing_task():
            sys.exit(1)
        tg9.position_task(position=int(args.position), velocity=600000)
