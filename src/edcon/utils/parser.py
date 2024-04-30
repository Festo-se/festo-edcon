"""Helper functions for common parser arguments"""

import argparse


class Parser(argparse.ArgumentParser):
    """Class which provides common parser arguments"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_argument(
            "-i",
            "--ip-address",
            default="192.168.0.1",
            help="IP address to connect to (default: %(default)s).",
        )

        self.add_argument(
            "-q", "--quiet", action="store_true", help="suppress output verbosity"
        )
