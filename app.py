"""Module docstring. Write something clever."""
import logging
import logging.config

from examplepackage.example_module import Aclass

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
    aclass = Aclass(first_variable=2)
    _LOGGER.info("Ending")
    _LOGGER.debug("")
    _LOGGER.info("")
    _LOGGER.warning("")
    _LOGGER.error("")
    _LOGGER.critical("")
