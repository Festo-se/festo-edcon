"""Contains class which contains logging methods."""
import logging
from rich.logging import RichHandler


class Logging:
    """Class that contains common functions for logging."""

    logger = logging.getLogger('edcon')
    def __init__(self, logging_level=logging.INFO, filename=None):
        Logging.logger.setLevel(logging_level)
        Logging.logger.propagate = False

        if filename:
            self.enable_file_logging(filename, logging_level)
        else:
            self.enable_stream_logging(logging_level)

    def enable_stream_logging(self, logging_level):
        """Enables logging to stream using the provided log level with rich log formatting."""
        ch = RichHandler()
        ch.setLevel(logging_level)
        formatter = logging.Formatter(fmt='%(message)s', datefmt="[%X]")
        ch.setFormatter(formatter)
        Logging.logger.addHandler(ch)

    def enable_file_logging(self, filename, logging_level):
        """Enables logging to a file using the provided filename and log level."""
        ch = logging.FileHandler(filename)
        ch.setLevel(logging_level)
        formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="[%X]")
        ch.setFormatter(formatter)
        Logging.logger.addHandler(ch)