"""CLI Tool to write whole paremeter set EDrive device using .pck file."""
from edcon.utils.logging import Logging
from edcon.edrive.parameter_set import ParameterSet
from edcon.edrive.parameter_handler import ParameterHandler


def add_parameter_set_load_parser(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_pnu = subparsers.add_parser('parameter-set-load')
    parser_pnu.set_defaults(func=parameter_set_load_func)

    parser_pnu.add_argument("file",
                            help="Parameter set to write.")


def parameter_set_load_func(com, args):
    """Executes subcommand based on provided arguments"""
    parameter_set = ParameterSet(args.file)
    parameter_handler = ParameterHandler(com)

    counter = 0
    for parameter in parameter_set:
        status = parameter_handler.write(parameter_uid=parameter.uid(),
                                         value=parameter.value,
                                         subindex=parameter.subindex,
                                         raw=True)
        if status:
            counter += 1
        else:
            Logging.logger.error(
                f"Setting {parameter.uid()} at subindex {parameter.subindex} "
                f"to {parameter.value} failed")

    print(f"{counter} PNUs succesfully written!")
