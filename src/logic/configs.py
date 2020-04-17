from abc import ABC, abstractmethod
from datetime import datetime


class ConfigContainer:

    @property
    @abstractmethod
    def _config(self):
        pass

    @abstractmethod
    def _persist_config(self):
        pass

    def _set__config(self, namespace, key, value):
        if namespace not in self._config:
            self._config[namespace] = {}
        self._config[namespace][key] = value
        self._persist_config()

    def _get_config(self, namespace, key, fallback=None):
        if namespace in self._config:
            if key in self._config[namespace]:
                return self._config[namespace][key]

        return fallback


class ApplicationConfig(ConfigContainer, ABC):
    __APPLICATION_CONFIG_NAMESPACE = 'Application'

    def __get_locale(self):
        return self._get_config(ApplicationConfig.__APPLICATION_CONFIG_NAMESPACE, 'locale', fallback='en')

    def __set_locale(self, locale):
        self._set__config(ApplicationConfig.__APPLICATION_CONFIG_NAMESPACE, 'locale', locale)

    locale = property(__get_locale, __set_locale)


class DeviceConfig(ConfigContainer, ABC):
    __DEVICE_CONFIG_NAMESPACE = 'Device'

    def __get_initial_connect(self):
        return self._get_config(DeviceConfig.__DEVICE_CONFIG_NAMESPACE, 'initial_connect')

    def __get_last_connect(self):
        return self._get_config(DeviceConfig.__DEVICE_CONFIG_NAMESPACE, 'last_connect')

    def _set_connect_time(self):
        if self.__get_initial_connect() is None:
            self._set__config(DeviceConfig.__DEVICE_CONFIG_NAMESPACE, 'initial_connect',
                              datetime.now().strftime("%d-%b-%Y %H:%M:%S"))
        self._set__config(DeviceConfig.__DEVICE_CONFIG_NAMESPACE, 'last_connect',
                          datetime.now().strftime("%d-%b-%Y %H:%M:%S"))

    initial_connect = property(__get_initial_connect)
    last_connect = property(__get_last_connect)
