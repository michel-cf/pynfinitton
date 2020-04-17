from typing import Dict, Optional, List

from . import tasks


class Screen:

    def __init__(self, task_list: Dict[str, tasks.BaseTask], name: str, config: dict = None):
        self._task_list = task_list
        self.name = name
        self._keys: List[Optional[tasks.BaseTask]] = [None] * 15

        if config is not None:
            for key_index in range(15):
                if 'key_' + str(key_index) in config:
                    self._keys[key_index] = task_list[config['key_' + str(key_index)]]

    def __get_name(self):
        return self.__name

    def __set_name(self, name: str):
        self.__name = name

    name = property(__get_name, __set_name)

    def execute_key(self, key_index):
        print('Screen: %s executes task %s' % (self.name, key_index))
        if self._keys[key_index] is not None:
            self._keys[key_index].execute()
