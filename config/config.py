"""Configuration module."""

import logging
import os
import re
import time
import tomllib
from dataclasses import dataclass
from pathlib import Path

from dacite import Config as daciteConfig
from dacite import from_dict


@dataclass
class MqttConfig:
    """MQTT configuration."""

    broker_url: str
    broker_port: int
    username: str
    password: str


@dataclass
class Config:
    """Dataclass for all configs."""

    mqtt: MqttConfig
    logging: dict | None
    show_me_the_bool: bool | None


def log_and_time(func):
    """Decorate a function to log and time its execution.

    Args:
    ----
        func: The function to be decorated.
    ----

    Returns:
    -------
        The decorated function.
    -------
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        logging.info(f"Starting {func.__name__}...")
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"{func.__name__} finished in {end_time - start_time} seconds.")
        return result

    return wrapper


def get_config() -> Config:
    """Read configs from toml and return Config class object."""
    config_dict = load_config()
    return from_dict(data_class=Config, data=config_dict, config=daciteConfig(cast=[int]))


def load_config():
    """Load configuration based on the environment variable STAGE.

    If STAGE is not set, default to "local".
    """
    environment = os.environ.get("STAGE") or "local"
    _config = {}
    match environment:
        case "local":
            local_config = read_config("local")
            _config.update(local_config)
        case "development":
            dev_config = read_config(environment)
            _config.update(dev_config)
        case "production":
            prod_config = read_config(environment)
            _config.update(prod_config)
        case other:
            raise ValueError(f"Unknown environment: {other}")
    return _config


def read_config(env: str):
    """Read configuration environment."""
    config_path = Path(__file__).parent / f"{env}.toml"
    with config_path.open("rb") as file:
        config = tomllib.load(file)
    replace_env_vars(config)
    return config


def replace_env_vars(dictionary: dict):
    """Replace values in a dictionary with environment variables.

    If an environment variable is not found, the value is not changed.
    If an environment variable is found, the value is replaced with the environment variable's value.

    Args: dictionary: The dictionary to be updated.

    """
    for key, value in dictionary.items():
        if isinstance(value, dict):
            replace_env_vars(value)
        elif env_var_match := re.fullmatch(r"\$\{(.*)\}", str(value)):
            env_var = env_var_match.group(1)
            dictionary[key] = os.environ.get(env_var)
