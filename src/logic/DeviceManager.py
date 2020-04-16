import configparser
from datetime import datetime
from typing import Callable

import config_path
import libinfinitton


class DeviceManager:

    def __init__(self, configuration_file_path: config_path.ConfigPath, callback: Callable[[], None] = None):
        self._callback = callback

        self._device_active = False
        self.device = libinfinitton.Infinitton()
        self._config = configparser.ConfigParser()

        path = configuration_file_path.readFilePath()
        if path is None:
            self._config['device'] = {
                'initial_connect': datetime.now().strftime("%d-%b-%Y %H:%M:%S")
            }
            with open(configuration_file_path.saveFilePath(True), 'w') as configfile:
                self._config.write(configfile)
        else:
            self._config.read(path)

        print('Initial device connect: ' + self._config['device']['initial_connect'])

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

        if self._callback is not None:
            self._callback()

    def _on_press(self, key_index):
        print('click ' + str(key_index))
