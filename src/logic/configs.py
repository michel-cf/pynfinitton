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

    def _set_config(self, namespace: str, key: str, value: str):
        if namespace not in self._config:
            self._config[namespace] = {}
        self._config[namespace][key] = value
        self._persist_config()

    def _set_bool_config(self, namespace: str, key: str, value: bool):
        self._set_config(namespace, key, ('true' if value else 'false'))

    def _get_config(self, namespace: str, key: str, fallback: str = None) -> str:
        if namespace in self._config:
            if key in self._config[namespace]:
                return self._config[namespace][key]

        return fallback

    def _get_bool_config(self, namespace, key, fallback: bool = None) -> bool:
        value = self._get_config(namespace, key)
        if value is None:
            return fallback
        else:
            return value.lower() in ['yes', 'true', '1']


class ApplicationConfig(ConfigContainer, ABC):
    __APPLICATION_CONFIG_NAMESPACE = 'Application'

    def __get_locale(self):
        return self._get_config(ApplicationConfig.__APPLICATION_CONFIG_NAMESPACE, 'locale', fallback='en')

    def __set_locale(self, locale):
        self._set_config(ApplicationConfig.__APPLICATION_CONFIG_NAMESPACE, 'locale', locale)

    locale = property(__get_locale, __set_locale)

    def __get_open_on_start(self) -> bool:
        return self._get_bool_config(ApplicationConfig.__APPLICATION_CONFIG_NAMESPACE, 'open-on-start', fallback=True)

    def __set_open_on_start(self, open_on_start):
        self._set_bool_config(ApplicationConfig.__APPLICATION_CONFIG_NAMESPACE, 'open-on-start', open_on_start)

    open_on_start = property(__get_open_on_start, __set_open_on_start)


class DeviceConfig(ConfigContainer, ABC):
    __DEVICE_CONFIG_NAMESPACE = 'Device'

    def __get_initial_connect(self):
        return self._get_config(DeviceConfig.__DEVICE_CONFIG_NAMESPACE, 'initial_connect')

    def __get_last_connect(self):
        return self._get_config(DeviceConfig.__DEVICE_CONFIG_NAMESPACE, 'last_connect')

    def _set_connect_time(self):
        if self.__get_initial_connect() is None:
            self._set_config(DeviceConfig.__DEVICE_CONFIG_NAMESPACE, 'initial_connect',
                             datetime.now().strftime("%d-%b-%Y %H:%M:%S"))
        self._set_config(DeviceConfig.__DEVICE_CONFIG_NAMESPACE, 'last_connect',
                         datetime.now().strftime("%d-%b-%Y %H:%M:%S"))

    initial_connect = property(__get_initial_connect)
    last_connect = property(__get_last_connect)
