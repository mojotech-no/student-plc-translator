"""Test config module."""

import os
import tomllib
from unittest import TestCase, mock

from config.config import get_config


class TestConfig(TestCase):
    """Test config module.

    Basically, just test that the config module can be loaded.
    """

    test_toml = tomllib.loads(
        """
            show_me_the_bool = true

            [mqtt]
            broker_url = "somewhere:on//the.internet"
            broker_port = 69
            username = "myname"
            password = "1234"
        """
    )

    @mock.patch.dict(os.environ, {"STAGE": "local"})
    def test_get_config_local(self):
        """Test get_config() with STAGE=local."""
        _config = get_config()
        self.assertIsNotNone(_config)

    @mock.patch.dict(os.environ, {"STAGE": "local"})
    @mock.patch("config.config.read_config")
    def test_get_config_local_port_as_int(self, mock_func):
        """Mock return value of read_config, with an int for port."""
        self.test_toml["mqtt"]["broker_port"] = 8833
        mock_func.return_value = self.test_toml
        _config = get_config()
        self.assertIsNotNone(_config)
        self.assertIsInstance(_config.mqtt.broker_port, int)

    @mock.patch.dict(os.environ, {"STAGE": "local"})
    @mock.patch("config.config.read_config")
    def test_get_config_local_port_as_str(self, mock_func):
        """Mock return value of read_config, now with a str for port."""
        self.test_toml["mqtt"]["broker_port"] = "8833"
        mock_func.return_value = self.test_toml
        _config = get_config()
        self.assertIsNotNone(_config)
        self.assertIsInstance(_config.mqtt.broker_port, int)

    @mock.patch.dict(os.environ, {"STAGE": "local"})
    @mock.patch("config.config.read_config")
    def test_get_config_local_port_wrong_type_raises_valueerror(self, mock_func):
        """Mock return value of read_config, now with a str for port that give ValueError."""
        self.test_toml["mqtt"]["broker_port"] = "8833abcd"
        mock_func.return_value = self.test_toml
        self.assertRaises(ValueError, get_config)

        # TODO: handle float. It does not raise error, just rounds it.
        """
        self.test_toml["mqtt"]["broker_port"] = 8833.2
        mock_func.return_value = self.test_toml
        self.assertRaises(ValueError, get_config)
        """

    @mock.patch.dict(
        os.environ,
        {
            "STAGE": "development",
            "ENV_SECRET_SDT_MQTT_BROKER_URL": "somewhere:on//the.internet",
            "ENV_SECRET_SDT_MQTT_BROKER_PORT": "69",
            "ENV_SECRET_SDT_MQTT_USERNAME": "myname",
            "ENV_SECRET_SDT_MQTT_PASSWORD": "1234",
        },
    )
    def test_get_config_development(self):
        """Test get_config() with STAGE=development."""
        _config = get_config()
        self.assertIsNotNone(_config)
