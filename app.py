"""Module docstring. Write something clever."""

import io
import logging
import logging.config
import sys
from logging import StreamHandler

from config.config import get_config
from src.plctranslator.tia_helpers import read_scl_file
from src.plctranslator.tia_translator import check, translate

log_stream = io.StringIO()
stream_handler = StreamHandler(log_stream)
_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(stream_handler)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)


_CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)
if _CONFIG.logging is not None:
    logging.config.dictConfig(_CONFIG.logging)


if __name__ == "__main__":
    _LOGGER.info("Starting")
    _LOGGER.info("Starting")

    logged_text = log_stream.getvalue()
    print(logged_text)
    _LOGGER.debug("Starting")
    print(sys.argv[1])  # Use given path to SCL file to translate and dump to terminal as string
    full_text = read_scl_file(sys.argv[1])

    check(full_text)
    translate(full_text, sys.argv[2])
