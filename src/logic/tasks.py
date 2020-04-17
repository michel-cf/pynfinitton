from abc import ABC, abstractmethod

from pynput import keyboard


class BaseTask(ABC):

    def __init__(self, name: str = None, task_config: dict = None):
        self.name = name
        if task_config is not None:
            self._parse_config(task_config)

    def __get_name(self):
        return self.__name

    def __set_name(self, name: str):
        self.__name = name

    name = property(__get_name, __set_name)

    @abstractmethod
    def _parse_config(self, task_config: dict):
        pass

    @abstractmethod
    def execute(self):
        pass


class TypeTask(BaseTask):
    _keyboard = keyboard.Controller()

    def _parse_config(self, task_config: dict):
        self.__text = task_config['text']

    def execute(self):
        TypeTask._keyboard.type(self.__text)
