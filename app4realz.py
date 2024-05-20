"""This is the app. It does app things."""

import logging
import logging.config
import sys

from plctranslator import translate

from config.config import get_config

_CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)
if _CONFIG.logging is not None:
    logging.config.dictConfig(_CONFIG.logging)


if __name__ == "__main__":
    """App will read arguments from the command line and translate the files in the input folder.
    The translated files will be saved in the output folder.
    """
    _LOGGER.debug("Starting")
    expected_number_of_arguments = 2 + 1  # 2 arguments + 1 for the script name
    if len(sys.argv) != expected_number_of_arguments:
        _LOGGER.error("Usage: python app4realz.py <input_folder> <output_folder>")
        sys.exit(1)
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    _LOGGER.debug(f"Translating files in {input_folder} to {output_folder}")
    translate(input_folder, output_folder)
