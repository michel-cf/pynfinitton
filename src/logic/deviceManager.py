import configparser
import logging
import os
from typing import Callable, Optional, Dict

import config_path
import libinfinitton

from . import configs, screen, tasks, deviceAccessor


class DeviceManager(configs.ApplicationConfig, configs.DeviceConfig, deviceAccessor.DeviceAccessor):
    __TASK_TYPES = {
        'type': tasks.TypeTask,
        'screen': tasks.ScreenTask,
        'web-page': tasks.WebPageTask
    }
    logger = logging.getLogger(__name__)

    def __init__(self, configuration_file_path: config_path.ConfigPath, callback: Callable[[], None] = None):
        self._callback = callback

        self._active_screen: Optional[screen.Screen] = None  # To be initialized later

        self._device_active = False
        self.device = libinfinitton.Infinitton()
        self.__config = configparser.ConfigParser()
        self._configuration_file_path = configuration_file_path

        path = configuration_file_path.readFolderPath(True)
        config_file = os.path.join(path, 'config.ini')
        if os.path.exists(config_file) and os.path.isfile(config_file):
            self._config.read(config_file)

        self.tasks = self._parse_tasks()
        self.screens = self._parse_screens()

        if len(self.screens) == 0:
            self.screens['main'] = screen.Screen(self.tasks, 'main')

        self.config_screen = 'main'

        self.device.on('down', self._on_press)
        if not self.try_connect():
            # todo start retry thread
            pass

    # USB Infinitton device methods
    @staticmethod
    def is_connected():
        return libinfinitton.Infinitton.is_present()

    def try_connect(self) -> bool:
        if self._device_active:
            return True
        if self.is_connected():
            self.device.connect()
            self._device_active = True

            self._on_connect()
            return True

        return False

    def is_active(self) -> bool:
        return self._device_active

    def _on_connect(self) -> None:
        self._set_connect_time()
        self.show_screen('main')

        if self._callback is not None:
            self._callback()

    def _on_press(self, key_index: int):
        self._active_screen.execute_key(key_index)

    # Config methods
    def _persist_config(self):
        path = self._configuration_file_path.saveFolderPath(True)
        config_file = os.path.join(path, 'config.ini')

        with open(config_file, 'w') as configfile:
            self._config.write(configfile)

    @property
    def _config(self):
        return self.__config

    # Tasks methods
    def _parse_tasks(self) -> Dict[str, tasks.BaseTask]:
        task_list = {}
        for key in self._config:
            if key[:5] == 'Task:':
                task_name = key[5:]
                task = self._parse_task(task_name, key)
                if task is not None:
                    task_list[task_name.lower()] = task

        return task_list

    def _parse_task(self, task_name: str, task_key: str) -> Optional[tasks.BaseTask]:
        task_config = self._config[task_key]
        task_type = task_config['type']

        if task_type in DeviceManager.__TASK_TYPES:
            return DeviceManager.__TASK_TYPES[task_type](self, task_name, task_config)

        DeviceManager.logger.warning('Unknown task type: ' + task_type)
        return None

    # Screen methods
    def _parse_screens(self) -> Dict[str, screen.Screen]:
        screen_list = {}
        for key in self._config:
            if key[:7] == 'Screen:':
                screen_name = key[7:]
                screen_list[screen_name.lower()] = self._parse_screen(screen_name, key)

        return screen_list

    def _parse_screen(self, screen_name: str, screen_key: str) -> screen.Screen:
        screen_config = self._config[screen_key]

        return screen.Screen(self.tasks, screen_name, screen_config)

    def show_screen(self, screen_name: str):
        self._active_screen = self.screens[screen_name.lower()]
        self._active_screen.show(self.device, self._configuration_file_path.readFolderPath())

    def __get_config_screen(self) -> screen.Screen:
        return self._config_screen

    def __set_config_screen(self, name: str):
        self._config_screen = self.screens[name]

    config_screen = property(__get_config_screen, __set_config_screen)

    def make_unique_task_name(self, name: str):
        if name.lower() in self.tasks:
            unique = 0
            unique_name = name + ' ' + str(unique)
            while unique_name.lower() in self.tasks:
                unique_name = name + ' ' + str(unique)
                unique += 1
            return unique_name
        else:
            return name

    def get_icon_folder(self):
        return os.path.join(self._configuration_file_path.saveFolderPath(), 'icons')
