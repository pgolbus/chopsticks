from dataclasses import dataclass
import logging
import sys


@dataclass
class Player:
    left: int
    right: int


def setup_logger():
    """
    Sets up the logger with a timestamp and stderr handler.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the desired logging level here

    # Create a console handler that logs to stderr
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)

    # Create a formatter with a timestamp
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add the formatter to the handler
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger

logger = setup_logger()