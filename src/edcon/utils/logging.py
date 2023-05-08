"""Contains class which contains logging methods."""
import logging
from rich.logging import RichHandler


class Logging:
    """Class that contains common functions for logging."""

    def __init__(self, logging_level=logging.INFO, filename=None):
        if filename:
            self.enable_file_logging(filename, logging_level)
        else:
            self.enable_stream_logging(logging_level)

    def enable_stream_logging(self, logging_level):
        """Enables logging to stream using the provided log level with rich log formatting."""
        logging.basicConfig(level=logging_level,
                            format='%(message)s',
                            datefmt="[%X]",
                            handlers=[RichHandler()])

    def enable_file_logging(self, filename, logging_level):
        """Enables logging to a file using the provided filename and log level."""
        self.filename = filename
        logging.basicConfig(filename=filename,
                            level=logging_level,
                            format='%(message)s',
                            datefmt="[%X]")
