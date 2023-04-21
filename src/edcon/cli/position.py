"""CLI tool to execute positioning tasks using MotionExecutor."""
import sys
import traceback
from edcon.edrive.motion import MotionExecutor


def add_position_args(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_position = subparsers.add_parser('position')
    parser_position.set_defaults(func=position_func)

    parser_position.add_argument('-p', '--position', default="10000",
                                 help='Target position to be reached')
    parser_position.add_argument('-s', '--speed', default="600000",
                                 help='Speed used for positioning task')
    parser_position.add_argument('-a', '--absolute', action='store_true',
                                 help='Use absolute positioning mode')
    parser_position.add_argument('-r', '--reference', action='store_true',
                                 help='Perform a referencing task before positioning task')


def position_func(edrive, args):
    """Executes subcommand based on provided arguments"""
    try:
        with MotionExecutor(edrive) as mot:
            if not mot.acknowledge_faults():
                sys.exit(1)
            if not mot.enable_powerstage():
                sys.exit(1)

            if args.reference:
                if not mot.referencing_task():
                    sys.exit(1)

            mot.position_task(position=int(args.position),
                              velocity=int(args.speed), absolute=args.absolute)
    except ConnectionError:
        print(traceback.format_exc())
