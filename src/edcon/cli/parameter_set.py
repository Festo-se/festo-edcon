"""CLI Tool to write whole paremeter set EDrive device using .pck file."""
from edcon.edrive.parameter_set import ParameterSet


def add_parameter_set_parser(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_pnu = subparsers.add_parser('parameter-set')
    parser_pnu.set_defaults(func=parameter_set_func)

    parser_pnu.add_argument("file",
                            help="Parameter set to write.")


def parameter_set_func(com, args):
    """Executes subcommand based on provided arguments"""
    parameter_set = ParameterSet(args.file)
    print(com)
    print(parameter_set.parameters)
    # counter = 0
    # for pnuvalue in pnuvalues:
    #     status = edrive.write_pnu_raw(
    #         pnu=pnumap[pnuvalue[0].rsplit('.', 1)[0]], subindex=int(
    #             pnuvalue[0].split('.')[-1]),
    #         num_elements=1, value=pnuvalue[1][::-1])

    #     if status:
    #         counter += 1
    #     else:
    #         logging.error(f"Setting {pnuvalue[0]} to {pnuvalue[1]} failed")

    # print(f"{counter} PNUs succesfully written!")
