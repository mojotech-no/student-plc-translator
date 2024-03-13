"""Module docstring. Write something clever."""

import logging
import logging.config
import sys

from plctranslator import check, read_scl_file, translate

from config.config import get_config

_CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)
if _CONFIG.logging is not None:
    logging.config.dictConfig(_CONFIG.logging)


if __name__ == "__main__":
    _LOGGER.debug("Starting")
    print(sys.argv[1])  # Use given path to SCL file to translate and dump to terminal as string
    full_text = read_scl_file(sys.argv[1])
    check(full_text)
    translate(full_text, sys.argv[2])
