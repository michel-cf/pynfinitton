import configparser
from typing import Callable

import config_path
import libinfinitton

from . import configs


class DeviceManager(configs.ApplicationConfig, configs.DeviceConfig):

    def __init__(self, configuration_file_path: config_path.ConfigPath, callback: Callable[[], None] = None):
        self._callback = callback

        self._device_active = False
        self.device = libinfinitton.Infinitton()
        self.__config = configparser.ConfigParser()
        self._configuration_file_path = configuration_file_path

        path = configuration_file_path.readFilePath()
        if path is None:
            self.locale = 'en'
        else:
            self._config.read(path)

        self.device.on('down', self._on_press)
        self.try_connect()

    @staticmethod
    def is_connected():
        return libinfinitton.Infinitton.is_present()

    def try_connect(self) -> None:
        if not self._device_active and self.is_connected():
            self.device.connect()
            self._device_active = True

            self._on_connect()

    def is_active(self) -> bool:
        return self._device_active

    def _on_connect(self) -> None:
        self._set_connect_time()

        if self._callback is not None:
            self._callback()

    def _on_press(self, key_index):
        print('click ' + str(key_index))

    def _persist_config(self):
        with open(self._configuration_file_path.saveFilePath(True), 'w') as configfile:
            self._config.write(configfile)

    @property
    def _config(self):
        return self.__config
