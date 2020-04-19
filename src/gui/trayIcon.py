import sys

from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QMenu, QAction

from . import mainWindow, configWindow


class TrayIconMenu(QMenu):

    def __init__(self, gui_window: mainWindow.MainWindow):
        super().__init__(None)
        self._gui_window = gui_window

        self._open_action = QAction(QCoreApplication.translate('tray_icon', 'Open'),
                                    triggered=self._open_window)
        self.addAction(self._open_action)
        self._settings_action = QAction(QCoreApplication.translate('tray_icon', 'Configs'),
                                        triggered=self._open_settings)
        self.addAction(self._settings_action)
        self._close_action = QAction(QCoreApplication.translate('tray_icon', 'Exit'),
                                     triggered=self._exit)
        self.addAction(self._close_action)

    def _open_window(self):
        self._gui_window.show()

    def _open_settings(self):
        self._config_window = configWindow.ConfigWindow(self._gui_window, self._gui_window.get_device_manager())
        self._config_window.show()

    def _exit(self):
        sys.exit()
