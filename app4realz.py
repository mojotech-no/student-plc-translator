"""This is the app. It does app things."""

import logging
import logging.config
import sys

from config.config import get_config
from plctranslator import translate

_CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)
if _CONFIG.logging is not None:
    logging.config.dictConfig(_CONFIG.logging)


if __name__ == "__main__":
    """App will read arguments from the command line and translate a single scl file.
    The translated file will be saved in the output folder.
    """
    _LOGGER.debug("Starting")
    expected_number_of_arguments = 2 + 1  # 2 arguments + 1 for the script name
    if len(sys.argv) != expected_number_of_arguments:
        _LOGGER.error("Usage: python app4realz.py <input_file> <output_folder>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_folder = sys.argv[2]

    _LOGGER.debug(f"Translating {input_file} to {output_folder}")
    translate(input_file, output_folder)
