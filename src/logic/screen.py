import logging
from typing import Dict, Optional, List

import libinfinitton

from . import tasks


class Screen:

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
            self._keys[key_index] = self._task_list[task_name]
        else:
            logging.warning('Unknown task: ' + task_name)

    def get_config(self) -> Dict[str, str]:
        config = {}
        for key_index in range(15):
            if self._keys[key_index] is not None:
                config['key_' + str(key_index)] = self._keys[key_index].name
        return config

    def show(self, device: libinfinitton.Infinitton):
        for key_index in range(15):
            if self._keys[key_index] is None:
                device.fill_color(key_index, 0, 0, 0)
            else:
                # TODO show task icon
                device.fill_color(key_index, 255, 255, 255)

    def execute_key(self, key_index):
        logging.info('Screen: %s executes task %s' % (self.name, key_index))
        if self._keys[key_index] is not None:
            self._keys[key_index].execute()
