from abc import ABC, abstractmethod


class DeviceAccessor(ABC):

    def __get_tasks(self):
        return self.__tasks

    def __set_tasks(self, tasks):
        self.__tasks = tasks

    tasks = property(__get_tasks, __set_tasks)

    def __get_screens(self):
        return self.__screens

    def __set_screens(self, screens):
        self.__screens = screens

    screens = property(__get_screens, __set_screens)

    @abstractmethod
    def show_screen(self, screen_name: str):
        pass
