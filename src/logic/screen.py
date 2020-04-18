import logging
import os
from typing import Dict, Optional, List

import libinfinitton

from . import tasks


class Screen:

    logger = logging.getLogger(__name__)

    def __init__(self, task_list: Dict[str, tasks.BaseTask], name: str, config: dict = None):
        self._task_list = task_list
        self.name = name
        self._keys: List[Optional[tasks.BaseTask]] = [None] * 15

        if config is not None:
            for key_index in range(15):
                if 'key_' + str(key_index) in config:
                    task_name = config['key_' + str(key_index)]
                    self.set_task(key_index, task_name)

    def __get_name(self):
        return self.__name

    def __set_name(self, name: str):
        self.__name = name

    name = property(__get_name, __set_name)

    def set_task(self, key_index: int, task_name: str):
        if task_name in self._task_list:
            self._keys[key_index] = self._task_list[task_name.lower()]
        else:
            Screen.logger.warning('Unknown task: ' + task_name)

    def get_config(self) -> Dict[str, str]:
        config = {}
        for key_index in range(15):
            if self._keys[key_index] is not None:
                config['key_' + str(key_index)] = self._keys[key_index].name
        return config

    def show(self, device: libinfinitton.Infinitton, config_path: str):
        for key_index in range(15):
            self.show_key(device, config_path, key_index)

    def show_key(self, device: libinfinitton.Infinitton, config_path: str, key_index: int):
        if self._keys[key_index] is None:
            device.fill_color(key_index, 0, 0, 0)
        else:
            icon = self._keys[key_index].icon
            if icon is None or icon == '':
                Screen.logger.warning('No icon defined for action: %s of type %s' % (
                    self._keys[key_index].name, type(self._keys[key_index]).__name__))
                device.fill_color(key_index, 255, 255, 255)
            else:
                if os.path.exists(icon) and os.path.isfile(icon):
                    # 1: absolute path: file exists at path
                    Screen.logger.debug('Icon for action is on absolute path: ' + self._keys[key_index].name)
                    device.fill_image_path(key_index, icon)
                elif os.path.exists(os.path.join(config_path, icon)) and os.path.isfile(
                        os.path.join(config_path, icon)):
                    # 2: in config directory
                    Screen.logger.debug('Icon for action is in the config directory: ' + self._keys[key_index].name)
                    device.fill_image_path(key_index, os.path.join(config_path, icon))
                elif os.path.exists(os.path.join(os.getcwd(), 'resources', 'icons', icon)) and os.path.isfile(
                        os.path.join(os.getcwd(), 'resources', 'icons', icon)):
                    # 3: in application resources
                    Screen.logger.debug('Icon for action is in application icon resources: ' + self._keys[key_index].name)
                    device.fill_image_path(key_index, os.path.join(os.getcwd(), 'resources', 'icons', icon))
                else:
                    # Fallback: icon not found
                    Screen.logger.warning('Icon not found for action: %s: %s' % (self._keys[key_index].name, icon))
                    device.fill_color(key_index, 255, 255, 255)

    def execute_key(self, key_index):
        Screen.logger.info('Screen: %s executes task %s' % (self.name, key_index))
        if self._keys[key_index] is not None:
            self._keys[key_index].execute()
