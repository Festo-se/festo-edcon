import argparse
import logging
from edrive.edrive_logging import EDriveLogging


class GenericBusArgParser():
    def __init__(self, desc_str):
        self.desc_str = desc_str
        # Shared options
        self.common = argparse.ArgumentParser()
        self.common.add_argument(
            '-i', '--ip-address', default="192.168.0.51", help='IP address to connect to.')
        self.common.add_argument('-v', '--verbose', action='store_true',
                                 help='Print additional information')

    def add_argument(self, *args, **kwargs):
        return self.common.add_argument(*args, **kwargs)

    def add_subparsers(self, **kwargs):
        return self.common.add_subparsers(**kwargs)

    def create(self):
        # Bus specific options
        parser = argparse.ArgumentParser(description=self.desc_str)
        subparsers = parser.add_subparsers(dest='com_type', required=True,
                                                title='communication types',
                                                description='Valid communication types')
        ethernetip_parser = subparsers.add_parser(
            "ethernetip", add_help=False,
            description='Use EtherNet/IP communication',
            parents=[self.common])
        modbus_parser = subparsers.add_parser(
            "modbus", add_help=False,
            description='Use Modbus communication',
            parents=[self.common])
        modbus_parser.add_argument(
            "--flavour", choices=['CMMT-AS', 'CPX-AP'], default='CMMT-AS', required=False)

        args = parser.parse_args()

        if args.verbose:
            EDriveLogging(logging.INFO)
        else:
            EDriveLogging(logging.WARNING)
        return args
