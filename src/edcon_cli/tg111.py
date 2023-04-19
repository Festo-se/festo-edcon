"""CLI tool that performs a sequence on Telegram111 and EDrive classes."""
import sys
from edrive.telegram_executors.telegram111_executor import Telegram111Executor


def add_tg111_args(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_tg111 = subparsers.add_parser('tg111')
    parser_tg111.set_defaults(func=tg111_func)


def tg111_func(edrive, args):
    """Executes subcommand based on provided arguments"""
    with Telegram111Executor(edrive) as tg111:
        tg111.telegram.override.value = 16384
        if not tg111.acknowledge_faults():
            sys.exit(1)
        if not tg111.enable_powerstage():
            sys.exit(1)
        if not tg111.set_current_position_task():
            sys.exit(1)
        tg111.position_task(position=1000000, velocity=60000)
