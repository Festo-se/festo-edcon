"""CLI tool that performs a sequence on Telegram1 and EDrive classes."""
import sys
from edrive.telegram_executors.telegram1_executor import Telegram1Executor


def add_tg1_args(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_tg1 = subparsers.add_parser('tg1')
    parser_tg1.set_defaults(func=tg1_func)
    parser_tg1.add_argument(
        '-s', '--speed-setpoint', default="2000", help='Speed setpoint to use')


def tg1_func(edrive, args):
    """Executes subcommand based on provided arguments"""
    with Telegram1Executor(edrive) as tg1:
        if not tg1.acknowledge_faults():
            sys.exit(1)
        if not tg1.enable_powerstage():
            sys.exit(1)
        if not tg1.velocity_task(int(args.speed_setpoint), duration=3.0):
            sys.exit(1)
