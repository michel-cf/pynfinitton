from abc import ABC, abstractmethod
from typing import Dict

from pynput import keyboard
from . import deviceAccessor, applicationExceptions


class BaseTask(ABC):
    TYPE = None

    def __init__(self, device_accessor: deviceAccessor.DeviceAccessor, name: str, task_config: dict = None):
        if self.TYPE is None:
            raise applicationExceptions.ImplementationException('Missing task type')

        self._device_accessor = device_accessor
        self.name = name
        if task_config is not None:
            self._parse_config(task_config)

    def __get_name(self):
        return self.__name

    def __set_name(self, name: str):
        self.__name = name

    name = property(__get_name, __set_name)

    @abstractmethod
    def _parse_config(self, task_config: Dict[str, str]):
        pass

    def get_config(self) -> Dict[str, str]:
        config = {
            'type': self.TYPE
        }
        config.update(self._get_task_config())
        return config

    @abstractmethod
    def _get_task_config(self) -> Dict[str, str]:
        return {}

    @abstractmethod
    def execute(self):
        pass


class TypeTask(BaseTask):
    TYPE = 'type'
    _keyboard = keyboard.Controller()

    def _parse_config(self, task_config: dict):
        self.__text = task_config['text']

    def _get_task_config(self) -> Dict[str, str]:
        return {
            'text': self.__text
        }

    def execute(self):
        TypeTask._keyboard.type(self.__text)


class ScreenTask(BaseTask):
    TYPE = 'screen'

    def _parse_config(self, task_config: dict):
        self.__screen = task_config['screen']

    def _get_task_config(self) -> Dict[str, str]:
        return {
            'screen': self.__screen
        }

    def execute(self):
        self._device_accessor.show_screen(self.__screen)
