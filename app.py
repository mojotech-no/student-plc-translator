"""Module docstring. Write something clever."""

import logging
import logging.config
import sys

from plctranslator.tia_helpers import read_scl_file

from config.config import get_config

_CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)
if _CONFIG.logging is not None:
    logging.config.dictConfig(_CONFIG.logging)
_LOGGER.debug("Some configs..")
_LOGGER.debug(_CONFIG)
_LOGGER.debug(f"A specific nested config: {_CONFIG.mqtt.broker_url}")
_LOGGER.debug("Starting soonish")


if __name__ == "__main__":
    _LOGGER.debug("Starting")
    print(sys.argv[1])  # Use given path to SCL file to translate and dump to terminal as string
    print(sys.argv[2])  # Use given path to check if scl can be translated (true/false)
    read_scl_file(sys.argv[1])
    _LOGGER.info("Ending")
    _LOGGER.debug("")
    _LOGGER.info("")
    _LOGGER.warning("")
    _LOGGER.error("")
    _LOGGER.critical("")
